# -----------------------------------------------------------------------------
# Copyright (c) 2025 Salvatore D'Angelo, Code4Projects
# Licensed under the MIT License. See LICENSE.md for details.
# -----------------------------------------------------------------------------
from models import EtfDAO, QuoteDAO
from core.database import DatabaseManager
from core.log import LoggerManager
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
        self.logger = LoggerManager.get_logger(self.__class__.__name__)
        self.logger.info("EtfService initialized")

    def get_all(self) -> list[ETF]:
        """
        Retrieve all ETFs from database

        Returns:
            List of ETF DTOs
        """
        self.logger.debug("Fetching all ETFs from database")
        etf_daos = EtfDAO.query.all()
        self.logger.info(f"Retrieved {len(etf_daos)} ETFs from database")
        return [ETF.model_validate(dao) for dao in etf_daos]

    def get_by_ticker(self, ticker: str) -> ETF | None:
        """
        Retrieve a specific ETF by ticker

        Args:
            ticker: ETF ticker symbol

        Returns:
            ETF DTO if found, None otherwise
        """
        self.logger.debug(f"Fetching ETF with ticker: {ticker}")
        etf_dao = EtfDAO.query.get(ticker)
        if etf_dao:
            self.logger.debug(f"ETF {ticker} found in database")
            return ETF.model_validate(etf_dao)
        else:
            self.logger.debug(f"ETF {ticker} not found in database")
            return None

    def create(self, etf_dto: ETF) -> None:
        """
        Create a new ETF

        Args:
            etf_dto: ETF DTO with validated data

        Raises:
            SQLAlchemyError: On database errors
        """
        self.logger.info(f"Creating new ETF: {etf_dto.ticker}")
        with self.db_manager.get_session() as session:
            etf_dao = EtfDAO()
            etf_dao.ticker = etf_dto.ticker
            etf_dao.name = etf_dto.name
            etf_dao.isin = etf_dto.isin
            etf_dao.launchDate = etf_dto.launchDate
            etf_dao.capital = etf_dto.capital
            etf_dao.replication = etf_dto.replication
            etf_dao.volatility = etf_dto.volatility
            etf_dao.currency = etf_dto.currency
            etf_dao.dividendType = etf_dto.dividendType
            etf_dao.dividendFrequency = etf_dto.dividendFrequency
            etf_dao.yeld = etf_dto.yeld
            session.add(etf_dao)
            self.logger.info(f"ETF {etf_dto.ticker} created successfully in database")

    def update(self, etf_dto: ETF) -> None:
        """
        Update an existing ETF

        Args:
            etf_dto: ETF DTO with new validated data (ticker identifies the record)

        Raises:
            ValueError: If ETF not found
            SQLAlchemyError: On database errors
        """
        self.logger.info(f"Updating ETF: {etf_dto.ticker}")
        with self.db_manager.get_session():
            etf_dao = EtfDAO.query.get(etf_dto.ticker)
            if not etf_dao:
                self.logger.error(f"ETF {etf_dto.ticker} not found for update")
                raise ValueError(f"ETF {etf_dto.ticker} not found")

            # Update all fields from DTO
            etf_dao.name = etf_dto.name
            etf_dao.isin = etf_dto.isin
            etf_dao.launchDate = etf_dto.launchDate
            etf_dao.capital = etf_dto.capital
            etf_dao.replication = etf_dto.replication
            etf_dao.volatility = etf_dto.volatility
            etf_dao.currency = etf_dto.currency
            etf_dao.dividendType = etf_dto.dividendType
            etf_dao.dividendFrequency = etf_dto.dividendFrequency
            etf_dao.yeld = etf_dto.yeld
            self.logger.info(f"ETF {etf_dto.ticker} updated successfully in database")

    def delete(self, ticker: str) -> None:
        """
        Delete an ETF

        Args:
            ticker: Ticker of the ETF to delete

        Raises:
            ValueError: If ETF not found
            SQLAlchemyError: On database errors
        """
        self.logger.info(f"Deleting ETF: {ticker}")
        with self.db_manager.get_session() as session:
            etf_dao = EtfDAO.query.get(ticker)
            if not etf_dao:
                self.logger.error(f"ETF {ticker} not found for deletion")
                raise ValueError(f"ETF {ticker} not found")

            session.delete(etf_dao)
            self.logger.info(f"ETF {ticker} deleted successfully from database")

    def exists(self, ticker: str) -> bool:
        """
        Check if an ETF exists

        Args:
            ticker: ETF ticker symbol

        Returns:
            True if exists, False otherwise
        """
        exists = EtfDAO.query.get(ticker) is not None
        self.logger.debug(f"ETF {ticker} exists: {exists}")
        return exists

    def get_quotes(self, ticker: str, period: str = "1Y") -> list[Quote]:
        """
        Retrieve quotes for an ETF within a specific period

        Args:
            ticker: ETF ticker symbol
            period: Time period (5D, 1M, 3M, 6M, 1Y, YTD, 5Y, Max)

        Returns:
            List of Quote DTOs
        """
        self.logger.info(f"Fetching quotes for ETF {ticker}, period: {period}")

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
        self.logger.debug(f"Calculated start date for period {period}: {start_date.strftime('%Y-%m-%d')}")

        # Query quotes from database
        quote_daos = (
            QuoteDAO.query.filter(QuoteDAO.Ticker == ticker, QuoteDAO.Date > start_date.strftime("%Y-%m-%d"))
            .order_by(QuoteDAO.Date)
            .all()
        )

        self.logger.info(f"Retrieved {len(quote_daos)} quotes for ETF {ticker}")

        # Convert DAOs to DTOs
        return [
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
