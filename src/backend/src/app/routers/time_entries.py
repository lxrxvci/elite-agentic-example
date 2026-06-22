"""Time entries router."""

from __future__ import annotations

import uuid
from datetime import UTC, datetime

from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.dependencies import CurrentUser, get_current_user, get_db
from app.exceptions import ConflictError, NotFoundError
from app.schemas import (
    PaginatedResponse,
    TimeEntryCreateSchema,
    TimeEntrySchema,
    TimeEntryUpdateSchema,
)
from domain.entities import Tenant, TimeEntry
from domain.services.time_entry import create_time_entry
from infrastructure.repositories import (
    ClientRepository,
    ProjectRepository,
    TenantRepository,
    TimeEntryRepository,
)

router = APIRouter(prefix="/time-entries", tags=["Time Entries"])


def _to_schema(entry: TimeEntry) -> TimeEntrySchema:
    return TimeEntrySchema(
        id=entry.id,
        tenant_id=entry.tenant_id,
        client_id=entry.client_id,
        project_id=entry.project_id,
        invoice_id=entry.invoice_id,
        description=entry.description,
        duration_minutes=entry.duration_minutes,
        rounded_minutes=entry.rounded_minutes,
        status=entry.status.value,
        started_at=entry.started_at,
        ended_at=entry.ended_at,
        created_at=entry.created_at,
        updated_at=entry.updated_at,
    )


@router.get("", response_model=PaginatedResponse)
def list_time_entries(
    client_id: uuid.UUID | None = None,
    project_id: uuid.UUID | None = None,
    status: str | None = None,
    limit: int = Query(20, ge=1, le=100),
    offset: int = Query(0, ge=0),
    user: CurrentUser = Depends(get_current_user),
    db: Session = Depends(get_db),
) -> PaginatedResponse:
    repo = TimeEntryRepository(db, user.tenant_id)
    entries = repo.list(
        client_id=client_id,
        project_id=project_id,
        status=status,
        limit=limit,
        offset=offset,
    )
    return PaginatedResponse(
        items=[_to_schema(e) for e in entries],
        total=len(entries),
        limit=limit,
        offset=offset,
    )


@router.post("", response_model=TimeEntrySchema, status_code=201)
def create_time_entry_endpoint(
    payload: TimeEntryCreateSchema,
    user: CurrentUser = Depends(get_current_user),
    db: Session = Depends(get_db),
) -> TimeEntrySchema:
    tenant_repo = TenantRepository(db, user.tenant_id)
    tenant_orm = tenant_repo.get()
    if not tenant_orm:
        raise NotFoundError("Tenant not found")

    client_repo = ClientRepository(db, user.tenant_id)
    client = client_repo.get(payload.client_id)
    if not client:
        raise NotFoundError("Client not found")

    project_repo = ProjectRepository(db, user.tenant_id)
    project = project_repo.get(payload.project_id)
    if not project:
        raise NotFoundError("Project not found")
    if project.client_id != client.id:
        raise ConflictError("Project does not belong to the selected client")

    tenant = Tenant(
        id=tenant_orm.id,
        name=tenant_orm.name,
        default_currency=tenant_orm.default_currency,
        default_hourly_rate=tenant_orm.default_hourly_rate,
    )

    entry = create_time_entry(
        tenant=tenant,
        project=project,
        description=payload.description,
        duration_minutes=payload.duration_minutes,
        started_at=payload.started_at,
        ended_at=payload.ended_at,
    )

    repo = TimeEntryRepository(db, user.tenant_id)
    created = repo.create(entry)
    db.commit()
    return _to_schema(created)


@router.get("/{time_entry_id}", response_model=TimeEntrySchema)
def get_time_entry(
    time_entry_id: uuid.UUID,
    user: CurrentUser = Depends(get_current_user),
    db: Session = Depends(get_db),
) -> TimeEntrySchema:
    repo = TimeEntryRepository(db, user.tenant_id)
    entry = repo.get(time_entry_id)
    if not entry:
        raise NotFoundError("Time entry not found")
    return _to_schema(entry)


@router.patch("/{time_entry_id}", response_model=TimeEntrySchema)
def update_time_entry(
    time_entry_id: uuid.UUID,
    payload: TimeEntryUpdateSchema,
    user: CurrentUser = Depends(get_current_user),
    db: Session = Depends(get_db),
) -> TimeEntrySchema:
    repo = TimeEntryRepository(db, user.tenant_id)
    entry = repo.get(time_entry_id)
    if not entry:
        raise NotFoundError("Time entry not found")
    if entry.status.value == "billed":
        raise ConflictError("Cannot edit a billed time entry")

    if payload.description is not None:
        entry.description = payload.description
    if payload.duration_minutes is not None:
        entry.duration_minutes = payload.duration_minutes
        entry.rounded_minutes = (
            payload.duration_minutes
        )  # Simplified; should re-apply project rounding
    if payload.started_at is not None:
        entry.started_at = payload.started_at
    if payload.ended_at is not None:
        entry.ended_at = payload.ended_at
    entry.updated_at = datetime.now(UTC)

    updated = repo.update(entry)
    db.commit()
    return _to_schema(updated)
