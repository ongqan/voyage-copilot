from __future__ import annotations

from datetime import datetime
from typing import Literal, Optional

from pydantic import BaseModel, ConfigDict, Field, field_validator


class ApiModel(BaseModel):
    model_config = ConfigDict(extra="forbid")


class MeResponse(ApiModel):
    tenant_id: str
    user_id: str
    display_name: str
    membership_level: str
    roles: list[str]


class TripCreate(ApiModel):
    flight_number: str = Field(min_length=3, max_length=12)
    departure_airport: str = Field(min_length=3, max_length=3)
    arrival_airport: str = Field(min_length=3, max_length=3)
    departure_at: datetime
    arrival_at: datetime
    departure_terminal: Optional[str] = Field(default=None, max_length=12)
    arrival_terminal: Optional[str] = Field(default=None, max_length=12)
    party_adults: int = Field(default=1, ge=1, le=20)
    party_children: int = Field(default=0, ge=0, le=20)

    @field_validator("flight_number", "departure_airport", "arrival_airport")
    @classmethod
    def normalize_code(cls, value: str) -> str:
        return value.strip().upper()

    @field_validator("departure_at", "arrival_at")
    @classmethod
    def require_timezone(cls, value: datetime) -> datetime:
        if value.utcoffset() is None:
            raise ValueError("datetime must include a timezone offset")
        return value

    @field_validator("arrival_at")
    @classmethod
    def validate_arrival(cls, value: datetime, info):
        departure_at = info.data.get("departure_at")
        if departure_at and value <= departure_at:
            raise ValueError("arrival_at must be after departure_at")
        return value


class TripResponse(ApiModel):
    id: str
    tenant_id: str
    user_id: str
    status: Literal["DRAFT", "CONFIRMED"]
    flight_number: str
    departure_airport: str
    arrival_airport: str
    departure_at: datetime
    arrival_at: datetime
    departure_terminal: Optional[str]
    arrival_terminal: Optional[str]
    party_adults: int
    party_children: int
    version: int
    created_at: datetime
    confirmed_at: Optional[datetime]


class TripListResponse(ApiModel):
    items: list[TripResponse]
    total: int


class ErrorBody(ApiModel):
    code: str
    message: str
    retryable: bool = False
    action: Optional[str] = None


class ErrorResponse(ApiModel):
    error: ErrorBody
    trace_id: str
