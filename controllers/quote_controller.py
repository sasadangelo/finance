# -----------------------------------------------------------------------------
# Copyright (c) 2025 Salvatore D'Angelo, Code4Projects
# Licensed under the MIT License. See LICENSE.md for details.
# -----------------------------------------------------------------------------
from dto.quote import Quote
from flask import jsonify, request, Response, current_app
from services import QuoteService, EtfService
from dto import QuotePeriod
from core.log import LoggerManager
import json


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
        self.logger = LoggerManager.get_logger(name=self.__class__.__name__)
        self.logger.info("QuoteController initialized")

    def get_quotes(self, ticker: str):
        """
        Return quote data in JSON format for Chart.js (HTTP handling only)

        Args:
            ticker: ETF ticker symbol

        Returns:
            JSON response with quote data or error
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
                return jsonify({"error": "No quotes available"}), 404

            # Format data for Chart.js
            dates = [quote.date for quote in quotes]
            prices = [float(quote.close) for quote in quotes]

            self.logger.info(f"Retrieved {len(quotes)} quotes for ETF {ticker}")
            return jsonify({"labels": dates, "data": prices, "ticker": ticker})

        except Exception as e:
            self.logger.error(f"Error fetching quotes for ETF {ticker}: {str(e)}")
            return jsonify({"error": str(e)}), 500

    def update_single(self, ticker: str):
        """
        Update quotes for a single ETF (HTTP handling only)
        Delegates orchestration to EtfService (Application Service)

        Args:
            ticker: ETF ticker symbol

        Returns:
            JSON response with update status
        """
        self.logger.info(f"HTTP request: update quotes for single ETF: {ticker}")

        try:
            # Delegate to Application Service (orchestration)
            result = self.etf_service.update_etf_quotes(ticker)

            status_code = 200 if result["success"] else (404 if "non trovato" in result["message"] else 500)
            return jsonify(result), status_code

        except Exception as e:
            self.logger.exception(f"Unexpected error updating quotes for {ticker}: {str(e)}")
            return jsonify({"success": False, "ticker": ticker, "message": str(e)}), 500

    # def update_all(self):
    #     """
    #     Update quotes for all ETFs (HTTP handling only)
    #     Delegates orchestration to EtfService (Application Service)

    #     Returns:
    #         JSON response with overall status and individual results
    #     """
    #     self.logger.info("HTTP request: update quotes for all ETFs")

    #     try:
    #         # Delegate to Application Service (orchestration)
    #         summary = self.etf_service.update_all_etf_quotes()

    #         status_code = 200 if summary.get("total", 0) > 0 else 404
    #         return jsonify(summary), status_code

    #     except Exception as e:
    #         self.logger.exception(f"Unexpected error during bulk update: {str(e)}")
    #         return jsonify({"success": False, "message": f"Errore imprevisto: {str(e)}"}), 500

    def update_all_stream(self):
        """
        Update quotes for all ETFs with Server-Sent Events (SSE) for real-time progress

        Returns:
            SSE stream with progress updates
        """
        self.logger.info("HTTP request: update quotes for all ETFs (SSE stream)")

        # Get Flask app instance BEFORE creating the generator
        app = current_app._get_current_object()

        def generate():
            """Generator function that yields SSE events"""
            with app.app_context():
                try:
                    # Get all ETFs
                    etfs = self.etf_service.get_all()
                    total = len(etfs)

                    if total == 0:
                        yield f"data: {json.dumps({'error': 'Nessun ETF trovato nel database'})}\n\n"
                        return

                    self.logger.info(f"Starting bulk update for {total} ETFs via SSE")

                    success_count = 0
                    failed_etfs = []

                    # Process each ETF and send progress updates
                    for index, etf in enumerate(etfs, 1):
                        try:
                            # Update quotes for this ETF
                            self.etf_service.update_etf_quotes(etf.ticker)

                            success_count += 1
                            progress = int((index / total) * 100)

                            # Send success event
                            event_data = {
                                "progress": progress,
                                "current": index,
                                "total": total,
                                "ticker": etf.ticker,
                                "name": etf.name,
                                "status": "success",
                                "message": "Aggiornato",
                            }
                            yield f"data: {json.dumps(event_data)}\n\n"

                            self.logger.debug(f"SSE: Updated {etf.ticker} ({index}/{total})")

                        except Exception as e:
                            # ETF update failed, but continue with others
                            error_message = str(e)
                            failed_etfs.append({"ticker": etf.ticker, "name": etf.name, "error": error_message})

                            progress = int((index / total) * 100)

                            # Send error event
                            event_data = {
                                "progress": progress,
                                "current": index,
                                "total": total,
                                "ticker": etf.ticker,
                                "name": etf.name,
                                "status": "error",
                                "message": error_message,
                            }
                            yield f"data: {json.dumps(event_data)}\n\n"

                            self.logger.warning(f"SSE: Failed to update {etf.ticker}: {error_message}")

                    # Send completion event
                    completion_data = {
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
                    yield f"data: {json.dumps(completion_data)}\n\n"

                    self.logger.info(f"SSE: Bulk update completed - {success_count}/{total} successful")

                except Exception as e:
                    # Unexpected error
                    self.logger.exception(f"SSE: Unexpected error during bulk update: {str(e)}")
                    error_data = {"error": True, "message": f"Errore imprevisto: {str(e)}"}
                    yield f"data: {json.dumps(error_data)}\n\n"

        return Response(generate(), mimetype="text/event-stream")
