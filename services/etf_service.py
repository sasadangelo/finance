# -----------------------------------------------------------------------------
# Copyright (c) 2025 Salvatore D'Angelo, Code4Projects
# Licensed under the MIT License. See LICENSE.md for details.
# -----------------------------------------------------------------------------
from models.etf import Etf
from database import db
from dto.etf import ETF


class EtfService:
    """Service layer per la gestione degli ETF"""

    @staticmethod
    def get_all_etfs():
        """Recupera tutti gli ETF dal database"""
        return Etf.query.all()

    @staticmethod
    def get_etf_by_ticker(ticker):
        """Recupera un ETF specifico tramite ticker"""
        return Etf.query.get(ticker)

    @staticmethod
    def create_etf(etf_dto: ETF):
        """
        Crea un nuovo ETF

        Args:
            etf_dto: ETF DTO con i dati validati

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
                dividend=etf_dto.dividend,
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
        Aggiorna un ETF esistente

        Args:
            ticker: Ticker dell'ETF da aggiornare
            etf_dto: ETF DTO con i nuovi dati validati

        Returns:
            tuple: (etf_model, error_message)
        """
        try:
            etf = Etf.query.get(ticker)
            if not etf:
                return None, "ETF non trovato"

            # Update all fields from DTO
            etf.name = etf_dto.name
            etf.isin = etf_dto.isin
            etf.launchDate = etf_dto.launchDate
            etf.capital = etf_dto.capital
            etf.replication = etf_dto.replication
            etf.volatility = etf_dto.volatility
            etf.currency = etf_dto.currency
            etf.dividend = etf_dto.dividend
            etf.dividendFrequency = etf_dto.dividendFrequency
            etf.yeld = etf_dto.yeld

            db.session.commit()
            return etf, None
        except Exception as e:
            db.session.rollback()
            return None, str(e)

    @staticmethod
    def delete_etf(ticker):
        """Elimina un ETF"""
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
        """Verifica se un ETF esiste"""
        return Etf.query.get(ticker) is not None


# Made with Bob
