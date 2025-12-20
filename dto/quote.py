# -----------------------------------------------------------------------------
# Copyright (c) 2025 Salvatore D'Angelo, Code4Projects
# Licensed under the MIT License. See LICENSE.md for details.
# -----------------------------------------------------------------------------
from pydantic import BaseModel, Field, ConfigDict


class Quote(BaseModel):
    """DTO for ETF quote data"""

    ticker: str = Field(..., min_length=1, max_length=10, alias="Ticker")
    date: str = Field(..., min_length=1, max_length=20, alias="Date")
    open: float | None = Field(None, ge=0, alias="Open")
    high: float | None = Field(None, ge=0, alias="High")
    low: float | None = Field(None, ge=0, alias="Low")
    close: float = Field(..., ge=0, alias="Close")
    volume: int | None = Field(None, ge=0, alias="Volume")

    model_config = ConfigDict(from_attributes=True, populate_by_name=True)
