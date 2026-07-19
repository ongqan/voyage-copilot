from __future__ import annotations

from dataclasses import dataclass
from typing import Optional

from fastapi import Header, HTTPException, Request, status


@dataclass(frozen=True)
class AuthContext:
    tenant_id: str
    user_id: str
    roles: tuple[str, ...]


async def get_auth_context(
    request: Request,
    x_demo_tenant_id: Optional[str] = Header(default=None),
    x_demo_user_id: Optional[str] = Header(default=None),
) -> AuthContext:
    settings = request.app.state.settings
    if not settings.demo_auth_enabled:
        raise HTTPException(
            status_code=status.HTTP_501_NOT_IMPLEMENTED,
            detail={"code": "AUTH_PROVIDER_NOT_CONFIGURED", "message": "认证服务尚未配置。"},
        )

    if not x_demo_tenant_id or not x_demo_user_id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail={
                "code": "UNAUTHENTICATED",
                "message": "开发环境需要Demo身份请求头。",
            },
        )

    user = request.app.state.db.get_user(x_demo_tenant_id, x_demo_user_id)
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail={"code": "FORBIDDEN", "message": "Demo用户不属于当前租户。"},
        )

    return AuthContext(
        tenant_id=x_demo_tenant_id,
        user_id=x_demo_user_id,
        roles=tuple(user["roles"].split(",")),
    )
