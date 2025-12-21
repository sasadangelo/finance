# -----------------------------------------------------------------------------
# Copyright (c) 2025 Salvatore D'Angelo, Code4Projects
# Licensed under the MIT License. See LICENSE.md for details.
# -----------------------------------------------------------------------------
from pydantic import BaseModel, Field, field_validator


class Index(BaseModel):
    """
    Index Data Transfer Object
    Used across all layers for data validation and transfer
    """

    # Required fields
    ticker: str = Field(..., min_length=1, max_length=10, description="Index ticker symbol")
    name: str = Field(..., min_length=1, max_length=200, description="Index name")

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
