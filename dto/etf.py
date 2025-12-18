# -----------------------------------------------------------------------------
# Copyright (c) 2025 Salvatore D'Angelo, Code4Projects
# Licensed under the MIT License. See LICENSE.md for details.
# -----------------------------------------------------------------------------
from pydantic import BaseModel, Field, field_validator
from typing import Optional


class ETF(BaseModel):
    """
    ETF Data Transfer Object
    Used across all layers for data validation and transfer
    """

    ticker: str = Field(..., min_length=1, max_length=10, description="ETF ticker symbol")
    name: str = Field(..., min_length=1, max_length=50, description="ETF name")
    isin: Optional[str] = Field(None, max_length=15, description="ISIN code")
    launchDate: Optional[str] = Field(None, max_length=20, description="Launch date")
    capital: Optional[float] = Field(None, ge=0, description="Capital in millions")
    replication: Optional[str] = Field(None, max_length=30, description="Replication type")
    volatility: Optional[float] = Field(None, ge=0, le=100, description="Volatility percentage")
    currency: Optional[str] = Field(None, max_length=10, description="Currency")
    dividend: Optional[str] = Field(None, max_length=20, description="Dividend type")
    dividendFrequency: Optional[int] = Field(None, ge=1, le=12, description="Dividend frequency")
    yeld: Optional[float] = Field(None, ge=0, le=100, description="Yield percentage")

    @field_validator("ticker")
    @classmethod
    def ticker_must_be_uppercase(cls, v: str) -> str:
        """Ensure ticker is uppercase"""
        return v.upper() if v else v

    @field_validator("name")
    @classmethod
    def name_must_not_be_empty(cls, v: str) -> str:
        """Ensure name is not empty after stripping"""
        if not v or not v.strip():
            raise ValueError("Name cannot be empty")
        return v.strip()

    class Config:
        str_strip_whitespace = True
        from_attributes = True  # Allows creation from ORM models


# Made with Bob
