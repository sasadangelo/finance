# -----------------------------------------------------------------------------
# Copyright (c) 2025 Salvatore D'Angelo, Code4Projects
# Licensed under the MIT License. See LICENSE.md for details.
# -----------------------------------------------------------------------------
from models import EtfDAO, QuoteDAO
from database import db
from dto import ETF, Quote
import datetime as dt
from dateutil.relativedelta import relativedelta


class EtfService:
    """Service layer for ETF management"""

    @staticmethod
    def get_all_etfs():
        """Retrieve all ETFs from database"""
        return EtfDAO.query.all()

    @staticmethod
    def get_etf_by_ticker(ticker):
        """Retrieve a specific ETF by ticker"""
        return EtfDAO.query.get(ticker)

    @staticmethod
    def create_etf(etf_dto: ETF):
        """
        Create a new ETF

        Args:
            etf_dto: ETF DTO with validated data

        Returns:
            tuple: (etf_model, error_message)
        """
        try:
            # Create model from DTO
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
            db.session.add(etf)
            db.session.commit()
            return etf, None
        except Exception as e:
            db.session.rollback()
            return None, str(e)

    @staticmethod
    def update_etf(ticker, etf_dto: ETF):
        """
        Update an existing ETF

        Args:
            ticker: Ticker of the ETF to update
            etf_dto: ETF DTO with new validated data

        Returns:
            tuple: (etf_model, error_message)
        """
        try:
            etf = EtfDAO.query.get(ticker)
            if not etf:
                return None, "ETF not found"

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

            db.session.commit()
            return etf, None
        except Exception as e:
            db.session.rollback()
            return None, str(e)

    @staticmethod
    def delete_etf(ticker):
        """Delete an ETF"""
        try:
            etf = EtfDAO.query.get(ticker)
            if not etf:
                return False, "ETF non trovato"

            db.session.delete(etf)
            db.session.commit()
            return True, None
        except Exception as e:
            db.session.rollback()
            return False, str(e)

    @staticmethod
    def etf_exists(ticker):
        """Check if an ETF exists"""
        return EtfDAO.query.get(ticker) is not None

    @staticmethod
    def get_quotes(ticker, period="1Y"):
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
