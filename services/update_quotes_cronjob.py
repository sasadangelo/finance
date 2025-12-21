# -----------------------------------------------------------------------------
# Copyright (c) 2025 Salvatore D'Angelo, Code4Projects
# Licensed under the MIT License. See LICENSE.md for details.
# -----------------------------------------------------------------------------
"""
Cron job for updating ETF quotes daily.
Runs at 11 PM Monday-Friday (excluding weekends) by default.
"""
from __future__ import annotations

from typing import TYPE_CHECKING
from core.cronjob import CronJob
from core.database import DatabaseManager
from services.etf_service import EtfService
from services.quote_service import QuoteService

if TYPE_CHECKING:
    from flask import Flask


class UpdateQuotesCronJob(CronJob):
    """
    Cron job that updates quotes for all ETFs in the database.
    Scheduled to run at 11 PM Monday-Friday by default.
    """

    def __init__(self, db_manager: DatabaseManager, app: Flask) -> None:
        """
        Initialize the UpdateQuotesCronJob.

        Args:
            db_manager: DatabaseManager instance for database operations
            app: Flask application instance for context
        """
        super().__init__()
        self.db_manager = db_manager
        self.app = app

        # Initialize services
        self.quote_service = QuoteService(db_manager=db_manager)
        self.etf_service = EtfService(db_manager=db_manager, quote_service=self.quote_service)

        self._logger.info("UpdateQuotesCronJob initialized")

    def action(self) -> None:
        """
        Execute the quote update action for all ETFs.
        This method is called by the scheduler according to the cron expression.
        """
        self._logger.info("Starting scheduled quote update for all ETFs...")

        try:
            # Execute within Flask application context
            with self.app.app_context():
                # Use the EtfService to update all ETF quotes
                result = self.etf_service.update_all_etf_quotes()

            # Log the results
            if result["success"]:
                self._logger.info(
                    f"Quote update completed successfully: " f"{result['success_count']}/{result['total']} ETFs updated"
                )
            else:
                self._logger.warning(
                    f"Quote update completed with errors: "
                    f"{result['success_count']} success, {result['failed_count']} failed"
                )

                # Log failed ETFs
                if result["failed_etfs"]:
                    for failed in result["failed_etfs"]:
                        self._logger.error(f"Failed to update {failed['ticker']} ({failed['name']}): {failed['error']}")

        except Exception as e:
            self._logger.exception(f"Unexpected error during quote update: {str(e)}")

    def get_default_cron_expression(self) -> str:
        """
        Get the default cron expression for this job.
        Default: 11 PM Monday-Friday (0 23 * * 1-5)

        Returns:
            Default cron expression string
        """
        return "0 23 * * 1-5"

    def get_cron_expression_key(self) -> str:
        """
        Get the configuration key for this job's cron expression.

        Returns:
            Configuration key string
        """
        return "quotes_crontab"


# Made with Bob
