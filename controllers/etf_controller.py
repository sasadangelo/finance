from flask import render_template, request, redirect, url_for, flash
from services.etf_service import EtfService
from dto.etf import ETF
from pydantic import ValidationError


class EtfController:
    """Controller per la gestione delle route degli ETF"""

    @staticmethod
    def index():
        """Mostra la lista di tutti gli ETF"""
        etfs = EtfService.get_all_etfs()
        return render_template("etf/index.html", etfs=etfs)

    @staticmethod
    def create():
        """Mostra il form per creare un nuovo ETF"""
        return render_template("etf/create.html")

    @staticmethod
    def store():
        """Salva un nuovo ETF nel database"""
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
                dividend=request.form.get("dividend") or None,
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
        """Mostra il form per modificare un ETF"""
        etf = EtfService.get_etf_by_ticker(ticker)
        if not etf:
            flash("ETF non trovato", "danger")
            return redirect(url_for("etf.index"))
        return render_template("etf/edit.html", etf=etf)

    @staticmethod
    def update(ticker):
        """Aggiorna un ETF esistente"""
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
                dividend=request.form.get("dividend") or None,
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
        """Elimina un ETF"""
        success, error = EtfService.delete_etf(ticker)
        if error:
            flash(f"Errore nell'eliminazione dell'ETF: {error}", "danger")
        else:
            flash(f"ETF {ticker} eliminato con successo!", "success")

        return redirect(url_for("etf.index"))

    @staticmethod
    def show(ticker):
        """Mostra i dettagli di un ETF"""
        etf = EtfService.get_etf_by_ticker(ticker)
        if not etf:
            flash("ETF non trovato", "danger")
            return redirect(url_for("etf.index"))
        return render_template("etf/show.html", etf=etf)


# Made with Bob
