# -----------------------------------------------------------------------------
# Copyright (c) 2025 Salvatore D'Angelo, Code4Projects
# Licensed under the MIT License. See LICENSE.md for details.
# -----------------------------------------------------------------------------
from enum import Enum
import datetime as dt
from dateutil.relativedelta import relativedelta


class QuotePeriod(str, Enum):
    """Enum for quote time periods"""

    FIVE_DAYS = "5D"
    ONE_MONTH = "1M"
    THREE_MONTHS = "3M"
    SIX_MONTHS = "6M"
    ONE_YEAR = "1Y"
    YEAR_TO_DATE = "YTD"
    FIVE_YEARS = "5Y"
    MAX = "Max"

    def get_start_date(self) -> dt.datetime:
        """
        Calculate the start date for this period

        Returns:
            datetime: Start date for the period

        Raises:
            ValueError: If period is invalid
        """
        now = dt.datetime.now()

        period_map = {
            QuotePeriod.MAX: dt.datetime(1970, 1, 1),
            QuotePeriod.FIVE_YEARS: now - relativedelta(years=5),
            QuotePeriod.ONE_YEAR: now - relativedelta(years=1),
            QuotePeriod.YEAR_TO_DATE: dt.datetime(now.year, 1, 1),
            QuotePeriod.SIX_MONTHS: now - relativedelta(months=6),
            QuotePeriod.THREE_MONTHS: now - relativedelta(months=3),
            QuotePeriod.ONE_MONTH: now - relativedelta(months=1),
            QuotePeriod.FIVE_DAYS: now - relativedelta(days=5),
        }

        return period_map[self]

    @classmethod
    def from_string(cls, period_str: str) -> "QuotePeriod":
        """
        Convert string to QuotePeriod enum

        Args:
            period_str: Period string (e.g., "1Y", "5D")

        Returns:
            QuotePeriod enum value

        Raises:
            ValueError: If period string is invalid
        """
        try:
            return cls(period_str)
        except ValueError:
            valid_periods = ", ".join([p.value for p in cls])
            raise ValueError(f"Invalid period '{period_str}'. Valid periods are: {valid_periods}")
