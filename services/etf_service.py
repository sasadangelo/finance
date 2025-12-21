# -----------------------------------------------------------------------------
# Copyright (c) 2025 Salvatore D'Angelo, Code4Projects
# Licensed under the MIT License. See LICENSE.md for details.
# -----------------------------------------------------------------------------
from __future__ import annotations
from datetime import datetime
from models import EtfDAO
from typing import TYPE_CHECKING, Any
from core.database import DatabaseManager
from core.log import LoggerManager
from dto import ETF
from dto.etf_screener_filters import ETFScreenerFilters
from mappers.etf_mapper import EtfMapper

if TYPE_CHECKING:
    from services.quote_service import QuoteService


class EtfService:
    """Application Service for ETF management and orchestration"""

    def __init__(self, db_manager: DatabaseManager, quote_service: "QuoteService") -> None:
        """
        Initialize EtfService with dependencies

        Args:
            db_manager: DatabaseManager instance for session handling
            quote_service: QuoteService instance for quote operations
        """
        self.db_manager = db_manager
        self.quote_service = quote_service
        self.logger = LoggerManager.get_logger(name=self.__class__.__name__)
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
        return [EtfMapper.to_dto(dao) for dao in etf_daos]

    def get_by_ticker(self, ticker: str) -> ETF | None:
        """
        Retrieve a specific ETF by ticker

        Args:
            ticker: ETF ticker symbol

        Returns:
            ETF DTO if found, None otherwise
        """
        self.logger.debug(f"Fetching ETF with ticker: {ticker}")
        etf_dao: EtfDAO | None = EtfDAO.query.get(ident=ticker)
        if etf_dao:
            self.logger.debug(f"ETF {ticker} found in database")
            return EtfMapper.to_dto(dao=etf_dao)
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
            etf_dao: EtfDAO = EtfMapper.to_dao(etf_dto)
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
            etf_dao: EtfDAO | None = EtfDAO.query.get(ident=etf_dto.ticker)
            if not etf_dao:
                self.logger.error(f"ETF {etf_dto.ticker} not found for update")
                raise ValueError(f"ETF {etf_dto.ticker} not found")

            # Update DAO using mapper
            EtfMapper.to_dao(etf_dto, dao=etf_dao)
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
            etf_dao: EtfDAO | None = EtfDAO.query.get(ticker)
            if not etf_dao:
                self.logger.error(f"ETF {ticker} not found for deletion")
                raise ValueError(f"ETF {ticker} not found")

            session.delete(instance=etf_dao)
            self.logger.info(f"ETF {ticker} deleted successfully from database")

    def exists(self, ticker: str) -> bool:
        """
        Check if an ETF exists

        Args:
            ticker: ETF ticker symbol

        Returns:
            True if exists, False otherwise
        """
        exists: bool = EtfDAO.query.get(ident=ticker) is not None
        self.logger.debug(f"ETF {ticker} exists: {exists}")
        return exists

    def update_etf_quotes(self, ticker: str) -> dict[str, Any]:
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
            error_message: str = f"Errore durante l'aggiornamento: {str(e)}"
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
            return self._create_empty_summary()

        self.logger.info(f"Found {total} ETFs to update")

        # Process all ETFs and collect results
        results = []
        failed_etfs = []

        for index, etf in enumerate(etfs, 1):
            self.logger.info(f"Processing ETF {index}/{total}: {etf.ticker}")
            result = self._update_single_etf_quotes(etf)
            results.append(result)

            if not result["success"]:
                failed_etfs.append({"ticker": etf.ticker, "name": etf.name, "error": result["message"]})

        # Prepare and return summary
        return self._create_update_summary(total, results, failed_etfs)

    def _update_single_etf_quotes(self, etf: ETF) -> dict[str, Any]:
        """
        Update quotes for a single ETF

        Args:
            etf: ETF to update

        Returns:
            Dictionary with update result
        """
        try:
            self.quote_service.update_quotes(ticker=etf.ticker)
            return {"success": True, "ticker": etf.ticker, "message": "Aggiornato"}
        except Exception as e:
            error_message = str(e)
            self.logger.error(f"Failed to update {etf.ticker}: {error_message}")
            return {"success": False, "ticker": etf.ticker, "message": error_message}

    def _create_empty_summary(self) -> dict[str, Any]:
        """Create summary for empty ETF list"""
        return {
            "success": False,
            "message": "Nessun ETF trovato nel database",
            "total": 0,
            "success_count": 0,
            "failed_count": 0,
            "failed_etfs": [],
            "results": [],
        }

    def _create_update_summary(self, total: int, results: list[dict], failed_etfs: list[dict]) -> dict[str, Any]:
        """
        Create summary for bulk update operation

        Args:
            total: Total number of ETFs processed
            results: List of individual update results
            failed_etfs: List of failed ETF updates

        Returns:
            Summary dictionary
        """
        success_count = sum(1 for r in results if r["success"])
        failed_count = len(failed_etfs)

        summary = {
            "success": failed_count == 0,
            "total": total,
            "success_count": success_count,
            "failed_count": failed_count,
            "failed_etfs": failed_etfs,
            "results": results,
        }

        if failed_count == 0:
            summary["message"] = f"Tutti i {total} ETF sono stati aggiornati con successo!"
            self.logger.info(f"Bulk update completed successfully: {success_count}/{total}")
        else:
            summary["message"] = f"Aggiornamento completato: {success_count} successi, {failed_count} errori"
            self.logger.warning(f"Bulk update completed with errors: {success_count} success, {failed_count} failed")

        return summary

    def screen_etfs(self, filters: ETFScreenerFilters) -> list[ETF]:
        """
        Screen ETFs based on provided filters

        Args:
            filters: ETFScreenerFilters DTO with filter criteria

        Returns:
            List of ETF DTOs matching the filters
        """
        self.logger.debug(f"Screening ETFs with filters: {filters}")

        # Get all ETFs and convert to DTOs using mapper
        etf_daos: list[EtfDAO] = EtfDAO.query.all()
        all_etfs: list[ETF] = [EtfMapper.to_dto(dao) for dao in etf_daos]

        # Apply filters using list comprehension
        filtered_etfs: list[ETF] = [etf for etf in all_etfs if self._matches_filters(etf, filters)]

        self.logger.info(f"Screener found {len(filtered_etfs)} ETFs matching filters")
        return filtered_etfs

    def _matches_filters(self, etf: ETF, filters: ETFScreenerFilters) -> bool:
        """
        Check if an ETF matches all provided filters

        Args:
            etf: ETF to check
            filters: Filter criteria

        Returns:
            True if ETF matches all filters, False otherwise
        """
        # Asset type filter
        if filters.asset_type is not None and etf.assetType != filters.asset_type:
            return False

        # Dividend type filter
        if filters.dividend_type and etf.dividendType != filters.dividend_type:
            return False

        # Currency filter
        if filters.currency and etf.currency != filters.currency:
            return False

        # Replication type filter
        if filters.replication and (not etf.replication or etf.replication != filters.replication):
            return False

        # Index filter
        if filters.index_ticker and etf.indexTicker != filters.index_ticker:
            return False

        # Fund size filter
        if filters.min_capital is not None and (not etf.capital or etf.capital < filters.min_capital):
            return False

        # Age filter
        if filters.min_age_years is not None:
            age_years: float | None = self._calculate_etf_age(launch_date_str=etf.launchDate)
            if age_years is None or age_years < filters.min_age_years:
                return False

        return True

    def _calculate_etf_age(self, launch_date_str: str) -> float | None:
        """
        Calculate ETF age in years from launch date string

        Args:
            launch_date_str: Launch date in YYYY-MM-DD format

        Returns:
            Age in years, or None if date is invalid
        """
        try:
            launch_date: datetime = datetime.strptime(launch_date_str, "%Y-%m-%d")
            current_date: datetime = datetime.now()
            age_days: int = (current_date - launch_date).days
            return age_days / 365.25  # Account for leap years
        except (ValueError, AttributeError):
            return None
