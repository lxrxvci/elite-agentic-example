"""Time entry domain service."""

from __future__ import annotations

import uuid
from datetime import UTC, datetime

from domain.entities import Project, Tenant, TimeEntry, TimeEntryStatus


def create_time_entry(
    tenant: Tenant,
    project: Project,
    description: str,
    duration_minutes: int | None,
    started_at: datetime | None,
    ended_at: datetime | None,
) -> TimeEntry:
    """Create a time entry, computing duration and rounded minutes."""
    if duration_minutes is None:
        if started_at is None or ended_at is None:
            raise ValueError("Either duration_minutes or both timestamps are required")
        duration_minutes = max(0, int((ended_at - started_at).total_seconds() // 60))

    rounded_minutes = project.round_minutes(duration_minutes)

    return TimeEntry(
        id=uuid.uuid4(),
        tenant_id=tenant.id,
        client_id=project.client_id,
        project_id=project.id,
        description=description,
        duration_minutes=duration_minutes,
        rounded_minutes=rounded_minutes,
        status=TimeEntryStatus.UNBILLED,
        started_at=started_at,
        ended_at=ended_at,
        created_at=datetime.now(UTC),
        updated_at=datetime.now(UTC),
    )
