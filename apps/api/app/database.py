from __future__ import annotations

from datetime import datetime, timezone
import json
from pathlib import Path
import sqlite3
from threading import RLock
from typing import Any
from uuid import uuid4

from .schemas import TripCreate


class Database:
    def __init__(self, path: Path):
        self.path = path
        self._lock = RLock()

    def connect(self) -> sqlite3.Connection:
        connection = sqlite3.connect(self.path, check_same_thread=False)
        connection.row_factory = sqlite3.Row
        connection.execute("PRAGMA foreign_keys = ON")
        return connection

    def initialize(self) -> None:
        self.path.parent.mkdir(parents=True, exist_ok=True)
        with self._lock, self.connect() as connection:
            connection.executescript(
                """
                CREATE TABLE IF NOT EXISTS tenants (
                    id TEXT PRIMARY KEY,
                    name TEXT NOT NULL
                );
                CREATE TABLE IF NOT EXISTS users (
                    id TEXT NOT NULL,
                    tenant_id TEXT NOT NULL,
                    display_name TEXT NOT NULL,
                    membership_level TEXT NOT NULL,
                    roles TEXT NOT NULL,
                    PRIMARY KEY (id, tenant_id),
                    FOREIGN KEY (tenant_id) REFERENCES tenants(id)
                );
                CREATE TABLE IF NOT EXISTS trips (
                    id TEXT PRIMARY KEY,
                    tenant_id TEXT NOT NULL,
                    user_id TEXT NOT NULL,
                    status TEXT NOT NULL CHECK(status IN ('DRAFT', 'CONFIRMED')),
                    flight_number TEXT NOT NULL,
                    departure_airport TEXT NOT NULL,
                    arrival_airport TEXT NOT NULL,
                    departure_at TEXT NOT NULL,
                    arrival_at TEXT NOT NULL,
                    departure_terminal TEXT,
                    arrival_terminal TEXT,
                    party_adults INTEGER NOT NULL,
                    party_children INTEGER NOT NULL,
                    version INTEGER NOT NULL DEFAULT 1,
                    created_at TEXT NOT NULL,
                    confirmed_at TEXT,
                    FOREIGN KEY (tenant_id) REFERENCES tenants(id),
                    FOREIGN KEY (user_id, tenant_id) REFERENCES users(id, tenant_id)
                );
                CREATE INDEX IF NOT EXISTS idx_trips_owner
                    ON trips(tenant_id, user_id, created_at DESC);
                CREATE TABLE IF NOT EXISTS audit_logs (
                    id TEXT PRIMARY KEY,
                    tenant_id TEXT NOT NULL,
                    user_id TEXT NOT NULL,
                    action TEXT NOT NULL,
                    resource_type TEXT NOT NULL,
                    resource_id TEXT NOT NULL,
                    result TEXT NOT NULL,
                    trace_id TEXT NOT NULL,
                    metadata_json TEXT NOT NULL,
                    created_at TEXT NOT NULL
                );
                """
            )
            connection.execute(
                "INSERT OR IGNORE INTO tenants(id, name) VALUES (?, ?)",
                ("tenant_demo_01", "Voyage Demo Tenant"),
            )
            connection.execute(
                """
                INSERT OR IGNORE INTO users(
                    id, tenant_id, display_name, membership_level, roles
                ) VALUES (?, ?, ?, ?, ?)
                """,
                ("user_demo_001", "tenant_demo_01", "林晨", "臻享计划", "member"),
            )

    def get_user(self, tenant_id: str, user_id: str) -> dict[str, Any] | None:
        with self.connect() as connection:
            row = connection.execute(
                "SELECT * FROM users WHERE tenant_id = ? AND id = ?",
                (tenant_id, user_id),
            ).fetchone()
        return dict(row) if row else None

    def create_trip(
        self, tenant_id: str, user_id: str, payload: TripCreate, trace_id: str
    ) -> dict[str, Any]:
        trip_id = f"trip_{uuid4().hex}"
        created_at = datetime.now(timezone.utc).isoformat()
        values = (
            trip_id,
            tenant_id,
            user_id,
            "DRAFT",
            payload.flight_number,
            payload.departure_airport,
            payload.arrival_airport,
            payload.departure_at.isoformat(),
            payload.arrival_at.isoformat(),
            payload.departure_terminal,
            payload.arrival_terminal,
            payload.party_adults,
            payload.party_children,
            created_at,
        )
        with self._lock, self.connect() as connection:
            connection.execute(
                """
                INSERT INTO trips(
                    id, tenant_id, user_id, status, flight_number,
                    departure_airport, arrival_airport, departure_at, arrival_at,
                    departure_terminal, arrival_terminal, party_adults,
                    party_children, created_at
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """,
                values,
            )
            self._insert_audit(
                connection,
                tenant_id,
                user_id,
                "trip.create",
                trip_id,
                trace_id,
                {"source_type": "manual"},
            )
            row = connection.execute("SELECT * FROM trips WHERE id = ?", (trip_id,)).fetchone()
        return self._trip_from_row(row)

    def list_trips(self, tenant_id: str, user_id: str) -> list[dict[str, Any]]:
        with self.connect() as connection:
            rows = connection.execute(
                """
                SELECT * FROM trips
                WHERE tenant_id = ? AND user_id = ?
                ORDER BY created_at DESC
                """,
                (tenant_id, user_id),
            ).fetchall()
        return [self._trip_from_row(row) for row in rows]

    def get_trip(self, tenant_id: str, user_id: str, trip_id: str) -> dict[str, Any] | None:
        with self.connect() as connection:
            row = connection.execute(
                """
                SELECT * FROM trips
                WHERE tenant_id = ? AND user_id = ? AND id = ?
                """,
                (tenant_id, user_id, trip_id),
            ).fetchone()
        return self._trip_from_row(row) if row else None

    def confirm_trip(
        self, tenant_id: str, user_id: str, trip_id: str, trace_id: str
    ) -> dict[str, Any] | None:
        confirmed_at = datetime.now(timezone.utc).isoformat()
        with self._lock, self.connect() as connection:
            row = connection.execute(
                "SELECT * FROM trips WHERE tenant_id = ? AND user_id = ? AND id = ?",
                (tenant_id, user_id, trip_id),
            ).fetchone()
            if row is None:
                return None
            if row["status"] == "DRAFT":
                connection.execute(
                    """
                    UPDATE trips
                    SET status = 'CONFIRMED', confirmed_at = ?, version = version + 1
                    WHERE id = ?
                    """,
                    (confirmed_at, trip_id),
                )
                self._insert_audit(
                    connection,
                    tenant_id,
                    user_id,
                    "trip.confirm",
                    trip_id,
                    trace_id,
                    {},
                )
            updated = connection.execute("SELECT * FROM trips WHERE id = ?", (trip_id,)).fetchone()
        return self._trip_from_row(updated)

    @staticmethod
    def _insert_audit(
        connection: sqlite3.Connection,
        tenant_id: str,
        user_id: str,
        action: str,
        resource_id: str,
        trace_id: str,
        metadata: dict[str, Any],
    ) -> None:
        connection.execute(
            """
            INSERT INTO audit_logs(
                id, tenant_id, user_id, action, resource_type, resource_id,
                result, trace_id, metadata_json, created_at
            ) VALUES (?, ?, ?, ?, 'trip', ?, 'success', ?, ?, ?)
            """,
            (
                f"audit_{uuid4().hex}",
                tenant_id,
                user_id,
                action,
                resource_id,
                trace_id,
                json.dumps(metadata, ensure_ascii=False),
                datetime.now(timezone.utc).isoformat(),
            ),
        )

    @staticmethod
    def _trip_from_row(row: sqlite3.Row) -> dict[str, Any]:
        result = dict(row)
        for field in ("departure_at", "arrival_at", "created_at", "confirmed_at"):
            if result[field] is not None:
                result[field] = datetime.fromisoformat(result[field])
        return result

