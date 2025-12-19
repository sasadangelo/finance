# -----------------------------------------------------------------------------
# Copyright (c) 2025 Salvatore D'Angelo, Code4Projects
# Licensed under the MIT License. See LICENSE.md for details.
# -----------------------------------------------------------------------------
from flask import render_template, request, redirect, url_for, flash
from dto import ETF
from pydantic import ValidationError
from sqlalchemy.exc import SQLAlchemyError
from services import EtfService


class EtfController:
    """Controller for managing ETF routes"""

    def __init__(self, etf_service: EtfService):
        """
        Initialize EtfController with an EtfService instance

        Args:
            etf_service: EtfService instance for business logic
        """
        self.etf_service = etf_service

    def index(self):
        """Display list of all ETFs"""
        etfs = self.etf_service.get_all()
        return render_template("etf/index.html", etfs=etfs)

    def create(self):
        """Display form to create a new ETF"""
        return render_template("etf/create.html")

    def store(self):
        """Save a new ETF to database"""
        try:
            # Create DTO from form data with validation
            etf_dto = ETF(
                ticker=request.form.get("ticker"),
                name=request.form.get("name"),
                isin=request.form.get("isin") or None,
                launchDate=request.form.get("launchDate") or None,
                capital=float(request.form.get("capital")) if request.form.get("capital") else None,
                replication=request.form.get("replication") or None,
                volatility=float(request.form.get("volatility")) if request.form.get("volatility") else None,
                currency=request.form.get("currency") or None,
                dividendType=request.form.get("dividendType") or None,
                dividendFrequency=(
                    int(request.form.get("dividendFrequency")) if request.form.get("dividendFrequency") else None
                ),
                yeld=float(request.form.get("yeld")) if request.form.get("yeld") else None,
            )

            # Call service - exceptions propagate from context manager
            self.etf_service.create(etf_dto)
            flash(f"ETF {etf_dto.ticker} creato con successo!", "success")

        except ValidationError as e:
            # Handle Pydantic validation errors
            errors = "; ".join([f"{err['loc'][0]}: {err['msg']}" for err in e.errors()])
            flash(f"Errori di validazione: {errors}", "danger")
        except SQLAlchemyError as e:
            # Handle database errors (from context manager)
            flash(f"Errore database: {str(e)}", "danger")
        except ValueError as e:
            # Handle business logic errors
            flash(f"Errore: {str(e)}", "danger")
        except Exception as e:
            # Catch-all for unexpected errors
            flash(f"Errore imprevisto: {str(e)}", "danger")

        return redirect(url_for("etf.index"))

    def edit(self, ticker):
        """Display form to edit an ETF"""
        etf = self.etf_service.get_by_ticker(ticker)
        if not etf:
            flash("ETF non trovato", "danger")
            return redirect(url_for("etf.index"))
        return render_template("etf/edit.html", etf=etf)

    def update(self, ticker):
        """Update an existing ETF"""
        try:
            # Create DTO from form data with validation
            etf_dto = ETF(
                ticker=ticker,  # Keep existing ticker
                name=request.form.get("name"),
                isin=request.form.get("isin") or None,
                launchDate=request.form.get("launchDate") or None,
                capital=float(request.form.get("capital")) if request.form.get("capital") else None,
                replication=request.form.get("replication") or None,
                volatility=float(request.form.get("volatility")) if request.form.get("volatility") else None,
                currency=request.form.get("currency") or None,
                dividendType=request.form.get("dividendType") or None,
                dividendFrequency=(
                    int(request.form.get("dividendFrequency")) if request.form.get("dividendFrequency") else None
                ),
                yeld=float(request.form.get("yeld")) if request.form.get("yeld") else None,
            )

            # Call service - exceptions propagate from context manager
            self.etf_service.update(etf_dto)
            flash(f"ETF {ticker} aggiornato con successo!", "success")

        except ValidationError as e:
            errors = "; ".join([f"{err['loc'][0]}: {err['msg']}" for err in e.errors()])
            flash(f"Errori di validazione: {errors}", "danger")
        except SQLAlchemyError as e:
            flash(f"Errore database: {str(e)}", "danger")
        except ValueError as e:
            flash(f"Errore: {str(e)}", "danger")
        except Exception as e:
            flash(f"Errore imprevisto: {str(e)}", "danger")

        return redirect(url_for("etf.index"))

    def delete(self, ticker):
        """Delete an ETF"""
        try:
            self.etf_service.delete(ticker)
            flash(f"ETF {ticker} eliminato con successo!", "success")
        except SQLAlchemyError as e:
            flash(f"Errore database: {str(e)}", "danger")
        except ValueError as e:
            flash(f"Errore: {str(e)}", "danger")
        except Exception as e:
            flash(f"Errore imprevisto: {str(e)}", "danger")

        return redirect(url_for("etf.index"))

    def show(self, ticker):
        """Display ETF details"""
        etf = self.etf_service.get_by_ticker(ticker)
        if not etf:
            flash(f"ETF {ticker} non trovato!", "danger")
            return redirect(url_for("etf.index"))

        return render_template("etf/show.html", etf=etf)

    def get_quotes(self, ticker):
        """Return quote data in JSON format for Chart.js"""
        from flask import jsonify

        # Get period from query parameter (default 1Y)
        period = request.args.get("period", "1Y")

        try:
            # Use service layer to get quotes
            quotes = self.etf_service.get_quotes(ticker, period)

            if not quotes:
                return jsonify({"error": "No quotes available"}), 404

            # Format data for Chart.js
            dates = [quote.date for quote in quotes]
            prices = [float(quote.close) for quote in quotes]

            return jsonify({"labels": dates, "data": prices, "ticker": ticker})

        except Exception as e:
            return jsonify({"error": str(e)}), 500
