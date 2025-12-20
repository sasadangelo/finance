# -----------------------------------------------------------------------------
# Copyright (c) 2025 Salvatore D'Angelo, Code4Projects
# Licensed under the MIT License. See LICENSE.md for details.
# -----------------------------------------------------------------------------
from dto import Quote, QuoteResponse, ErrorResponse, QuotePeriod
from flask import jsonify, request, Response, current_app
from core import LoggerManager
from controllers.types import APIResponse
from controllers.quote_sse_handler import QuoteSSEHandler
from services import QuoteService, EtfService


class QuoteController:
    """Controller for managing Quote routes (Presentation Layer - HTTP only)"""

    def __init__(self, quote_service: QuoteService, etf_service: EtfService) -> None:
        """
        Initialize QuoteController with services

        Args:
            quote_service: QuoteService instance (Domain Service)
            etf_service: EtfService instance (Application Service - Orchestration)
        """
        self.quote_service = quote_service
        self.etf_service = etf_service
        self.sse_handler = QuoteSSEHandler()
        self.logger = LoggerManager.get_logger(name=self.__class__.__name__)
        self.logger.info("QuoteController initialized")

    def get_quotes(self, ticker: str) -> APIResponse:
        """
        Return quote data in JSON format for Chart.js (HTTP handling only)

        Args:
            ticker: ETF ticker symbol

        Returns:
            JSON API response with explicit status code
        """
        # Get period from query parameter (default 1Y)
        period_str: str = request.args.get("period", "1Y")
        self.logger.info(f"HTTP request: get quotes for {ticker}, period: {period_str}")

        try:
            # Convert string to QuotePeriod enum
            period: QuotePeriod = QuotePeriod.from_string(period_str)

            # Delegate to Domain Service
            quotes: list[Quote] = self.quote_service.get_quotes(ticker, period)

            if not quotes:
                self.logger.warning(f"No quotes available for ETF {ticker}")
                error_response = ErrorResponse(error="No quotes available")
                return jsonify(error_response.model_dump()), 404

            # Create response DTO
            response: QuoteResponse = QuoteResponse(
                ticker=ticker, labels=[quote.date for quote in quotes], data=[float(quote.close) for quote in quotes]
            )

            self.logger.info(f"Retrieved {len(quotes)} quotes for ETF {ticker}")
            return jsonify(response.model_dump()), 200

        except Exception as e:
            self.logger.error(f"Error fetching quotes for ETF {ticker}: {str(e)}")
            error_response: ErrorResponse = ErrorResponse(error=str(e))
            return jsonify(error_response.model_dump()), 500

    def update_single(self, ticker: str) -> APIResponse:
        """
        Update quotes for a single ETF (HTTP handling only)
        Delegates orchestration to EtfService (Application Service)

        Args:
            ticker: ETF ticker symbol

        Returns:
            JSON API response with explicit status code
        """
        self.logger.info(f"HTTP request: update quotes for single ETF: {ticker}")

        try:
            # Delegate to Application Service (orchestration)
            result = self.etf_service.update_etf_quotes(ticker)

            status_code: int = 200 if result["success"] else (404 if "non trovato" in result["message"] else 500)
            return jsonify(result), status_code

        except Exception as e:
            self.logger.exception(f"Unexpected error updating quotes for {ticker}: {str(e)}")
            error_response: ErrorResponse = ErrorResponse(error=str(e))
            return jsonify({"success": False, "ticker": ticker, "message": error_response.error}), 500

    def update_all(self) -> Response:
        """
        Update quotes for all ETFs with Server-Sent Events (SSE) for real-time progress

        Returns:
            SSE stream response with progress updates
        """
        self.logger.info("HTTP request: update quotes for all ETFs (SSE stream)")

        # Get Flask app instance BEFORE creating the generator
        # _get_current_object() is a Werkzeug LocalProxy method (type checker doesn't know it)
        app = current_app._get_current_object()  # type: ignore[attr-defined]

        def generate_events():
            with app.app_context():
                try:
                    etfs = self.etf_service.get_all()

                    # Use QuoteSSEHandler for bulk quote update events
                    yield from self.sse_handler.generate_bulk_quote_update_events(
                        etfs=etfs, update_func=lambda etf: self.etf_service.update_etf_quotes(etf.ticker)
                    )

                except Exception as e:
                    self.logger.exception(f"SSE: Unexpected error during bulk update: {str(e)}")
                    error_event = self.sse_handler.create_error_event(f"Errore imprevisto: {str(e)}")
                    yield self.sse_handler.format_event(error_event)

        return Response(response=generate_events(), mimetype=self.sse_handler.MIMETYPE)
