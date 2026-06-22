"""FastAPI dependencies for auth, database, and tenant isolation."""

from __future__ import annotations

import uuid
from datetime import UTC, datetime, timedelta
from typing import Any

from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from jose import JWTError, jwt
from passlib.context import CryptContext
from pydantic import BaseModel
from sqlalchemy.orm import Session

from app.config import settings
from app.features import is_feature_enabled
from infrastructure.database import get_db
from infrastructure.models import Tenant as TenantORM
from infrastructure.models import User as UserORM

__all__ = [
    "CurrentUser",
    "CurrentTenant",
    "create_access_token",
    "get_current_user",
    "get_current_tenant",
    "get_db",
    "is_feature_enabled",
]

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
security = HTTPBearer(auto_error=False)


class CurrentUser(BaseModel):
    id: uuid.UUID
    email: str
    name: str
    tenant_id: uuid.UUID


class CurrentTenant(BaseModel):
    id: uuid.UUID
    name: str
    default_currency: str
    default_hourly_rate: float | None = None


def create_access_token(
    user_id: uuid.UUID,
    email: str,
    name: str,
    tenant_id: uuid.UUID,
    expires_delta: timedelta | None = None,
) -> str:
    to_encode: dict[str, Any] = {
        "sub": str(user_id),
        "email": email,
        "name": name,
        "tenant_id": str(tenant_id),
    }
    expire = datetime.now(UTC) + (
        expires_delta or timedelta(minutes=settings.access_token_expire_minutes)
    )
    to_encode["exp"] = expire
    return jwt.encode(to_encode, settings.secret_key, algorithm=settings.algorithm)


def _decode_token(token: str) -> dict[str, Any]:
    try:
        payload = jwt.decode(token, settings.secret_key, algorithms=[settings.algorithm])
        return payload
    except JWTError as exc:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials",
            headers={"WWW-Authenticate": "Bearer"},
        ) from exc


def get_current_user(
    credentials: HTTPAuthorizationCredentials | None = Depends(security),
    db: Session = Depends(get_db),
) -> CurrentUser:
    if not credentials:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Not authenticated",
            headers={"WWW-Authenticate": "Bearer"},
        )
    payload = _decode_token(credentials.credentials)
    user_id = uuid.UUID(payload.get("sub"))
    user = db.query(UserORM).filter(UserORM.id == user_id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="User not found")
    return CurrentUser(
        id=user.id,
        email=user.email,
        name=user.name,
        tenant_id=user.tenant_id,
    )


def get_current_tenant(
    user: CurrentUser = Depends(get_current_user),
    db: Session = Depends(get_db),
) -> CurrentTenant:
    tenant = db.query(TenantORM).filter(TenantORM.id == user.tenant_id).first()
    if not tenant:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Tenant not found")
    return CurrentTenant(
        id=tenant.id,
        name=tenant.name,
        default_currency=tenant.default_currency,
        default_hourly_rate=float(tenant.default_hourly_rate)
        if tenant.default_hourly_rate
        else None,
    )


# is_feature_enabled is re-exported from app.features for backward compatibility.
# It supports Unleash when configured and falls back to ENABLED_FEATURES env var.
