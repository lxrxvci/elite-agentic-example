"""Pydantic request/response schemas aligned with openapi.yaml."""

from __future__ import annotations

from datetime import date, datetime
from typing import Any
from uuid import UUID

from pydantic import BaseModel, ConfigDict, EmailStr, Field, ValidationInfo, field_validator


class MoneySchema(BaseModel):
    amount: str = Field(..., pattern=r"^-?\d+(\.\d{1,2})?$")
    currency: str = Field(..., min_length=3, max_length=3)


class TenantSchema(BaseModel):
    id: UUID
    name: str
    default_currency: str
    default_hourly_rate: str | None = None


class CurrentUserSchema(BaseModel):
    id: UUID
    email: EmailStr
    name: str
    tenant: TenantSchema


class ClientCreateSchema(BaseModel):
    name: str = Field(..., min_length=1, max_length=255)
    email: EmailStr | None = None
    currency: str = Field(default="USD", min_length=3, max_length=3)
    default_hourly_rate: str | None = Field(None, pattern=r"^\d+(\.\d{1,2})?$")


class ClientSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    tenant_id: UUID
    name: str
    email: str | None = None
    currency: str
    default_hourly_rate: str | None = None
    created_at: datetime
    updated_at: datetime


class ProjectCreateSchema(BaseModel):
    client_id: UUID
    name: str = Field(..., min_length=1, max_length=255)
    rounding_minutes: int = Field(default=15, ge=1)


class ProjectSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    tenant_id: UUID
    client_id: UUID
    name: str
    rounding_minutes: int
    created_at: datetime
    updated_at: datetime


class TimeEntryCreateSchema(BaseModel):
    client_id: UUID
    project_id: UUID
    description: str = Field(..., min_length=1, max_length=2000)
    duration_minutes: int | None = Field(None, ge=0)
    started_at: datetime | None = None
    ended_at: datetime | None = None

    @field_validator("duration_minutes")
    @classmethod
    def validate_duration_or_timestamps(cls, v: int | None, info: ValidationInfo) -> int | None:
        data = info.data
        if v is None and (data.get("started_at") is None or data.get("ended_at") is None):
            raise ValueError("Either duration_minutes or both started_at and ended_at are required")
        return v


class TimeEntryUpdateSchema(BaseModel):
    description: str | None = Field(None, min_length=1, max_length=2000)
    duration_minutes: int | None = Field(None, ge=0)
    started_at: datetime | None = None
    ended_at: datetime | None = None


class TimeEntrySchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    tenant_id: UUID
    client_id: UUID
    project_id: UUID
    invoice_id: UUID | None = None
    description: str
    duration_minutes: int
    rounded_minutes: int
    status: str
    started_at: datetime | None = None
    ended_at: datetime | None = None
    created_at: datetime
    updated_at: datetime


class InvoiceLineItemSchema(BaseModel):
    id: UUID
    description: str
    quantity: str
    rate: str
    amount: MoneySchema
    time_entry_ids: list[UUID]


class InvoiceSchema(BaseModel):
    id: UUID
    tenant_id: UUID
    client_id: UUID
    status: str
    issue_date: date
    due_date: date
    subtotal: MoneySchema
    tax: MoneySchema
    total: MoneySchema
    line_items: list[InvoiceLineItemSchema]
    notes: str | None = None
    created_at: datetime
    updated_at: datetime


class InvoiceCreateSchema(BaseModel):
    client_id: UUID
    time_entry_ids: list[UUID] = Field(..., min_length=1)
    issue_date: date
    due_date: date
    notes: str | None = Field(None, max_length=2000)
    idempotency_key: str | None = Field(None, max_length=255)


class InvoiceMarkPaidSchema(BaseModel):
    payment_method: str = Field(..., pattern=r"^(bank_transfer|card|cash|check|other)$")
    paid_at: datetime | None = None


class PaginatedResponse(BaseModel):
    items: list[Any]
    total: int
    limit: int
    offset: int
