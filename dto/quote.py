# -----------------------------------------------------------------------------
# Copyright (c) 2025 Salvatore D'Angelo, Code4Projects
# Licensed under the MIT License. See LICENSE.md for details.
# -----------------------------------------------------------------------------
from pydantic import BaseModel, Field


class Quote(BaseModel):
    """DTO for ETF quote data"""

    ticker: str = Field(..., min_length=1, max_length=10)
    date: str = Field(..., min_length=1, max_length=20)
    open: float | None = Field(None, ge=0)
    high: float | None = Field(None, ge=0)
    low: float | None = Field(None, ge=0)
    close: float = Field(..., ge=0)
    volume: int | None = Field(None, ge=0)

    class Config:
        from_attributes = True
