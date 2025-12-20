# -----------------------------------------------------------------------------
# Copyright (c) 2025 Salvatore D'Angelo, Code4Projects
# Licensed under the MIT License. See LICENSE.md for details.
# -----------------------------------------------------------------------------
from enum import Enum


class ETFAssetType(str, Enum):
    """ETF Asset Type enumeration"""

    EQUITY = "EQUITY"
    BOND = "BOND"
    PRECIOUS_METALS = "PRECIOUS_METALS"
    COMMODITIES = "COMMODITIES"
    CRYPTOCURRENCY = "CRYPTOCURRENCY"
    REAL_ESTATE = "REAL_ESTATE"
    MONEY_MARKET = "MONEY_MARKET"
