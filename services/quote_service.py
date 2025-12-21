# -----------------------------------------------------------------------------
# Copyright (c) 2025 Salvatore D'Angelo, Code4Projects
# Licensed under the MIT License. See LICENSE.md for details.
# -----------------------------------------------------------------------------
from typing import Any
from datetime import datetime
from pandas.core.frame import DataFrame
from models import QuoteDAO
from core.database import DatabaseManager
from core.log import LoggerManager
from dto import Quote, QuotePeriod
import datetime as dt
import yfinance as yf
import math


class QuoteService:
    """Service layer for Quote management and download"""

    def __init__(self, db_manager: DatabaseManager) -> None:
        """
        Initialize QuoteService with a DatabaseManager instance

        Args:
            db_manager: DatabaseManager instance for session handling
        """
        self.db_manager = db_manager
        self.logger = LoggerManager.get_logger(name=self.__class__.__name__)
        self.start_date = dt.datetime(year=1970, month=1, day=1)
        self.end_date = dt.datetime.now() - dt.timedelta(days=1)
        self.logger.info("QuoteService initialized")

    def get_quotes(self, ticker: str, period: QuotePeriod = QuotePeriod.ONE_YEAR) -> list[Quote]:
        """
        Retrieve quotes for an ETF within a specific period

        Args:
            ticker: ETF ticker symbol
            period: Time period (QuotePeriod enum)

        Returns:
            List of Quote DTOs
        """
        self.logger.info(f"Fetching quotes for ETF {ticker}, period: {period.value}")

        # Get start date from enum
        start_date: datetime = period.get_start_date()

        self.logger.debug(f"Calculated start date for period {period.value}: {start_date.strftime('%Y-%m-%d')}")

        # Query quotes from database
        quote_daos: list[QuoteDAO] = (
            QuoteDAO.query.filter(QuoteDAO.Ticker == ticker, QuoteDAO.Date > start_date.strftime("%Y-%m-%d"))
            .order_by(QuoteDAO.Date)
            .all()
        )

        self.logger.info(f"Retrieved {len(quote_daos)} quotes for ETF {ticker}")

        # Convert DAOs to DTOs using Pydantic's model_validate
        return [Quote.model_validate(dao) for dao in quote_daos]

    def update_quotes(self, ticker: str) -> None:
        """
        Download and update quotes for a specific ETF ticker directly in the database

        Args:
            ticker: ETF ticker symbol

        Raises:
            ValueError: If no historical data is available for the ticker
            Exception: For any other errors during download or database operations
        """
        self.logger.info(f"Updating quotes for ETF: {ticker}")

        # Determine date range for download
        start_date: datetime | None = self._get_download_start_date(ticker)
        if start_date is None:
            return  # Already up to date

        # Download quotes from yfinance
        self.logger.debug(f"Downloading quotes from {start_date.date()} to {self.end_date.date()}")
        raw_df: DataFrame | None = yf.download(
            tickers=ticker,
            start=start_date,
            end=self.end_date,
            progress=False,
            auto_adjust=False,
        )

        # No data available
        if raw_df is None or (hasattr(raw_df, "empty") and raw_df.empty):
            last_quote: QuoteDAO | None = (
                QuoteDAO.query.filter(QuoteDAO.Ticker == ticker).order_by(QuoteDAO.Date.desc()).first()
            )
            if last_quote:
                self.logger.info("  No new quotes available")
                return
            else:
                raise ValueError(f"No historical data available for ticker {ticker}")

        # Process and save quotes to database using bulk insert
        self._bulk_insert_quotes(ticker, raw_df)
        self.logger.info(f"  Added {len(raw_df)} new quotes")

    def _get_download_start_date(self, ticker: str) -> datetime | None:
        """
        Determine the start date for downloading quotes

        Args:
            ticker: ETF ticker symbol

        Returns:
            Start date for download, or None if already up to date
        """
        last_quote: QuoteDAO | None = (
            QuoteDAO.query.filter(QuoteDAO.Ticker == ticker).order_by(QuoteDAO.Date.desc()).first()
        )

        if last_quote:
            last_quote_date: datetime = dt.datetime.strptime(last_quote.Date, "%Y-%m-%d")
            start_date: datetime = last_quote_date + dt.timedelta(days=1)

            # Already up to date
            if start_date > self.end_date:
                self.logger.info(f"  Already up to date (last quote: {last_quote_date.date()})")
                return None

            return start_date
        else:
            # No quotes in database, download all historical data
            return self.start_date

    def _bulk_insert_quotes(self, ticker: str, raw_df: DataFrame) -> None:
        """
        Bulk insert quotes into database using pandas to_sql

        Args:
            ticker: ETF ticker symbol
            raw_df: DataFrame with quote data from yfinance
        """
        from core.database import db
        import pandas as pd

        # Reset index to get Date as a column
        df = raw_df.reset_index()

        # Flatten MultiIndex columns if present (yfinance returns MultiIndex for single ticker)
        if isinstance(df.columns, pd.MultiIndex):
            df.columns = df.columns.get_level_values(0)

        # Prepare DataFrame for database insertion
        df["Ticker"] = ticker
        df["Date"] = pd.to_datetime(df["Date"]).dt.strftime("%Y-%m-%d")

        # Handle NaN values using pandas methods (more efficient than apply)
        df["Open"] = df["Open"].replace([float("inf"), float("-inf")], None).round(2)
        df["High"] = df["High"].replace([float("inf"), float("-inf")], None).round(2)
        df["Low"] = df["Low"].replace([float("inf"), float("-inf")], None).round(2)
        df["Close"] = df["Close"].replace([float("inf"), float("-inf")], None).round(2)
        df["Adj_Close"] = df["Adj Close"].replace([float("inf"), float("-inf")], None).round(2)
        df["Volume"] = df["Volume"].replace([float("inf"), float("-inf")], None).astype("Int64")

        # Select only the columns we need
        quotes_df = df[["Ticker", "Date", "Open", "High", "Low", "Close", "Adj_Close", "Volume"]].copy()

        # Bulk insert using pandas to_sql
        with self.db_manager.get_session():
            quotes_df.to_sql(name="quotes", con=db.engine, if_exists="append", index=False)

    def _safe_float(self, value: Any) -> float | None:
        """
        Safely convert a value to float, handling NaN and errors

        Args:
            value: Value to convert

        Returns:
            Rounded float value or None if conversion fails or value is NaN
        """
        try:
            float_val = float(value)
            return round(float_val, 2) if not math.isnan(float_val) else None
        except (ValueError, TypeError):
            return None

    def _safe_int(self, value: Any) -> int | None:
        """
        Safely convert a value to int, handling errors

        Args:
            value: Value to convert

        Returns:
            Integer value or None if conversion fails
        """
        try:
            return int(value)
        except (ValueError, TypeError):
            return None
