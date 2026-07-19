from pathlib import Path

from fastapi.testclient import TestClient

from app.main import create_app


HEADERS = {
    "X-Demo-Tenant-ID": "tenant_demo_01",
    "X-Demo-User-ID": "user_demo_001",
}


def create_client(tmp_path: Path) -> TestClient:
    return TestClient(create_app(tmp_path / "test.sqlite3"))


def valid_trip() -> dict:
    return {
        "flight_number": "mu5105",
        "departure_airport": "sha",
        "arrival_airport": "pek",
        "departure_at": "2026-08-10T14:30:00+08:00",
        "arrival_at": "2026-08-10T16:50:00+08:00",
        "departure_terminal": "T2",
        "arrival_terminal": "T2",
        "party_adults": 1,
        "party_children": 0,
    }


def test_health_does_not_require_auth(tmp_path: Path):
    with create_client(tmp_path) as client:
        response = client.get("/api/v1/health")
    assert response.status_code == 200
    assert response.json()["status"] == "ok"
    assert response.headers["X-Trace-ID"].startswith("trace_")


def test_local_web_origin_passes_cors_preflight(tmp_path: Path):
    with create_client(tmp_path) as client:
        response = client.options(
            "/api/v1/trips",
            headers={
                "Origin": "http://127.0.0.1:3000",
                "Access-Control-Request-Method": "GET",
                "Access-Control-Request-Headers": (
                    "content-type,x-demo-tenant-id,x-demo-user-id"
                ),
            },
        )
    assert response.status_code == 200
    assert response.headers["Access-Control-Allow-Origin"] == "http://127.0.0.1:3000"


def test_trip_requires_demo_identity(tmp_path: Path):
    with create_client(tmp_path) as client:
        response = client.get("/api/v1/trips")
    assert response.status_code == 401
    assert response.json()["error"]["code"] == "UNAUTHENTICATED"


def test_create_list_and_confirm_trip(tmp_path: Path):
    with create_client(tmp_path) as client:
        created = client.post("/api/v1/trips", headers=HEADERS, json=valid_trip())
        assert created.status_code == 201
        trip = created.json()
        assert trip["flight_number"] == "MU5105"
        assert trip["status"] == "DRAFT"
        assert trip["tenant_id"] == "tenant_demo_01"

        listed = client.get("/api/v1/trips", headers=HEADERS)
        assert listed.status_code == 200
        assert listed.json()["total"] == 1

        confirmed = client.post(
            f"/api/v1/trips/{trip['id']}/confirm", headers=HEADERS
        )
        assert confirmed.status_code == 200
        assert confirmed.json()["status"] == "CONFIRMED"
        assert confirmed.json()["version"] == 2


def test_cross_tenant_access_is_rejected(tmp_path: Path):
    with create_client(tmp_path) as client:
        created = client.post("/api/v1/trips", headers=HEADERS, json=valid_trip()).json()
        response = client.get(
            f"/api/v1/trips/{created['id']}",
            headers={
                "X-Demo-Tenant-ID": "tenant_other",
                "X-Demo-User-ID": "user_demo_001",
            },
        )
    assert response.status_code == 403


def test_arrival_must_be_after_departure(tmp_path: Path):
    payload = valid_trip()
    payload["arrival_at"] = payload["departure_at"]
    with create_client(tmp_path) as client:
        response = client.post("/api/v1/trips", headers=HEADERS, json=payload)
    assert response.status_code == 422
    assert response.json()["error"]["code"] == "VALIDATION_ERROR"


def test_datetime_requires_timezone(tmp_path: Path):
    payload = valid_trip()
    payload["departure_at"] = "2026-08-10T14:30:00"
    with create_client(tmp_path) as client:
        response = client.post("/api/v1/trips", headers=HEADERS, json=payload)
    assert response.status_code == 422
    assert "departure_at" in response.json()["error"]["details"]["fields"]


def test_demo_mvp_endpoints(tmp_path: Path):
    with create_client(tmp_path) as client:
        trip = client.post("/api/v1/trips", headers=HEADERS, json=valid_trip()).json()
        client.post(f"/api/v1/trips/{trip['id']}/confirm", headers=HEADERS)
        assert client.get("/api/v1/me/entitlements", headers=HEADERS).json()["total"] == 3
        recommendations = client.post(
            f"/api/v1/trips/{trip['id']}/recommendation-runs", headers=HEADERS
        )
        assert recommendations.status_code == 200
        assert len(recommendations.json()["items"]) == 3
        assert client.post(
            f"/api/v1/trips/{trip['id']}/timeline-plans", headers=HEADERS
        ).status_code == 200
        quote = client.post("/api/v1/order-quotes", headers=HEADERS, json={}).json()
        assert quote["quote_hash"] == "demo_quote_hash_001"
        rejected = client.post(
            "/api/v1/orders/demo-order-001/confirm", headers=HEADERS, json={}
        )
        assert rejected.status_code == 403
        accepted = client.post(
            "/api/v1/orders/demo-order-001/confirm",
            headers=HEADERS,
            json={"confirmation_token": "demo-confirmation-token"},
        )
        assert accepted.json()["status"] == "CONFIRMED"
        assert client.get("/api/v1/disruptions/demo-event-001", headers=HEADERS).status_code == 200
        assert client.get("/api/v1/agent/conversations", headers=HEADERS).status_code == 200
        assert client.get("/api/v1/admin/dashboard", headers=HEADERS).status_code == 200
