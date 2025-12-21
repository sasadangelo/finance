# -----------------------------------------------------------------------------
# Copyright (c) 2025 Salvatore D'Angelo, Code4Projects
# Licensed under the MIT License. See LICENSE.md for details.
# -----------------------------------------------------------------------------
"""
Base class for cron jobs that provides a common structure for running
periodic tasks with configurable intervals using APScheduler.
"""
from __future__ import annotations

from abc import ABC, abstractmethod
from apscheduler.events import EVENT_JOB_ERROR, JobEvent
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.cron import CronTrigger
from core.config import Settings, get_settings
from core.log import LoggerManager


class CronJob(ABC):
    """
    A base class for cron jobs that provides a common structure
    for running periodic tasks with configurable intervals.
    """

    def __init__(self) -> None:
        """
        Initializes the CronJob instance.
        """
        self._logger = LoggerManager.get_logger(name=self.__class__.__name__)
        self._scheduler = BackgroundScheduler()
        self._scheduler.add_listener(callback=self.handle_error, mask=EVENT_JOB_ERROR)

    def run(self) -> None:
        """
        Schedule the cron job using APScheduler.
        """
        self._logger.info(f"Starting {self.__class__.__name__} ...")

        # Get the cron expression
        cron_expression: str = self.get_cron_expression()
        trigger: CronTrigger = CronTrigger.from_crontab(cron_expression)

        # Add the job to the scheduler
        self._scheduler.add_job(func=self.action, trigger=trigger)

        self._logger.info(f"{self.__class__.__name__} scheduled with cron expression '{cron_expression}'.")
        self._scheduler.start()
        self._logger.info(f"{self.__class__.__name__} is running... Press Ctrl+C to exit.")

    @abstractmethod
    def action(self) -> None:
        """
        Abstract method for executing the cron job's specific action.
        Must be implemented by subclasses.
        """
        pass

    @abstractmethod
    def get_default_cron_expression(self) -> str:
        """
        Abstract method to provide the default cron expression for the job.
        Must be implemented in subclasses.

        Returns:
            Default cron expression string (e.g., "0 23 * * 1-5" for 11 PM Mon-Fri)
        """
        pass

    @abstractmethod
    def get_cron_expression_key(self) -> str:
        """
        Returns the configuration key for the cron job's expression.
        Must be implemented by subclasses.

        Returns:
            Configuration key string (e.g., "quotes_crontab")
        """
        pass

    def get_cron_expression(self) -> str:
        """
        Retrieve and validate the cron expression from the configuration.

        Returns:
            A valid cron expression string.
        """
        cron_expression_key: str = self.get_cron_expression_key()
        default_cron_expression: str = self.get_default_cron_expression()

        # Get the cron expression from the config with a fallback to the default
        settings: Settings = get_settings()
        cron_expression: str = getattr(settings.cron, cron_expression_key, default_cron_expression)

        # Validate the cron expression
        if not self._is_valid_cron_expression(cron_expression):
            self._logger.warning(
                f"Invalid crontab value for '{cron_expression_key}'; using default value {default_cron_expression}."
            )
            cron_expression = default_cron_expression

        return cron_expression

    def _is_valid_cron_expression(self, cron_expression: str) -> bool:
        """
        Validates a cron expression.

        Args:
            cron_expression: The cron expression string to validate.

        Returns:
            True if the cron expression is valid, otherwise False.
        """
        try:
            # Try to create a CronTrigger with the provided expression
            CronTrigger.from_crontab(expr=cron_expression)
            return True
        except (ValueError, TypeError):
            # If it raises an exception, it's an invalid cron expression
            return False

    def stop(self) -> None:
        """
        Stop the scheduler gracefully.
        """
        self._scheduler.shutdown()
        self._logger.info(f"{self.__class__.__name__} stopped.")

    def handle_error(self, event: JobEvent) -> None:
        """
        Handle errors raised by jobs.

        Args:
            event: Job event containing error information
        """
        exception = getattr(event, "exception", None)
        job = self._scheduler.get_job(event.job_id) if hasattr(event, "job_id") else None

        if job:
            self._logger.exception(f"An error occurred in job '{job.id}': {exception}")
        else:
            self._logger.exception(f"An error occurred in a job (job not found): {exception}")
