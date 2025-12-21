# -----------------------------------------------------------------------------
# Copyright (c) 2025 Salvatore D'Angelo, Code4Projects
# Licensed under the MIT License. See LICENSE.md for details.
# -----------------------------------------------------------------------------
from pydantic import BaseModel, Field
from dto.etf_asset_type import ETFAssetType


class ETFScreenerFilters(BaseModel):
    """
    ETF Screener Filters DTO
    Used to filter ETFs based on various criteria
    """

    # Asset type filter
    asset_type: ETFAssetType | None = Field(default=None, description="Asset type filter")

    # Dividend type filter
    dividend_type: str | None = Field(default=None, description="Dividend type (Distribuzione/Accumulazione)")

    # Currency filter
    currency: str | None = Field(default=None, description="Currency filter")

    # Replication type filter
    replication: str | None = Field(default=None, description="Replication type filter")

    # Index filter
    index_ticker: str | None = Field(default=None, description="Reference index ticker filter")

    # Fund size filter (in millions)
    min_capital: float | None = Field(default=None, ge=0, description="Minimum fund size in millions")

    # Age filter (in years)
    min_age_years: int | None = Field(default=None, ge=0, description="Minimum age in years")

    class Config:
        str_strip_whitespace: bool = True
        from_attributes: bool = True
