# -----------------------------------------------------------------------------
# Copyright (c) 2025 Salvatore D'Angelo, Code4Projects
# Licensed under the MIT License. See LICENSE.md for details.
# -----------------------------------------------------------------------------
from pydantic import BaseModel, Field


class ErrorResponse(BaseModel):
    """DTO for error API responses"""

    error: str = Field(..., description="Error message")

    class Config:
        json_schema_extra = {"example": {"error": "No quotes available"}}
