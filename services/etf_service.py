# -----------------------------------------------------------------------------
# Copyright (c) 2025 Salvatore D'Angelo, Code4Projects
# Licensed under the MIT License. See LICENSE.md for details.
# -----------------------------------------------------------------------------
from models.etf import Etf
from database import db
from dto.etf import ETF


class EtfService:
    """Service layer for ETF management"""

    @staticmethod
    def get_all_etfs():
        """Retrieve all ETFs from database"""
        return Etf.query.all()

    @staticmethod
    def get_etf_by_ticker(ticker):
        """Retrieve a specific ETF by ticker"""
        return Etf.query.get(ticker)

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
            etf = Etf(
                ticker=etf_dto.ticker,
                name=etf_dto.name,
                isin=etf_dto.isin,
                launchDate=etf_dto.launchDate,
                capital=etf_dto.capital,
                replication=etf_dto.replication,
                volatility=etf_dto.volatility,
                currency=etf_dto.currency,
                dividendType=etf_dto.dividendType,
                dividendFrequency=etf_dto.dividendFrequency,
                yeld=etf_dto.yeld,
            )
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
            etf = Etf.query.get(ticker)
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
            etf = Etf.query.get(ticker)
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
        return Etf.query.get(ticker) is not None


# Made with Bob
