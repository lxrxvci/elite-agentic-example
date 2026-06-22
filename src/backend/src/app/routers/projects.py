"""Projects router."""

from __future__ import annotations

import uuid

from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.dependencies import CurrentUser, get_current_user, get_db
from app.exceptions import NotFoundError
from app.schemas import PaginatedResponse, ProjectCreateSchema, ProjectSchema
from domain.entities import Project
from infrastructure.repositories import ClientRepository, ProjectRepository

router = APIRouter(prefix="/projects", tags=["Projects"])


def _to_schema(project: Project) -> ProjectSchema:
    return ProjectSchema(
        id=project.id,
        tenant_id=project.tenant_id,
        client_id=project.client_id,
        name=project.name,
        rounding_minutes=project.rounding_minutes,
        created_at=project.created_at,
        updated_at=project.updated_at,
    )


@router.get("", response_model=PaginatedResponse)
def list_projects(
    client_id: uuid.UUID | None = None,
    limit: int = Query(20, ge=1, le=100),
    offset: int = Query(0, ge=0),
    user: CurrentUser = Depends(get_current_user),
    db: Session = Depends(get_db),
) -> PaginatedResponse:
    repo = ProjectRepository(db, user.tenant_id)
    projects = repo.list(client_id=client_id, limit=limit, offset=offset)
    return PaginatedResponse(
        items=[_to_schema(p) for p in projects],
        total=len(projects),
        limit=limit,
        offset=offset,
    )


@router.post("", response_model=ProjectSchema, status_code=201)
def create_project(
    payload: ProjectCreateSchema,
    user: CurrentUser = Depends(get_current_user),
    db: Session = Depends(get_db),
) -> ProjectSchema:
    client_repo = ClientRepository(db, user.tenant_id)
    client = client_repo.get(payload.client_id)
    if not client:
        raise NotFoundError("Client not found")

    repo = ProjectRepository(db, user.tenant_id)
    project = Project(
        id=uuid.uuid4(),
        tenant_id=user.tenant_id,
        client_id=payload.client_id,
        name=payload.name,
        rounding_minutes=payload.rounding_minutes,
    )
    created = repo.create(project)
    db.commit()
    return _to_schema(created)


@router.get("/{project_id}", response_model=ProjectSchema)
def get_project(
    project_id: uuid.UUID,
    user: CurrentUser = Depends(get_current_user),
    db: Session = Depends(get_db),
) -> ProjectSchema:
    repo = ProjectRepository(db, user.tenant_id)
    project = repo.get(project_id)
    if not project:
        raise NotFoundError("Project not found")
    return _to_schema(project)
