import re
from pydantic import BaseModel, Field, field_validator


class WebhookPayload(BaseModel):
    # Unique message identifier
    message_id: str = Field(..., min_length=1)

    # "from" and "to" are reserved words in Python,
    # so we map them using aliases
    from_msisdn: str = Field(..., alias="from")
    to_msisdn: str = Field(..., alias="to")

    # Timestamp in ISO-8601 UTC format with Z suffix
    ts: str

    # Optional message text
    text: str | None = Field(default=None, max_length=4096)

    # Validate phone numbers (E.164-like format)
    @field_validator("from_msisdn", "to_msisdn")
    @classmethod
    def validate_e164(cls, value: str) -> str:
        if not re.fullmatch(r"\+\d+", value):
            raise ValueError("Must be in E.164 format (e.g. +123456789)")
        return value

    # Validate timestamp format strictly
    @field_validator("ts")
    @classmethod
    def validate_timestamp(cls, value: str) -> str:
        iso_utc_pattern = r"\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}Z"
        if not re.fullmatch(iso_utc_pattern, value):
            raise ValueError("ts must be ISO-8601 UTC format (e.g. 2025-01-15T10:00:00Z)")
        return value
