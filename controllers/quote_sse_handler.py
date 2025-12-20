# -----------------------------------------------------------------------------
# Copyright (c) 2025 Salvatore D'Angelo, Code4Projects
# Licensed under the MIT License. See LICENSE.md for details.
# -----------------------------------------------------------------------------
import json
from typing import Generator, Callable
from sqlalchemy.exc import SQLAlchemyError
from core.log import LoggerManager


class QuoteSSEHandler:
    """Handler for Server-Sent Events (SSE) streaming for quote updates"""

    MIMETYPE = "text/event-stream"

    def __init__(self):
        self.logger = LoggerManager.get_logger(name=self.__class__.__name__)

    def format_event(self, data: dict) -> str:
        """
        Format data as SSE event

        Args:
            data: Dictionary to send as SSE event

        Returns:
            SSE formatted string
        """
        return f"data: {json.dumps(data)}\n\n"

    def create_progress_event(self, index: int, total: int, ticker: str, name: str, status: str, message: str) -> dict:
        """Create progress event data for quote updates"""
        return {
            "progress": int((index / total) * 100),
            "current": index,
            "total": total,
            "ticker": ticker,
            "name": name,
            "status": status,
            "message": message,
        }

    def create_completion_event(self, total: int, success_count: int, failed_etfs: list) -> dict:
        """Create completion event data for quote updates"""
        return {
            "done": True,
            "progress": 100,
            "total": total,
            "success_count": success_count,
            "failed_count": len(failed_etfs),
            "failed_etfs": failed_etfs,
            "message": (
                f"Completato: {success_count} successi, {len(failed_etfs)} errori"
                if failed_etfs
                else f"Tutti i {total} ETF aggiornati con successo!"
            ),
        }

    def create_error_event(self, message: str) -> dict:
        """Create error event data"""
        return {"error": True, "message": message}

    def _process_single_etf(self, etf, index: int, total: int, update_func: Callable) -> tuple[str, bool, dict | None]:
        """
        Process update for a single ETF

        Args:
            etf: ETF object to update
            index: Current ETF index
            total: Total number of ETFs
            update_func: Function to call for update

        Returns:
            Tuple of (SSE event string, success boolean, error dict or None)
        """
        try:
            update_func(etf)

            event_data = self.create_progress_event(index, total, etf.ticker, etf.name, "success", "Aggiornato")
            self.logger.debug(f"SSE: Updated {etf.ticker} ({index}/{total})")

            return self.format_event(data=event_data), True, None

        except (ValueError, SQLAlchemyError) as e:
            error_message = str(e)
            error_dict = {
                "ticker": etf.ticker,
                "name": etf.name,
                "error": error_message,
            }

            event_data = self.create_progress_event(index, total, etf.ticker, etf.name, "error", error_message)
            self.logger.warning(f"SSE: Failed to update {etf.ticker}: {error_message}")

            return self.format_event(event_data), False, error_dict

    def generate_bulk_quote_update_events(self, etfs: list, update_func: Callable) -> Generator[str, None, None]:
        """
        Generate SSE events for bulk ETF quote updates

        Args:
            etfs: List of ETFs to update
            update_func: Function to call for each ETF update (receives ETF)

        Yields:
            SSE formatted event strings
        """
        total = len(etfs)

        if total == 0:
            yield self.format_event({"error": "Nessun ETF trovato nel database"})
            return

        self.logger.info(f"Starting bulk quote update for {total} ETFs via SSE")

        success_count = 0
        failed_etfs = []

        for index, etf in enumerate(etfs, 1):
            event, success, error = self._process_single_etf(etf, index, total, update_func)
            yield event

            if success:
                success_count += 1
            elif error:
                failed_etfs.append(error)

        # Send completion event
        completion_data = self.create_completion_event(total, success_count, failed_etfs)
        yield self.format_event(completion_data)

        self.logger.info(f"SSE: Bulk quote update completed - {success_count}/{total} successful")
