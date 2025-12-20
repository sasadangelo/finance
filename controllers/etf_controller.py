# -----------------------------------------------------------------------------
# Copyright (c) 2025 Salvatore D'Angelo, Code4Projects
# Licensed under the MIT License. See LICENSE.md for details.
# -----------------------------------------------------------------------------
from typing import cast
from flask import render_template, request, redirect, url_for, flash
from core import LoggerManager
from controllers.types import WebResponse
from dto import ETF
from pydantic import ValidationError
from sqlalchemy.exc import SQLAlchemyError
from services import EtfService


class EtfController:
    """Controller for managing ETF routes"""

    def __init__(self, etf_service: EtfService) -> None:
        """
        Initialize EtfController with an EtfService instance

        Args:
            etf_service: EtfService instance for business logic
        """
        self.etf_service = etf_service
        self.logger = LoggerManager.get_logger(name=self.__class__.__name__)
        self.logger.info("EtfController initialized")

    def _parse_form_data(self, ticker: str | None = None) -> ETF:
        """
        Parse form data and create ETF DTO with validation

        Args:
            ticker: Optional ticker (for update, uses existing ticker)

        Returns:
            ETF DTO with validated data

        Raises:
            ValidationError: If Pydantic validation fails
        """
        from dto import ETFAssetType

        # Parse assetType from form
        asset_type_str = request.form.get("assetType")
        asset_type = None
        if asset_type_str:
            try:
                asset_type = ETFAssetType(asset_type_str)
            except ValueError:
                asset_type = None

        return ETF(
            ticker=ticker or cast(str, request.form.get("ticker")),
            name=cast(str, request.form.get("name")),
            isin=cast(str, request.form.get("isin") or None),
            launchDate=cast(str, request.form.get("launchDate") or None),
            capital=float(capital_str) if (capital_str := request.form.get("capital")) else None,
            replication=request.form.get("replication") or None,
            volatility=float(volatility_str) if (volatility_str := request.form.get("volatility")) else None,
            currency=cast(str, request.form.get("currency") or None),
            dividendType=request.form.get("dividendType") or None,
            assetType=asset_type,
            dividendFrequency=int(freq_str) if (freq_str := request.form.get("dividendFrequency")) else None,
            yeld=float(yeld_str) if (yeld_str := request.form.get("yeld")) else None,
        )

    def _handle_error(self, error: Exception, ticker: str | None, operation: str) -> None:
        """
        Handle errors and display appropriate flash messages

        Args:
            error: The exception that occurred
            ticker: ETF ticker (if available)
            operation: Operation being performed (e.g., "creating", "updating")
        """
        if isinstance(error, ValidationError):
            errors = "; ".join([f"{err['loc'][0]}: {err['msg']}" for err in error.errors()])
            self.logger.warning(f"Validation error {operation} ETF {ticker}: {errors}")
            flash(f"Errori di validazione: {errors}", "danger")
        elif isinstance(error, SQLAlchemyError):
            self.logger.error(f"Database error {operation} ETF {ticker}: {str(error)}")
            flash(f"Errore database: {str(error)}", "danger")
        elif isinstance(error, ValueError):
            self.logger.warning(f"Business logic error {operation} ETF {ticker}: {str(error)}")
            flash(f"Errore: {str(error)}", "danger")
        else:
            self.logger.exception(f"Unexpected error {operation} ETF {ticker}: {str(error)}")
            flash(f"Errore imprevisto: {str(error)}", "danger")

    def index(self) -> WebResponse:
        """Display list of all ETFs"""
        self.logger.info("Fetching all ETFs for index page")
        etfs: list[ETF] = self.etf_service.get_all()
        self.logger.info(f"Retrieved {len(etfs)} ETFs")
        return render_template(template_name_or_list="etf/index.html", etfs=etfs)

    def create(self) -> WebResponse:
        """Display form to create a new ETF"""
        return render_template(template_name_or_list="etf/create.html")

    def store(self) -> WebResponse:
        """Save a new ETF to database"""
        ticker = request.form.get("ticker")
        self.logger.info(f"Attempting to create new ETF with ticker: {ticker}")

        try:
            etf_dto = self._parse_form_data()
            self.etf_service.create(etf_dto)
            self.logger.info(f"ETF {etf_dto.ticker} created successfully")
            flash(f"ETF {etf_dto.ticker} creato con successo!", "success")
        except Exception as e:
            self._handle_error(e, ticker, "creating")

        return redirect(url_for("etf.index"))

    def edit(self, ticker: str) -> WebResponse:
        """Display form to edit an ETF"""
        self.logger.info(f"Fetching ETF {ticker} for editing")
        etf: ETF | None = self.etf_service.get_by_ticker(ticker)
        if not etf:
            self.logger.warning(f"ETF {ticker} not found for editing")
            flash(message="ETF non trovato", category="danger")
            return redirect(location=url_for(endpoint="etf.index"))
        return render_template(template_name_or_list="etf/edit.html", etf=etf)

    def update(self, ticker: str) -> WebResponse:
        """Update an existing ETF"""
        self.logger.info(f"Attempting to update ETF {ticker}")

        try:
            etf_dto = self._parse_form_data(ticker=ticker)
            self.etf_service.update(etf_dto)
            self.logger.info(f"ETF {ticker} updated successfully")
            flash(f"ETF {ticker} aggiornato con successo!", "success")
        except Exception as e:
            self._handle_error(e, ticker, "updating")

        return redirect(url_for("etf.index"))

    def delete(self, ticker: str) -> WebResponse:
        """Delete an ETF"""
        self.logger.info(f"Attempting to delete ETF {ticker}")

        try:
            self.etf_service.delete(ticker)
            self.logger.info(f"ETF {ticker} deleted successfully")
            flash(f"ETF {ticker} eliminato con successo!", "success")
        except Exception as e:
            self._handle_error(e, ticker, "deleting")

        return redirect(url_for("etf.index"))

    def show(self, ticker: str) -> WebResponse:
        """Display ETF details"""
        self.logger.info(f"Fetching ETF {ticker} details")
        etf: ETF | None = self.etf_service.get_by_ticker(ticker)
        if not etf:
            self.logger.warning(f"ETF {ticker} not found")
            flash(message=f"ETF {ticker} non trovato!", category="danger")
            return redirect(location=url_for("etf.index"))

        return render_template(template_name_or_list="etf/show.html", etf=etf)
