# -----------------------------------------------------------------------------
# Copyright (c) 2025 Salvatore D'Angelo, Code4Projects
# Licensed under the MIT License. See LICENSE.md for details.
# -----------------------------------------------------------------------------
from enum import Enum


class ETFCurrency(str, Enum):
    """
    Enumeration for ETF currency types
    """

    USD = "USD"
    EUR = "EUR"

    @classmethod
    def get_all_values(cls) -> list[str]:
        """Get all currency values"""
        return [member.value for member in cls]


# Made with Bob
