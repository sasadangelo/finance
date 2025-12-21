# -----------------------------------------------------------------------------
# Copyright (c) 2025 Salvatore D'Angelo, Code4Projects
# Licensed under the MIT License. See LICENSE.md for details.
# -----------------------------------------------------------------------------
from typing import cast
from flask import render_template, request, redirect, url_for, flash
from core import LoggerManager
from controllers.types import WebResponse
from dto.index import Index
from pydantic import ValidationError
from sqlalchemy.exc import SQLAlchemyError
from services.index_service import IndexService


class IndexController:
    """Controller for managing Index routes"""

    def __init__(self, index_service: IndexService) -> None:
        """
        Initialize IndexController with an IndexService instance

        Args:
            index_service: IndexService instance for business logic
        """
        self.index_service = index_service
        self.logger = LoggerManager.get_logger(name=self.__class__.__name__)
        self.logger.info("IndexController initialized")

    def _parse_form_data(self, ticker: str | None = None) -> Index:
        """
        Parse form data and create Index DTO with validation

        Args:
            ticker: Optional ticker (for update, uses existing ticker)

        Returns:
            Index DTO with validated data

        Raises:
            ValidationError: If Pydantic validation fails
        """
        return Index(
            ticker=ticker or cast(str, request.form.get("ticker")),
            name=cast(str, request.form.get("name")),
        )

    def _handle_error(self, error: Exception, ticker: str | None, operation: str) -> None:
        """
        Handle errors and display appropriate flash messages

        Args:
            error: The exception that occurred
            ticker: Index ticker (if available)
            operation: Operation being performed (e.g., "creating", "updating")
        """
        if isinstance(error, ValidationError):
            errors: str = "; ".join([f"{err['loc'][0]}: {err['msg']}" for err in error.errors()])
            self.logger.warning(f"Validation error {operation} index {ticker}: {errors}")
            flash(message=f"Errori di validazione: {errors}", category="danger")
        elif isinstance(error, SQLAlchemyError):
            self.logger.error(f"Database error {operation} index {ticker}: {str(error)}")
            flash(message=f"Errore database: {str(error)}", category="danger")
        elif isinstance(error, ValueError):
            self.logger.warning(f"Business logic error {operation} index {ticker}: {str(error)}")
            flash(message=f"Errore: {str(error)}", category="danger")
        else:
            self.logger.exception(f"Unexpected error {operation} index {ticker}: {str(error)}")
            flash(message=f"Errore imprevisto: {str(error)}", category="danger")

    def index(self) -> WebResponse:
        """Display list of all indices"""
        self.logger.info("Fetching indices for index page")
        indices: list[Index] = self.index_service.get_all()
        self.logger.info(f"Retrieved {len(indices)} indices")
        return render_template(template_name_or_list="index/index.html", indices=indices)

    def create(self) -> WebResponse:
        """Display form to create a new index"""
        return render_template(template_name_or_list="index/create.html")

    def store(self) -> WebResponse:
        """Save a new index to database"""
        ticker: str | None = request.form.get("ticker")
        self.logger.info(f"Attempting to create new index with ticker: {ticker}")

        try:
            index_dto: Index = self._parse_form_data()
            self.index_service.create(index_dto)
            self.logger.info(f"Index {index_dto.ticker} created successfully")
            flash(message=f"Indice {index_dto.ticker} creato con successo!", category="success")
        except Exception as e:
            self._handle_error(error=e, ticker=ticker, operation="creating")

        return redirect(location=url_for(endpoint="index.index"))

    def edit(self, ticker: str) -> WebResponse:
        """Display form to edit an index"""
        self.logger.info(f"Fetching index {ticker} for editing")
        index: Index | None = self.index_service.get_by_ticker(ticker)
        if not index:
            self.logger.warning(f"Index {ticker} not found for editing")
            flash(message="Indice non trovato", category="danger")
            return redirect(location=url_for(endpoint="index.index"))
        return render_template(template_name_or_list="index/edit.html", index=index)

    def update(self, ticker: str) -> WebResponse:
        """Update an existing index"""
        self.logger.info(f"Attempting to update index {ticker}")

        try:
            index_dto: Index = self._parse_form_data(ticker=ticker)
            self.index_service.update(index_dto)
            self.logger.info(f"Index {ticker} updated successfully")
            flash(message=f"Indice {ticker} aggiornato con successo!", category="success")
        except Exception as e:
            self._handle_error(error=e, ticker=ticker, operation="updating")

        return redirect(location=url_for(endpoint="index.index"))

    def delete(self, ticker: str) -> WebResponse:
        """Delete an index"""
        self.logger.info(f"Attempting to delete index {ticker}")

        try:
            self.index_service.delete(ticker)
            self.logger.info(f"Index {ticker} deleted successfully")
            flash(message=f"Indice {ticker} eliminato con successo!", category="success")
        except Exception as e:
            self._handle_error(error=e, ticker=ticker, operation="deleting")

        return redirect(location=url_for(endpoint="index.index"))

    def show(self, ticker: str) -> WebResponse:
        """Display index details"""
        self.logger.info(f"Fetching index {ticker} details")
        index: Index | None = self.index_service.get_by_ticker(ticker)
        if not index:
            self.logger.warning(f"Index {ticker} not found")
            flash(message=f"Indice {ticker} non trovato!", category="danger")
            return redirect(location=url_for(endpoint="index.index"))

        return render_template(template_name_or_list="index/show.html", index=index)
