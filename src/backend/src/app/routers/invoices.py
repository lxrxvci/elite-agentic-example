"""Invoices router."""

from __future__ import annotations

import uuid

from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.dependencies import CurrentUser, get_current_user, get_db
from app.exceptions import ConflictError, NotFoundError
from app.schemas import (
    InvoiceCreateSchema,
    InvoiceLineItemSchema,
    InvoiceMarkPaidSchema,
    InvoiceSchema,
    MoneySchema,
    PaginatedResponse,
)
from domain.entities import InvoiceStatus
from domain.services.invoice import create_invoice_from_time_entries
from infrastructure.repositories import (
    ClientRepository,
    InvoiceRepository,
    TimeEntryRepository,
)

router = APIRouter(prefix="/invoices", tags=["Invoices"])


def _to_schema(invoice) -> InvoiceSchema:  # type: ignore[no-untyped-def]
    return InvoiceSchema(
        id=invoice.id,
        tenant_id=invoice.tenant_id,
        client_id=invoice.client_id,
        status=invoice.status.value,
        issue_date=invoice.issue_date,
        due_date=invoice.due_date,
        subtotal=MoneySchema(
            amount=str(invoice.subtotal.amount), currency=invoice.subtotal.currency
        ),
        tax=MoneySchema(amount=str(invoice.tax.amount), currency=invoice.tax.currency),
        total=MoneySchema(amount=str(invoice.total.amount), currency=invoice.total.currency),
        line_items=[
            InvoiceLineItemSchema(
                id=li.id,
                description=li.description,
                quantity=str(li.quantity),
                rate=str(li.rate),
                amount=MoneySchema(amount=str(li.amount.amount), currency=li.amount.currency),
                time_entry_ids=li.time_entry_ids,
            )
            for li in invoice.line_items
        ],
        notes=invoice.notes,
        created_at=invoice.created_at,
        updated_at=invoice.updated_at,
    )


@router.get("", response_model=PaginatedResponse)
def list_invoices(
    client_id: uuid.UUID | None = None,
    status: str | None = None,
    limit: int = Query(20, ge=1, le=100),
    offset: int = Query(0, ge=0),
    user: CurrentUser = Depends(get_current_user),
    db: Session = Depends(get_db),
) -> PaginatedResponse:
    repo = InvoiceRepository(db, user.tenant_id)
    invoices = repo.list(client_id=client_id, status=status, limit=limit, offset=offset)
    return PaginatedResponse(
        items=[_to_schema(inv) for inv in invoices],
        total=len(invoices),
        limit=limit,
        offset=offset,
    )


@router.post("", response_model=InvoiceSchema, status_code=201)
def create_invoice(
    payload: InvoiceCreateSchema,
    user: CurrentUser = Depends(get_current_user),
    db: Session = Depends(get_db),
) -> InvoiceSchema:
    client_repo = ClientRepository(db, user.tenant_id)
    client = client_repo.get(payload.client_id)
    if not client:
        raise NotFoundError("Client not found")

    time_entry_repo = TimeEntryRepository(db, user.tenant_id)
    time_entries = time_entry_repo.get_many(payload.time_entry_ids)
    if len(time_entries) != len(payload.time_entry_ids):
        raise NotFoundError("One or more time entries not found")

    for entry in time_entries:
        if entry.status.value != "unbilled":
            raise ConflictError(f"Time entry {entry.id} is not available for invoicing")

    invoice = create_invoice_from_time_entries(
        tenant_id=user.tenant_id,
        client=client,
        time_entries=time_entries,
        issue_date=payload.issue_date,
        due_date=payload.due_date,
        notes=payload.notes,
        idempotency_key=payload.idempotency_key,
    )

    invoice_repo = InvoiceRepository(db, user.tenant_id)
    created = invoice_repo.create(invoice)
    for entry in time_entries:
        time_entry_repo.update(entry)
    db.commit()
    return _to_schema(created)


@router.get("/{invoice_id}", response_model=InvoiceSchema)
def get_invoice(
    invoice_id: uuid.UUID,
    user: CurrentUser = Depends(get_current_user),
    db: Session = Depends(get_db),
) -> InvoiceSchema:
    repo = InvoiceRepository(db, user.tenant_id)
    invoice = repo.get(invoice_id)
    if not invoice:
        raise NotFoundError("Invoice not found")
    return _to_schema(invoice)


@router.post("/{invoice_id}/mark-paid", response_model=InvoiceSchema)
def mark_invoice_paid(
    invoice_id: uuid.UUID,
    payload: InvoiceMarkPaidSchema,
    user: CurrentUser = Depends(get_current_user),
    db: Session = Depends(get_db),
) -> InvoiceSchema:
    repo = InvoiceRepository(db, user.tenant_id)
    invoice = repo.get(invoice_id)
    if not invoice:
        raise NotFoundError("Invoice not found")
    if invoice.status == InvoiceStatus.PAID:
        raise ConflictError("Invoice is already paid")

    invoice.mark_paid(payload.payment_method, payload.paid_at)
    updated = repo.update(invoice)
    db.commit()
    return _to_schema(updated)
