"""Clients router."""

from __future__ import annotations

import uuid
from decimal import Decimal

from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.dependencies import CurrentUser, get_current_user, get_db
from app.exceptions import NotFoundError
from app.schemas import ClientCreateSchema, ClientSchema, PaginatedResponse
from domain.entities import Client
from infrastructure.repositories import ClientRepository

router = APIRouter(prefix="/clients", tags=["Clients"])


def _to_schema(client: Client) -> ClientSchema:
    return ClientSchema(
        id=client.id,
        tenant_id=client.tenant_id,
        name=client.name,
        email=client.email,
        currency=client.currency,
        default_hourly_rate=str(client.default_hourly_rate) if client.default_hourly_rate else None,
        created_at=client.created_at,
        updated_at=client.updated_at,
    )


@router.get("", response_model=PaginatedResponse)
def list_clients(
    limit: int = Query(20, ge=1, le=100),
    offset: int = Query(0, ge=0),
    user: CurrentUser = Depends(get_current_user),
    db: Session = Depends(get_db),
) -> PaginatedResponse:
    repo = ClientRepository(db, user.tenant_id)
    clients = repo.list(limit=limit, offset=offset)
    return PaginatedResponse(
        items=[_to_schema(c) for c in clients],
        total=len(clients),
        limit=limit,
        offset=offset,
    )


@router.post("", response_model=ClientSchema, status_code=201)
def create_client(
    payload: ClientCreateSchema,
    user: CurrentUser = Depends(get_current_user),
    db: Session = Depends(get_db),
) -> ClientSchema:
    repo = ClientRepository(db, user.tenant_id)
    client = Client(
        id=uuid.uuid4(),
        tenant_id=user.tenant_id,
        name=payload.name,
        email=payload.email,
        currency=payload.currency,
        default_hourly_rate=Decimal(payload.default_hourly_rate)
        if payload.default_hourly_rate
        else None,
    )
    created = repo.create(client)
    db.commit()
    return _to_schema(created)


@router.get("/{client_id}", response_model=ClientSchema)
def get_client(
    client_id: uuid.UUID,
    user: CurrentUser = Depends(get_current_user),
    db: Session = Depends(get_db),
) -> ClientSchema:
    repo = ClientRepository(db, user.tenant_id)
    client = repo.get(client_id)
    if not client:
        raise NotFoundError("Client not found")
    return _to_schema(client)
