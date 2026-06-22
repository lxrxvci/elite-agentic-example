"""Domain entities (framework-independent)."""

from __future__ import annotations

import uuid
from dataclasses import dataclass, field
from datetime import UTC, date, datetime
from decimal import Decimal
from enum import StrEnum

from domain.value_objects import Money


class TimeEntryStatus(StrEnum):
    UNBILLED = "unbilled"
    BILLED = "billed"
    WRITTEN_OFF = "written_off"


class InvoiceStatus(StrEnum):
    DRAFT = "draft"
    SENT = "sent"
    PAID = "paid"
    OVERDUE = "overdue"
    CANCELLED = "cancelled"


@dataclass
class Tenant:
    id: uuid.UUID
    name: str
    default_currency: str = "USD"
    default_hourly_rate: Decimal | None = None
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))
    updated_at: datetime = field(default_factory=lambda: datetime.now(UTC))


@dataclass
class User:
    id: uuid.UUID
    tenant_id: uuid.UUID
    email: str
    name: str
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))
    updated_at: datetime = field(default_factory=lambda: datetime.now(UTC))


@dataclass
class Client:
    id: uuid.UUID
    tenant_id: uuid.UUID
    name: str
    email: str | None = None
    currency: str = "USD"
    default_hourly_rate: Decimal | None = None
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))
    updated_at: datetime = field(default_factory=lambda: datetime.now(UTC))


@dataclass
class Project:
    id: uuid.UUID
    tenant_id: uuid.UUID
    client_id: uuid.UUID
    name: str
    rounding_minutes: int = 15
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))
    updated_at: datetime = field(default_factory=lambda: datetime.now(UTC))

    def round_minutes(self, duration_minutes: int) -> int:
        step = self.rounding_minutes
        if step <= 0:
            return duration_minutes
        return ((duration_minutes + step // 2) // step) * step


@dataclass
class TimeEntry:
    id: uuid.UUID
    tenant_id: uuid.UUID
    client_id: uuid.UUID
    project_id: uuid.UUID
    description: str
    duration_minutes: int
    rounded_minutes: int
    status: TimeEntryStatus
    invoice_id: uuid.UUID | None = None
    started_at: datetime | None = None
    ended_at: datetime | None = None
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))
    updated_at: datetime = field(default_factory=lambda: datetime.now(UTC))

    def mark_billed(self, invoice_id: uuid.UUID) -> None:
        if self.status == TimeEntryStatus.BILLED:
            raise ValueError("Time entry is already billed")
        self.status = TimeEntryStatus.BILLED
        self.invoice_id = invoice_id
        self.updated_at = datetime.now(UTC)


@dataclass
class InvoiceLineItem:
    id: uuid.UUID
    description: str
    quantity: Decimal
    rate: Decimal
    amount: Money
    time_entry_ids: list[uuid.UUID]


@dataclass
class Invoice:
    id: uuid.UUID
    tenant_id: uuid.UUID
    client_id: uuid.UUID
    status: InvoiceStatus
    issue_date: date
    due_date: date
    subtotal: Money
    tax: Money
    total: Money
    line_items: list[InvoiceLineItem]
    notes: str | None = None
    idempotency_key: str | None = None
    payment_method: str | None = None
    paid_at: datetime | None = None
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))
    updated_at: datetime = field(default_factory=lambda: datetime.now(UTC))

    def mark_paid(self, payment_method: str, paid_at: datetime | None = None) -> None:
        if self.status == InvoiceStatus.PAID:
            raise ValueError("Invoice is already paid")
        self.status = InvoiceStatus.PAID
        self.payment_method = payment_method
        self.paid_at = paid_at or datetime.now(UTC)
        self.updated_at = datetime.now(UTC)
