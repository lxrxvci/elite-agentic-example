"""SQLAlchemy repositories with tenant isolation."""

from __future__ import annotations

import builtins
import uuid
from typing import Generic, TypeVar

from sqlalchemy.orm import Session

from domain.entities import (
    Client,
    Invoice,
    InvoiceLineItem,
    InvoiceStatus,
    Project,
    Tenant,
    TimeEntry,
    TimeEntryStatus,
    User,
)
from domain.value_objects import Money
from infrastructure import models

T = TypeVar("T")


class BaseRepository(Generic[T]):
    def __init__(self, session: Session, tenant_id: uuid.UUID) -> None:
        self.session = session
        self.tenant_id = tenant_id


class TenantRepository(BaseRepository[Tenant]):
    def get(self) -> Tenant | None:
        orm = self.session.query(models.Tenant).filter(models.Tenant.id == self.tenant_id).first()
        if not orm:
            return None
        return Tenant(
            id=orm.id,
            name=orm.name,
            default_currency=orm.default_currency,
            default_hourly_rate=orm.default_hourly_rate,
        )

    def create(self, tenant: Tenant) -> Tenant:
        orm = models.Tenant(
            id=tenant.id,
            name=tenant.name,
            default_currency=tenant.default_currency,
            default_hourly_rate=tenant.default_hourly_rate,
        )
        self.session.add(orm)
        self.session.flush()
        return tenant


class UserRepository(BaseRepository[User]):
    def get_by_email(self, email: str) -> User | None:
        orm = (
            self.session.query(models.User)
            .filter(models.User.tenant_id == self.tenant_id)
            .filter(models.User.email == email)
            .first()
        )
        if not orm:
            return None
        return User(
            id=orm.id,
            tenant_id=orm.tenant_id,
            email=orm.email,
            name=orm.name,
        )

    def create(self, user: User) -> User:
        orm = models.User(
            id=user.id,
            tenant_id=user.tenant_id,
            email=user.email,
            name=user.name,
        )
        self.session.add(orm)
        self.session.flush()
        return user


class ClientRepository(BaseRepository[Client]):
    def list(self, limit: int = 20, offset: int = 0) -> builtins.list[Client]:
        orms = (
            self.session.query(models.Client)
            .filter(models.Client.tenant_id == self.tenant_id)
            .offset(offset)
            .limit(limit)
            .all()
        )
        return [
            Client(
                id=orm.id,
                tenant_id=orm.tenant_id,
                name=orm.name,
                email=orm.email,
                currency=orm.currency,
                default_hourly_rate=orm.default_hourly_rate,
            )
            for orm in orms
        ]

    def get(self, client_id: uuid.UUID) -> Client | None:
        orm = (
            self.session.query(models.Client)
            .filter(models.Client.tenant_id == self.tenant_id)
            .filter(models.Client.id == client_id)
            .first()
        )
        if not orm:
            return None
        return Client(
            id=orm.id,
            tenant_id=orm.tenant_id,
            name=orm.name,
            email=orm.email,
            currency=orm.currency,
            default_hourly_rate=orm.default_hourly_rate,
        )

    def create(self, client: Client) -> Client:
        orm = models.Client(
            id=client.id,
            tenant_id=client.tenant_id,
            name=client.name,
            email=client.email,
            currency=client.currency,
            default_hourly_rate=client.default_hourly_rate,
        )
        self.session.add(orm)
        self.session.flush()
        return client


class ProjectRepository(BaseRepository[Project]):
    def list(
        self, client_id: uuid.UUID | None = None, limit: int = 20, offset: int = 0
    ) -> builtins.list[Project]:
        query = self.session.query(models.Project).filter(
            models.Project.tenant_id == self.tenant_id
        )
        if client_id:
            query = query.filter(models.Project.client_id == client_id)
        orms = query.offset(offset).limit(limit).all()
        return [
            Project(
                id=orm.id,
                tenant_id=orm.tenant_id,
                client_id=orm.client_id,
                name=orm.name,
                rounding_minutes=orm.rounding_minutes,
            )
            for orm in orms
        ]

    def get(self, project_id: uuid.UUID) -> Project | None:
        orm = (
            self.session.query(models.Project)
            .filter(models.Project.tenant_id == self.tenant_id)
            .filter(models.Project.id == project_id)
            .first()
        )
        if not orm:
            return None
        return Project(
            id=orm.id,
            tenant_id=orm.tenant_id,
            client_id=orm.client_id,
            name=orm.name,
            rounding_minutes=orm.rounding_minutes,
        )

    def create(self, project: Project) -> Project:
        orm = models.Project(
            id=project.id,
            tenant_id=project.tenant_id,
            client_id=project.client_id,
            name=project.name,
            rounding_minutes=project.rounding_minutes,
        )
        self.session.add(orm)
        self.session.flush()
        return project


class TimeEntryRepository(BaseRepository[TimeEntry]):
    def list(
        self,
        client_id: uuid.UUID | None = None,
        project_id: uuid.UUID | None = None,
        status: str | None = None,
        limit: int = 20,
        offset: int = 0,
    ) -> builtins.list[TimeEntry]:
        query = self.session.query(models.TimeEntry).filter(
            models.TimeEntry.tenant_id == self.tenant_id
        )
        if client_id:
            query = query.filter(models.TimeEntry.client_id == client_id)
        if project_id:
            query = query.filter(models.TimeEntry.project_id == project_id)
        if status:
            query = query.filter(models.TimeEntry.status == status)
        orms = query.order_by(models.TimeEntry.created_at.desc()).offset(offset).limit(limit).all()
        return [self._to_domain(orm) for orm in orms]

    def get(self, time_entry_id: uuid.UUID) -> TimeEntry | None:
        orm = (
            self.session.query(models.TimeEntry)
            .filter(models.TimeEntry.tenant_id == self.tenant_id)
            .filter(models.TimeEntry.id == time_entry_id)
            .first()
        )
        if not orm:
            return None
        return self._to_domain(orm)

    def get_many(self, ids: builtins.list[uuid.UUID]) -> builtins.list[TimeEntry]:
        orms = (
            self.session.query(models.TimeEntry)
            .filter(models.TimeEntry.tenant_id == self.tenant_id)
            .filter(models.TimeEntry.id.in_(ids))
            .all()
        )
        return [self._to_domain(orm) for orm in orms]

    def create(self, time_entry: TimeEntry) -> TimeEntry:
        orm = models.TimeEntry(
            id=time_entry.id,
            tenant_id=time_entry.tenant_id,
            client_id=time_entry.client_id,
            project_id=time_entry.project_id,
            invoice_id=time_entry.invoice_id,
            description=time_entry.description,
            duration_minutes=time_entry.duration_minutes,
            rounded_minutes=time_entry.rounded_minutes,
            status=time_entry.status.value,
            started_at=time_entry.started_at,
            ended_at=time_entry.ended_at,
        )
        self.session.add(orm)
        self.session.flush()
        return time_entry

    def update(self, time_entry: TimeEntry) -> TimeEntry:
        orm = (
            self.session.query(models.TimeEntry)
            .filter(models.TimeEntry.tenant_id == self.tenant_id)
            .filter(models.TimeEntry.id == time_entry.id)
            .first()
        )
        if not orm:
            raise ValueError("Time entry not found")
        orm.description = time_entry.description
        orm.duration_minutes = time_entry.duration_minutes
        orm.rounded_minutes = time_entry.rounded_minutes
        orm.status = time_entry.status.value
        orm.invoice_id = time_entry.invoice_id
        orm.started_at = time_entry.started_at
        orm.ended_at = time_entry.ended_at
        self.session.flush()
        return time_entry

    def _to_domain(self, orm: models.TimeEntry) -> TimeEntry:
        return TimeEntry(
            id=orm.id,
            tenant_id=orm.tenant_id,
            client_id=orm.client_id,
            project_id=orm.project_id,
            description=orm.description,
            duration_minutes=orm.duration_minutes,
            rounded_minutes=orm.rounded_minutes,
            status=TimeEntryStatus(orm.status),
            invoice_id=orm.invoice_id,
            started_at=orm.started_at,
            ended_at=orm.ended_at,
            created_at=orm.created_at,
            updated_at=orm.updated_at,
        )


class InvoiceRepository(BaseRepository[Invoice]):
    def list(
        self,
        client_id: uuid.UUID | None = None,
        status: str | None = None,
        limit: int = 20,
        offset: int = 0,
    ) -> builtins.list[Invoice]:
        query = self.session.query(models.Invoice).filter(
            models.Invoice.tenant_id == self.tenant_id
        )
        if client_id:
            query = query.filter(models.Invoice.client_id == client_id)
        if status:
            query = query.filter(models.Invoice.status == status)
        orms = query.order_by(models.Invoice.created_at.desc()).offset(offset).limit(limit).all()
        return [self._to_domain(orm) for orm in orms]

    def get(self, invoice_id: uuid.UUID) -> Invoice | None:
        orm = (
            self.session.query(models.Invoice)
            .filter(models.Invoice.tenant_id == self.tenant_id)
            .filter(models.Invoice.id == invoice_id)
            .first()
        )
        if not orm:
            return None
        return self._to_domain(orm)

    def create(self, invoice: Invoice) -> Invoice:
        orm = models.Invoice(
            id=invoice.id,
            tenant_id=invoice.tenant_id,
            client_id=invoice.client_id,
            status=invoice.status.value,
            issue_date=invoice.issue_date,
            due_date=invoice.due_date,
            subtotal_amount=invoice.subtotal.amount,
            subtotal_currency=invoice.subtotal.currency,
            tax_amount=invoice.tax.amount,
            tax_currency=invoice.tax.currency,
            total_amount=invoice.total.amount,
            total_currency=invoice.total.currency,
            notes=invoice.notes,
            idempotency_key=invoice.idempotency_key,
            payment_method=invoice.payment_method,
            paid_at=invoice.paid_at,
        )
        self.session.add(orm)
        self.session.flush()

        for line_item in invoice.line_items:
            line_orm = models.InvoiceLineItem(
                id=line_item.id,
                invoice_id=invoice.id,
                description=line_item.description,
                quantity=line_item.quantity,
                rate=line_item.rate,
                amount_amount=line_item.amount.amount,
                amount_currency=line_item.amount.currency,
                time_entry_ids=[str(te_id) for te_id in line_item.time_entry_ids],
            )
            self.session.add(line_orm)

        self.session.flush()
        return invoice

    def update(self, invoice: Invoice) -> Invoice:
        orm = (
            self.session.query(models.Invoice)
            .filter(models.Invoice.tenant_id == self.tenant_id)
            .filter(models.Invoice.id == invoice.id)
            .first()
        )
        if not orm:
            raise ValueError("Invoice not found")
        orm.status = invoice.status.value
        orm.payment_method = invoice.payment_method
        orm.paid_at = invoice.paid_at
        self.session.flush()
        return invoice

    def _to_domain(self, orm: models.Invoice) -> Invoice:
        return Invoice(
            id=orm.id,
            tenant_id=orm.tenant_id,
            client_id=orm.client_id,
            status=InvoiceStatus(orm.status),
            issue_date=orm.issue_date,
            due_date=orm.due_date,
            subtotal=Money(amount=orm.subtotal_amount, currency=orm.subtotal_currency),
            tax=Money(amount=orm.tax_amount, currency=orm.tax_currency),
            total=Money(amount=orm.total_amount, currency=orm.total_currency),
            line_items=[
                InvoiceLineItem(
                    id=li.id,
                    description=li.description,
                    quantity=li.quantity,
                    rate=li.rate,
                    amount=Money(amount=li.amount_amount, currency=li.amount_currency),
                    time_entry_ids=[
                        uuid.UUID(te_id) if isinstance(te_id, str) else te_id
                        for te_id in li.time_entry_ids
                    ],
                )
                for li in orm.line_items
            ],
            notes=orm.notes,
            idempotency_key=orm.idempotency_key,
            payment_method=orm.payment_method,
            paid_at=orm.paid_at,
            created_at=orm.created_at,
            updated_at=orm.updated_at,
        )
