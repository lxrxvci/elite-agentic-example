"""Current user router."""

from fastapi import APIRouter, Depends

from app.dependencies import (
    CurrentTenant,
    CurrentUser,
    get_current_tenant,
    get_current_user,
)
from app.schemas import CurrentUserSchema, TenantSchema

router = APIRouter(tags=["Users"])


@router.get("/me", response_model=CurrentUserSchema)
def get_current_user_endpoint(
    user: CurrentUser = Depends(get_current_user),
    tenant: CurrentTenant = Depends(get_current_tenant),
) -> CurrentUserSchema:
    return CurrentUserSchema(
        id=user.id,
        email=user.email,
        name=user.name,
        tenant=TenantSchema(
            id=tenant.id,
            name=tenant.name,
            default_currency=tenant.default_currency,
            default_hourly_rate=str(tenant.default_hourly_rate)
            if tenant.default_hourly_rate
            else None,
        ),
    )
