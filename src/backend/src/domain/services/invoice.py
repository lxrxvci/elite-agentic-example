"""Invoice domain service."""

from __future__ import annotations

import uuid
from datetime import UTC, date, datetime
from decimal import Decimal

from domain.entities import Client, Invoice, InvoiceLineItem, InvoiceStatus, TimeEntry
from domain.value_objects import Money


def create_invoice_from_time_entries(
    tenant_id: uuid.UUID,
    client: Client,
    time_entries: list[TimeEntry],
    issue_date: date,
    due_date: date,
    notes: str | None = None,
    idempotency_key: str | None = None,
) -> Invoice:
    """Create an invoice from unbilled time entries and mark them billed."""
    if not time_entries:
        raise ValueError("At least one time entry is required")

    for entry in time_entries:
        if entry.tenant_id != tenant_id:
            raise ValueError("All time entries must belong to the same tenant")
        if entry.client_id != client.id:
            raise ValueError("All time entries must belong to the invoice client")

    currency = client.currency
    rate = client.default_hourly_rate or Decimal("0.00")

    line_items: list[InvoiceLineItem] = []
    for entry in time_entries:
        hours = Decimal(entry.rounded_minutes) / Decimal("60")
        amount = Money(amount=rate * hours, currency=currency)
        line_item = InvoiceLineItem(
            id=uuid.uuid4(),
            description=entry.description,
            quantity=hours.quantize(Decimal("0.01")),
            rate=rate,
            amount=amount,
            time_entry_ids=[entry.id],
        )
        line_items.append(line_item)

    subtotal = sum(
        (li.amount for li in line_items), Money(amount=Decimal("0.00"), currency=currency)
    )
    tax = Money(amount=Decimal("0.00"), currency=currency)
    total = subtotal + tax

    invoice_id = uuid.uuid4()
    invoice = Invoice(
        id=invoice_id,
        tenant_id=tenant_id,
        client_id=client.id,
        status=InvoiceStatus.DRAFT,
        issue_date=issue_date,
        due_date=due_date,
        subtotal=subtotal,
        tax=tax,
        total=total,
        line_items=line_items,
        notes=notes,
        idempotency_key=idempotency_key,
        created_at=datetime.now(UTC),
        updated_at=datetime.now(UTC),
    )

    for entry in time_entries:
        entry.mark_billed(invoice_id)

    return invoice
