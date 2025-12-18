# -----------------------------------------------------------------------------
# Copyright (c) 2025 Salvatore D'Angelo, Code4Projects
# Licensed under the MIT License. See LICENSE.md for details.
# -----------------------------------------------------------------------------
from flask import render_template, request, redirect, url_for, flash
from services import EtfService
from dto import ETF
from pydantic import ValidationError


class EtfController:
    """Controller for managing ETF routes"""

    @staticmethod
    def index():
        """Display list of all ETFs"""
        etfs = EtfService.get_all_etfs()
        return render_template("etf/index.html", etfs=etfs)

    @staticmethod
    def create():
        """Display form to create a new ETF"""
        return render_template("etf/create.html")

    @staticmethod
    def store():
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

            # Pass DTO to service
            etf, error = EtfService.create_etf(etf_dto)
            if error:
                flash(f"Errore nella creazione dell'ETF: {error}", "danger")
            else:
                flash(f"ETF {etf.ticker} creato con successo!", "success")

        except ValidationError as e:
            # Handle validation errors
            errors = "; ".join([f"{err['loc'][0]}: {err['msg']}" for err in e.errors()])
            flash(f"Errori di validazione: {errors}", "danger")
        except ValueError as e:
            flash(f"Errore nei dati: {str(e)}", "danger")

        return redirect(url_for("etf.index"))

    @staticmethod
    def edit(ticker):
        """Display form to edit an ETF"""
        etf = EtfService.get_etf_by_ticker(ticker)
        if not etf:
            flash("ETF non trovato", "danger")
            return redirect(url_for("etf.index"))
        return render_template("etf/edit.html", etf=etf)

    @staticmethod
    def update(ticker):
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

            # Pass DTO to service
            etf, error = EtfService.update_etf(ticker, etf_dto)
            if error:
                flash(f"Errore nell'aggiornamento dell'ETF: {error}", "danger")
            else:
                flash(f"ETF {ticker} aggiornato con successo!", "success")

        except ValidationError as e:
            errors = "; ".join([f"{err['loc'][0]}: {err['msg']}" for err in e.errors()])
            flash(f"Errori di validazione: {errors}", "danger")
        except ValueError as e:
            flash(f"Errore nei dati: {str(e)}", "danger")

        return redirect(url_for("etf.index"))

    @staticmethod
    def delete(ticker):
        """Delete an ETF"""
        success, error = EtfService.delete_etf(ticker)
        if error:
            flash(f"Errore nell'eliminazione dell'ETF: {error}", "danger")
        else:
            flash(f"ETF {ticker} eliminato con successo!", "success")

        return redirect(url_for("etf.index"))

    @staticmethod
    def show(ticker):
        """Display ETF details"""
        etf = EtfService.get_etf_by_ticker(ticker)
        if not etf:
            flash(f"ETF {ticker} non trovato!", "danger")
            return redirect(url_for("etf.index"))

        return render_template("etf/show.html", etf=etf)

    @staticmethod
    def get_quotes(ticker):
        """Return quote data in JSON format for Chart.js"""
        from flask import jsonify, request

        # Get period from query parameter (default 1Y)
        period = request.args.get("period", "1Y")

        try:
            # Use service layer to get quotes
            quotes = EtfService.get_quotes(ticker, period)

            if not quotes:
                return jsonify({"error": "No quotes available"}), 404

            # Format data for Chart.js
            dates = [quote.date for quote in quotes]
            prices = [float(quote.close) for quote in quotes]

            return jsonify({"labels": dates, "data": prices, "ticker": ticker})

        except Exception as e:
            return jsonify({"error": str(e)}), 500
