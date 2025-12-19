# -----------------------------------------------------------------------------
# Copyright (c) 2025 Salvatore D'Angelo, Code4Projects
# Licensed under the MIT License. See LICENSE.md for details.
# -----------------------------------------------------------------------------
from models import EtfDAO, QuoteDAO
from core.database import DatabaseManager
from dto import ETF, Quote
import datetime as dt
from dateutil.relativedelta import relativedelta


class EtfService:
    """Service layer for ETF management"""

    def __init__(self, db_manager: DatabaseManager):
        """
        Initialize EtfService with a DatabaseManager instance

        Args:
            db_manager: DatabaseManager instance for session handling
        """
        self.db_manager = db_manager

    def get_all_etfs(self):
        """Retrieve all ETFs from database"""
        return EtfDAO.query.all()

    def get_etf_by_ticker(self, ticker):
        """Retrieve a specific ETF by ticker"""
        return EtfDAO.query.get(ticker)

    def create_etf(self, etf_dto: ETF):
        """
        Create a new ETF

        Args:
            etf_dto: ETF DTO with validated data

        Returns:
            EtfDAO: Created ETF model

        Raises:
            SQLAlchemyError: On database errors
        """
        with self.db_manager.get_session() as session:
            etf = EtfDAO()
            etf.ticker = etf_dto.ticker
            etf.name = etf_dto.name
            etf.isin = etf_dto.isin
            etf.launchDate = etf_dto.launchDate
            etf.capital = etf_dto.capital
            etf.replication = etf_dto.replication
            etf.volatility = etf_dto.volatility
            etf.currency = etf_dto.currency
            etf.dividendType = etf_dto.dividendType
            etf.dividendFrequency = etf_dto.dividendFrequency
            etf.yeld = etf_dto.yeld
            session.add(etf)
            # Commit happens automatically via context manager
        return etf

    def update_etf(self, ticker, etf_dto: ETF):
        """
        Update an existing ETF

        Args:
            ticker: Ticker of the ETF to update
            etf_dto: ETF DTO with new validated data

        Returns:
            EtfDAO: Updated ETF model

        Raises:
            ValueError: If ETF not found
            SQLAlchemyError: On database errors
        """
        with self.db_manager.get_session():
            etf = EtfDAO.query.get(ticker)
            if not etf:
                raise ValueError(f"ETF {ticker} not found")

            # Update all fields from DTO
            etf.name = etf_dto.name
            etf.isin = etf_dto.isin
            etf.launchDate = etf_dto.launchDate
            etf.capital = etf_dto.capital
            etf.replication = etf_dto.replication
            etf.volatility = etf_dto.volatility
            etf.currency = etf_dto.currency
            etf.dividendType = etf_dto.dividendType
            etf.dividendFrequency = etf_dto.dividendFrequency
            etf.yeld = etf_dto.yeld
            # Commit happens automatically via context manager
        return etf

    def delete_etf(self, ticker):
        """
        Delete an ETF

        Args:
            ticker: Ticker of the ETF to delete

        Returns:
            bool: True if deleted successfully

        Raises:
            ValueError: If ETF not found
            SQLAlchemyError: On database errors
        """
        with self.db_manager.get_session() as session:
            etf = EtfDAO.query.get(ticker)
            if not etf:
                raise ValueError(f"ETF {ticker} not found")

            session.delete(etf)
            # Commit happens automatically via context manager
        return True

    def etf_exists(self, ticker):
        """Check if an ETF exists"""
        return EtfDAO.query.get(ticker) is not None

    def get_quotes(self, ticker, period="1Y"):
        """
        Retrieve quotes for an ETF within a specific period

        Args:
            ticker: ETF ticker symbol
            period: Time period (5D, 1M, 3M, 6M, 1Y, YTD, 5Y, Max)

        Returns:
            list: List of QuoteDTO objects or empty list if none found
        """
        # Calculate start date based on period
        period_map = {
            "Max": dt.datetime(1970, 1, 1),
            "5Y": dt.datetime.now() - relativedelta(years=5),
            "1Y": dt.datetime.now() - relativedelta(years=1),
            "YTD": dt.datetime(dt.datetime.now().year, 1, 1),
            "6M": dt.datetime.now() - relativedelta(months=6),
            "3M": dt.datetime.now() - relativedelta(months=3),
            "1M": dt.datetime.now() - relativedelta(months=1),
            "5D": dt.datetime.now() - relativedelta(days=5),
        }
        start_date = period_map.get(period, dt.datetime.now() - relativedelta(years=1))

        # Query quotes from database
        quote_daos = (
            QuoteDAO.query.filter(QuoteDAO.Ticker == ticker, QuoteDAO.Date > start_date.strftime("%Y-%m-%d"))
            .order_by(QuoteDAO.Date)
            .all()
        )

        # Convert DAOs to DTOs
        quote_dtos = [
            Quote(
                ticker=q.Ticker,
                date=q.Date,
                open=q.Open,
                high=q.High,
                low=q.Low,
                close=q.Close,
                volume=q.Volume,
            )
            for q in quote_daos
        ]

        return quote_dtos
