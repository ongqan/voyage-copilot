from __future__ import annotations

from contextlib import asynccontextmanager
from pathlib import Path
from uuid import uuid4

from fastapi import Body, Depends, FastAPI, HTTPException, Request, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse

from .auth import AuthContext, get_auth_context
from .config import load_settings
from .database import Database
from .demo_data import ADMIN_SUMMARY, BENEFITS, CONVERSATIONS, RECOMMENDATIONS, TIMELINE
from .schemas import MeResponse, TripCreate, TripListResponse, TripResponse


def create_app(database_path: str | Path | None = None) -> FastAPI:
    settings = load_settings(database_path)
    database = Database(settings.database_path)

    @asynccontextmanager
    async def lifespan(app: FastAPI):
        database.initialize()
        app.state.settings = settings
        app.state.db = database
        yield

    app = FastAPI(
        title="Voyage Copilot API",
        version="0.1.0",
        description="Sprint 0 vertical slice for trip creation and confirmation.",
        lifespan=lifespan,
    )
    app.add_middleware(
        CORSMiddleware,
        allow_origins=list(settings.cors_origins),
        allow_credentials=False,
        allow_methods=["GET", "POST", "OPTIONS"],
        allow_headers=["Content-Type", "X-Demo-Tenant-ID", "X-Demo-User-ID", "X-Trace-ID"],
        expose_headers=["X-Trace-ID"],
    )

    @app.middleware("http")
    async def trace_middleware(request: Request, call_next):
        trace_id = request.headers.get("X-Trace-ID") or f"trace_{uuid4().hex}"
        request.state.trace_id = trace_id
        response = await call_next(request)
        response.headers["X-Trace-ID"] = trace_id
        return response

    @app.exception_handler(HTTPException)
    async def http_exception_handler(request: Request, exc: HTTPException):
        detail = exc.detail if isinstance(exc.detail, dict) else {}
        return JSONResponse(
            status_code=exc.status_code,
            content={
                "error": {
                    "code": detail.get("code", "HTTP_ERROR"),
                    "message": detail.get("message", "请求失败。"),
                    "retryable": detail.get("retryable", False),
                    "action": detail.get("action"),
                },
                "trace_id": getattr(request.state, "trace_id", "trace_unavailable"),
            },
        )

    @app.exception_handler(RequestValidationError)
    async def validation_exception_handler(request: Request, exc: RequestValidationError):
        fields = [".".join(str(part) for part in error["loc"][1:]) for error in exc.errors()]
        return JSONResponse(
            status_code=status.HTTP_422_UNPROCESSABLE_CONTENT,
            content={
                "error": {
                    "code": "VALIDATION_ERROR",
                    "message": "请求字段校验失败。",
                    "retryable": False,
                    "action": "correct_input",
                    "details": {"fields": fields},
                },
                "trace_id": getattr(request.state, "trace_id", "trace_unavailable"),
            },
        )

    @app.get("/api/v1/health", tags=["system"])
    async def health() -> dict[str, str]:
        return {"status": "ok", "service": "voyage-copilot-api", "version": "0.1.0"}

    @app.get("/api/v1/me", response_model=MeResponse, tags=["identity"])
    async def me(request: Request, auth: AuthContext = Depends(get_auth_context)):
        user = request.app.state.db.get_user(auth.tenant_id, auth.user_id)
        return MeResponse(
            tenant_id=auth.tenant_id,
            user_id=auth.user_id,
            display_name=user["display_name"],
            membership_level=user["membership_level"],
            roles=list(auth.roles),
        )

    @app.post(
        "/api/v1/trips",
        response_model=TripResponse,
        status_code=status.HTTP_201_CREATED,
        tags=["trips"],
    )
    async def create_trip(
        payload: TripCreate,
        request: Request,
        auth: AuthContext = Depends(get_auth_context),
    ):
        return request.app.state.db.create_trip(
            auth.tenant_id, auth.user_id, payload, request.state.trace_id
        )

    @app.get("/api/v1/trips", response_model=TripListResponse, tags=["trips"])
    async def list_trips(request: Request, auth: AuthContext = Depends(get_auth_context)):
        items = request.app.state.db.list_trips(auth.tenant_id, auth.user_id)
        return TripListResponse(items=items, total=len(items))

    @app.get("/api/v1/trips/{trip_id}", response_model=TripResponse, tags=["trips"])
    async def get_trip(
        trip_id: str, request: Request, auth: AuthContext = Depends(get_auth_context)
    ):
        trip = request.app.state.db.get_trip(auth.tenant_id, auth.user_id, trip_id)
        if trip is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail={"code": "TRIP_NOT_FOUND", "message": "未找到该行程。"},
            )
        return trip

    @app.get("/api/v1/me/entitlements", tags=["benefits"])
    async def list_entitlements(auth: AuthContext = Depends(get_auth_context)):
        return {"items": BENEFITS, "total": len(BENEFITS), "evaluated_for": auth.user_id}

    @app.post("/api/v1/trips/{trip_id}/recommendation-runs", tags=["recommendations"])
    async def create_recommendation_run(
        trip_id: str, request: Request, auth: AuthContext = Depends(get_auth_context)
    ):
        trip = request.app.state.db.get_trip(auth.tenant_id, auth.user_id, trip_id)
        if trip is None:
            raise HTTPException(status_code=404, detail={"code": "TRIP_NOT_FOUND", "message": "未找到该行程。"})
        if trip["status"] != "CONFIRMED":
            raise HTTPException(status_code=409, detail={"code": "TRIP_NOT_CONFIRMED", "message": "请先确认行程。"})
        return {"run_id": "recommendation_demo_001", "strategy_version": "demo-weighted-v1", "items": RECOMMENDATIONS, "generated_at": "2026-07-19T12:01:00+08:00"}

    @app.post("/api/v1/trips/{trip_id}/timeline-plans", tags=["timeline"])
    async def create_timeline_plan(
        trip_id: str, request: Request, auth: AuthContext = Depends(get_auth_context)
    ):
        trip = request.app.state.db.get_trip(auth.tenant_id, auth.user_id, trip_id)
        if trip is None:
            raise HTTPException(status_code=404, detail={"code": "TRIP_NOT_FOUND", "message": "未找到该行程。"})
        return {"plan_id": "timeline_demo_001", "items": TIMELINE, "safety_buffer_minutes": 32, "conflicts": []}

    @app.post("/api/v1/order-quotes", tags=["orders"])
    async def create_order_quote(
        payload: dict = Body(default={}), auth: AuthContext = Depends(get_auth_context)
    ):
        service_id = payload.get("service_id", "service-lounge-001")
        return {"quote_id": "quote_demo_001", "user_id": auth.user_id, "service_id": service_id, "points": 1, "amount_minor": 0, "currency": "CNY", "quote_hash": "demo_quote_hash_001", "expires_at": "2026-07-19T12:06:00+08:00", "rule_versions": ["demo-lounge-017@3"]}

    @app.post("/api/v1/orders/{order_id}/confirmation-tokens", tags=["orders"])
    async def create_confirmation_token(
        order_id: str, auth: AuthContext = Depends(get_auth_context)
    ):
        return {"order_id": order_id, "action": "confirm", "confirmation_token": "demo-confirmation-token", "expires_in_seconds": 300, "subject": auth.user_id}

    @app.post("/api/v1/orders/{order_id}/confirm", tags=["orders"])
    async def confirm_order(
        order_id: str,
        payload: dict = Body(default={}),
        auth: AuthContext = Depends(get_auth_context),
    ):
        if payload.get("confirmation_token") != "demo-confirmation-token":
            raise HTTPException(status_code=403, detail={"code": "CONFIRMATION_REQUIRED", "message": "需要有效的二次确认令牌。"})
        return {"id": order_id, "user_id": auth.user_id, "status": "CONFIRMED", "simulation": True, "voucher": "DEMO-QR-008"}

    @app.get("/api/v1/disruptions/demo-event-001", tags=["disruptions"])
    async def get_disruption(auth: AuthContext = Depends(get_auth_context)):
        return {"id": "demo-event-001", "type": "terminal_change", "severity": "important", "flight_number": "MU5105", "old_terminal": "T2", "new_terminal": "T1", "affected_order_ids": ["VC-DEMO-260810-008"], "resolution_options": ["rebook", "keep", "cancel"], "simulation": True}

    @app.get("/api/v1/agent/conversations", tags=["support"])
    async def list_conversations(auth: AuthContext = Depends(get_auth_context)):
        return {"items": CONVERSATIONS, "total": len(CONVERSATIONS), "tenant_id": auth.tenant_id}

    @app.get("/api/v1/admin/dashboard", tags=["admin"])
    async def admin_dashboard(auth: AuthContext = Depends(get_auth_context)):
        return {**ADMIN_SUMMARY, "tenant_id": auth.tenant_id, "simulation": True}

    @app.post(
        "/api/v1/trips/{trip_id}/confirm",
        response_model=TripResponse,
        tags=["trips"],
    )
    async def confirm_trip(
        trip_id: str, request: Request, auth: AuthContext = Depends(get_auth_context)
    ):
        trip = request.app.state.db.confirm_trip(
            auth.tenant_id, auth.user_id, trip_id, request.state.trace_id
        )
        if trip is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail={"code": "TRIP_NOT_FOUND", "message": "未找到该行程。"},
            )
        return trip

    return app


app = create_app()
