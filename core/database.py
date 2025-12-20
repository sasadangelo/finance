# -----------------------------------------------------------------------------
# Copyright (c) 2025 Salvatore D'Angelo, Code4Projects
# Licensed under the MIT License. See LICENSE.md for details.
# -----------------------------------------------------------------------------
from contextlib import contextmanager
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.exc import SQLAlchemyError
import logging

db: SQLAlchemy = SQLAlchemy()


class DatabaseManager:
    """
    Database manager with context manager for session handling.
    Provides automatic transaction management with commit/rollback.
    """

    def __init__(self, db_instance=None) -> None:
        """
        Initialize DatabaseManager

        Args:
            db_instance: SQLAlchemy instance (optional, defaults to global db)
        """
        self._db = db_instance or db
        self._logger = logging.getLogger(name=__name__)

    @contextmanager
    def get_session(self):
        """
        Context manager for database sessions.
        Automatically handles commit, rollback, and session cleanup.

        Usage:
            with db_manager.get_session() as session:
                # perform database operations
                session.add(obj)
                # commit happens automatically on success

        Yields:
            session: SQLAlchemy session object

        Raises:
            SQLAlchemyError: On database errors
            Exception: On unexpected errors
        """
        session = self._db.session
        try:
            yield session
            session.commit()
        except SQLAlchemyError:
            session.rollback()
            self._logger.exception("Database session error")
            raise
        except Exception:
            session.rollback()
            self._logger.exception("Unexpected error in database session")
            raise

    def query(self, model):
        """
        Helper method to create queries

        Args:
            model: SQLAlchemy model class

        Returns:
            Query object
        """
        return model.query

    @property
    def session(self):
        """Get the current session (for read-only operations)"""
        return self._db.session
