# -----------------------------------------------------------------------------
# Copyright (c) 2025 Salvatore D'Angelo, Code4Projects
# Licensed under the MIT License. See LICENSE.md for details.
# -----------------------------------------------------------------------------
from __future__ import annotations
from models import EtfDAO
from typing import TYPE_CHECKING
from core.database import DatabaseManager
from core.log import LoggerManager
from dto import ETF

if TYPE_CHECKING:
    from services.quote_service import QuoteService


class EtfService:
    """Application Service for ETF management and orchestration"""

    def __init__(self, db_manager: DatabaseManager, quote_service: "QuoteService"):
        """
        Initialize EtfService with dependencies

        Args:
            db_manager: DatabaseManager instance for session handling
            quote_service: QuoteService instance for quote operations
        """
        self.db_manager = db_manager
        self.quote_service = quote_service
        self.logger = LoggerManager.get_logger(self.__class__.__name__)
        self.logger.info("EtfService initialized")

    def get_all(self) -> list[ETF]:
        """
        Retrieve all ETFs from database

        Returns:
            List of ETF DTOs
        """
        self.logger.debug("Fetching all ETFs from database")
        etf_daos: list[EtfDAO] = EtfDAO.query.all()
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
            etf_dao: EtfDAO = EtfDAO()
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
            session.add(instance=etf_dao)
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

    def update_etf_quotes(self, ticker: str) -> dict:
        """
        Update quotes for a specific ETF (Application Service - Orchestration)

        Args:
            ticker: ETF ticker symbol

        Returns:
            Dictionary with status information:
            {
                'success': bool,
                'ticker': str,
                'message': str
            }
        """
        self.logger.info(f"Orchestrating quote update for ETF: {ticker}")

        try:
            # Check if ETF exists
            etf: ETF | None = self.get_by_ticker(ticker)
            if not etf:
                self.logger.warning(f"ETF {ticker} not found")
                return {"success": False, "ticker": ticker, "message": f"ETF {ticker} non trovato"}

            # Delegate to QuoteService (Domain Service)
            self.quote_service.update_quotes(ticker)

            message = "Quotazioni aggiornate con successo"
            self.logger.info(f"Successfully updated quotes for {ticker}")

            return {"success": True, "ticker": ticker, "message": message}

        except Exception as e:
            error_message = f"Errore durante l'aggiornamento: {str(e)}"
            self.logger.error(f"Failed to update quotes for {ticker}: {error_message}")
            return {"success": False, "ticker": ticker, "message": error_message}

    def update_all_etf_quotes(self) -> dict:
        """
        Update quotes for all ETFs (Application Service - Orchestration)

        Returns:
            Dictionary with overall status and individual results:
            {
                'success': bool,
                'total': int,
                'success_count': int,
                'failed_count': int,
                'failed_etfs': list,
                'results': list,
                'message': str
            }
        """
        self.logger.info("Orchestrating bulk quote update for all ETFs")

        # Get all ETFs
        etfs: list[ETF] = self.get_all()
        total: int = len(etfs)

        if total == 0:
            self.logger.warning("No ETFs found in database")
            return {
                "success": False,
                "message": "Nessun ETF trovato nel database",
                "total": 0,
                "success_count": 0,
                "failed_count": 0,
                "failed_etfs": [],
                "results": [],
            }

        self.logger.info(f"Found {total} ETFs to update")

        # Delegate to QuoteService for each ETF
        results = []
        success_count = 0
        failed_etfs = []

        for index, etf in enumerate(etfs, 1):
            self.logger.info(f"Processing ETF {index}/{total}: {etf.ticker}")

            try:
                self.quote_service.update_quotes(etf.ticker)
                message = "Aggiornato"
                results.append({"success": True, "ticker": etf.ticker, "message": message})
                success_count += 1

            except Exception as e:
                error_message = str(e)
                self.logger.error(f"Failed to update {etf.ticker}: {error_message}")
                results.append({"success": False, "ticker": etf.ticker, "message": error_message})
                failed_etfs.append({"ticker": etf.ticker, "name": etf.name, "error": error_message})

        # Prepare summary
        summary = {
            "success": len(failed_etfs) == 0,
            "total": total,
            "success_count": success_count,
            "failed_count": len(failed_etfs),
            "failed_etfs": failed_etfs,
            "results": results,
        }

        if len(failed_etfs) == 0:
            summary["message"] = f"Tutti i {total} ETF sono stati aggiornati con successo!"
            self.logger.info(f"Bulk update completed successfully: {success_count}/{total}")
        else:
            summary["message"] = f"Aggiornamento completato: {success_count} successi, {len(failed_etfs)} errori"
            self.logger.warning(
                f"Bulk update completed with errors: {success_count} success, {len(failed_etfs)} failed"
            )

        return summary
