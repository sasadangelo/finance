# -----------------------------------------------------------------------------
# Copyright (c) 2025 Salvatore D'Angelo, Code4Projects
# Licensed under the MIT License. See LICENSE.md for details.
# -----------------------------------------------------------------------------
from typing import cast
from flask import render_template, request, redirect, url_for, flash
from core import LoggerManager
from controllers.types import WebResponse
from dto import ETF, ETFAssetType, Index, ETFScreenerFilters
from pydantic import ValidationError
from sqlalchemy.exc import SQLAlchemyError
from services import EtfService
from services.index_service import IndexService


class EtfController:
    """Controller for managing ETF routes"""

    def __init__(self, etf_service: EtfService, index_service: IndexService) -> None:
        """
        Initialize EtfController with service instances

        Args:
            etf_service: EtfService instance for business logic
            index_service: IndexService instance for index data
        """
        self.etf_service = etf_service
        self.index_service = index_service
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
        # Parse assetType from form
        asset_type_str: str | None = request.form.get("assetType")
        asset_type: ETFAssetType | None = None
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
            indexTicker=request.form.get("indexTicker") or None,
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
            errors: str = "; ".join([f"{err['loc'][0]}: {err['msg']}" for err in error.errors()])
            self.logger.warning(f"Validation error {operation} ETF {ticker}: {errors}")
            flash(message=f"Errori di validazione: {errors}", category="danger")
        elif isinstance(error, SQLAlchemyError):
            self.logger.error(f"Database error {operation} ETF {ticker}: {str(error)}")
            flash(message=f"Errore database: {str(error)}", category="danger")
        elif isinstance(error, ValueError):
            self.logger.warning(f"Business logic error {operation} ETF {ticker}: {str(error)}")
            flash(message=f"Errore: {str(error)}", category="danger")
        else:
            self.logger.exception(f"Unexpected error {operation} ETF {ticker}: {str(error)}")
            flash(message=f"Errore imprevisto: {str(error)}", category="danger")

    def _get_filter_params(self) -> dict[str, str | None]:
        """Extract filter parameters from request"""
        filter_keys = [
            "asset_type",
            "dividend_type",
            "currency",
            "replication",
            "index_ticker",
            "min_capital",
            "min_age_years",
        ]
        return {key: request.args.get(key) for key in filter_keys}

    def _create_filters(self, params: dict[str, str | None]) -> ETFScreenerFilters:
        """Create ETFScreenerFilters object from request parameters"""
        return ETFScreenerFilters(
            asset_type=ETFAssetType(params["asset_type"]) if params["asset_type"] else None,
            dividend_type=params["dividend_type"] or None,
            currency=params["currency"] or None,
            replication=params["replication"] or None,
            index_ticker=params["index_ticker"] or None,
            min_capital=float(params["min_capital"]) if params["min_capital"] else None,
            min_age_years=int(params["min_age_years"]) if params["min_age_years"] else None,
        )

    def index(self) -> WebResponse:
        """Display list of all ETFs with optional filters"""

        self.logger.info("Fetching ETFs for index page")

        # Get filter parameters from request
        filter_params: dict[str, str | None] = self._get_filter_params()

        # Check if any filter is applied
        has_filters: bool = any(filter_params.values())

        # Create filters object
        filters: ETFScreenerFilters = self._create_filters(filter_params)

        # Cache all ETFs to avoid duplicate queries
        all_etfs: list[ETF] = self.etf_service.get_all()

        # Get ETFs (filtered or all)
        if has_filters:
            etfs: list[ETF] = self.etf_service.screen_etfs(filters)
            self.logger.info(f"Screener returned {len(etfs)} ETFs")
        else:
            etfs = all_etfs
            self.logger.info(f"Retrieved {len(etfs)} ETFs")

        # Get unique values for filter dropdowns using cached all_etfs
        currencies: list[str] = sorted(set(etf.currency for etf in all_etfs if etf.currency))
        replications: list[str] = sorted(set(etf.replication for etf in all_etfs if etf.replication))
        dividend_types: list[str] = sorted(set(etf.dividendType for etf in all_etfs if etf.dividendType))
        index_tickers: list[str] = sorted(set(etf.indexTicker for etf in all_etfs if etf.indexTicker))

        return render_template(
            template_name_or_list="etf/index.html",
            etfs=etfs,
            filters=filters,
            asset_types=ETFAssetType,
            currencies=currencies,
            replications=replications,
            dividend_types=dividend_types,
            index_tickers=index_tickers,
            has_filters=has_filters,
        )

    def create(self) -> WebResponse:
        """Display form to create a new ETF"""
        # Get all indices for dropdown
        indices: list[Index] = self.index_service.get_all()
        return render_template(template_name_or_list="etf/create.html", indices=indices)

    def store(self) -> WebResponse:
        """Save a new ETF to database"""
        ticker: str | None = request.form.get("ticker")
        self.logger.info(f"Attempting to create new ETF with ticker: {ticker}")

        try:
            etf_dto: ETF = self._parse_form_data()
            self.etf_service.create(etf_dto)
            self.logger.info(f"ETF {etf_dto.ticker} created successfully")
            flash(message=f"ETF {etf_dto.ticker} creato con successo!", category="success")
        except Exception as e:
            self._handle_error(error=e, ticker=ticker, operation="creating")

        return redirect(location=url_for(endpoint="etf.index"))

    def edit(self, ticker: str) -> WebResponse:
        """Display form to edit an ETF"""
        self.logger.info(f"Fetching ETF {ticker} for editing")
        etf: ETF | None = self.etf_service.get_by_ticker(ticker)
        if not etf:
            self.logger.warning(f"ETF {ticker} not found for editing")
            flash(message="ETF non trovato", category="danger")
            return redirect(location=url_for(endpoint="etf.index"))
        # Get all indices for dropdown
        indices: list[Index] = self.index_service.get_all()
        return render_template(template_name_or_list="etf/edit.html", etf=etf, indices=indices)

    def update(self, ticker: str) -> WebResponse:
        """Update an existing ETF"""
        self.logger.info(f"Attempting to update ETF {ticker}")

        try:
            etf_dto: ETF = self._parse_form_data(ticker=ticker)
            self.etf_service.update(etf_dto)
            self.logger.info(f"ETF {ticker} updated successfully")
            flash(message=f"ETF {ticker} aggiornato con successo!", category="success")
        except Exception as e:
            self._handle_error(error=e, ticker=ticker, operation="updating")

        return redirect(location=url_for(endpoint="etf.index"))

    def delete(self, ticker: str) -> WebResponse:
        """Delete an ETF"""
        self.logger.info(f"Attempting to delete ETF {ticker}")

        try:
            self.etf_service.delete(ticker)
            self.logger.info(f"ETF {ticker} deleted successfully")
            flash(message=f"ETF {ticker} eliminato con successo!", category="success")
        except Exception as e:
            self._handle_error(error=e, ticker=ticker, operation="deleting")

        return redirect(location=url_for(endpoint="etf.index"))

    def show(self, ticker: str) -> WebResponse:
        """Display ETF details"""
        self.logger.info(f"Fetching ETF {ticker} details")
        etf: ETF | None = self.etf_service.get_by_ticker(ticker)
        if not etf:
            self.logger.warning(f"ETF {ticker} not found")
            flash(message=f"ETF {ticker} non trovato!", category="danger")
            return redirect(location=url_for(endpoint="etf.index"))

        # Get index details if ETF has an index reference
        index: Index | None = None
        if etf.indexTicker:
            index = self.index_service.get_by_ticker(ticker=etf.indexTicker)

        return render_template(template_name_or_list="etf/show.html", etf=etf, index=index)
