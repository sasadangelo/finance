# -----------------------------------------------------------------------------
# Copyright (c) 2025 Salvatore D'Angelo, Code4Projects
# Licensed under the MIT License. See LICENSE.md for details.
# -----------------------------------------------------------------------------
from pydantic import BaseModel, Field


class QuoteResponse(BaseModel):
    """DTO for quote API response"""

    ticker: str = Field(..., description="ETF ticker symbol")
    labels: list[str] = Field(..., description="List of dates for chart labels")
    data: list[float] = Field(..., description="List of closing prices for chart data")

    class Config:
        json_schema_extra = {
            "example": {
                "ticker": "CW8.MI",
                "labels": ["2024-01-01", "2024-01-02", "2024-01-03"],
                "data": [100.5, 101.2, 102.0],
            }
        }
