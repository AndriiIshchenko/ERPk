import re
import uuid
from datetime import datetime

from pydantic import BaseModel, EmailStr, field_validator


def _validate_name(v: str) -> str:
    """Strip whitespace and enforce a non-empty name under 255 characters."""
    v = v.strip()
    if not v:
        raise ValueError("Name cannot be empty")
    if len(v) > 255:
        raise ValueError("Name cannot exceed 255 characters")
    return v


def _validate_phone(v: str | None) -> str | None:
    """Normalise and validate a phone number; returns None for blank input."""
    if v is None:
        return v
    v = v.strip()
    if not v:
        return None
    if not re.match(r"^[\+\d\s\-\(\)]{7,20}$", v):
        raise ValueError("Phone must be 7–20 characters: digits, spaces, +, -, ( )")
    return v


class CustomerCreate(BaseModel):
    """Payload for creating a new customer."""

    name: str
    email: EmailStr
    phone: str | None = None

    @field_validator("name")
    @classmethod
    def validate_name(cls, v: str) -> str:
        """Delegate to the shared name validator."""
        return _validate_name(v)

    @field_validator("phone")
    @classmethod
    def validate_phone(cls, v: str | None) -> str | None:
        """Delegate to the shared phone validator."""
        return _validate_phone(v)


class CustomerUpdate(BaseModel):
    """Payload for partially updating an existing customer; all fields optional."""

    name: str | None = None
    email: EmailStr | None = None
    phone: str | None = None

    @field_validator("name")
    @classmethod
    def validate_name(cls, v: str | None) -> str | None:
        """Validate name only when a new value is provided."""
        return _validate_name(v) if v is not None else v

    @field_validator("phone")
    @classmethod
    def validate_phone(cls, v: str | None) -> str | None:
        """Delegate to the shared phone validator."""
        return _validate_phone(v)


class CustomerRead(BaseModel):
    """Response schema for a customer record."""

    id: uuid.UUID
    name: str
    email: EmailStr
    phone: str | None
    created_at: datetime

    model_config = {"from_attributes": True}
