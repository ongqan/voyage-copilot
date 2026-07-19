from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
import os


@dataclass(frozen=True)
class Settings:
    app_env: str
    database_path: Path
    cors_origins: tuple[str, ...]

    @property
    def demo_auth_enabled(self) -> bool:
        return self.app_env in {"development", "test"}


def load_settings(database_path: str | Path | None = None) -> Settings:
    resolved_path = Path(
        database_path
        or os.getenv("APP_DATABASE_PATH", ".data/voyage-copilot.sqlite3")
    )
    origins = tuple(
        origin.strip()
        for origin in os.getenv(
            "APP_CORS_ORIGINS",
            "http://localhost:3000,http://127.0.0.1:3000",
        ).split(",")
        if origin.strip()
    )
    return Settings(
        app_env=os.getenv("APP_ENV", "development"),
        database_path=resolved_path,
        cors_origins=origins,
    )
