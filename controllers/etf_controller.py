# -----------------------------------------------------------------------------
# Copyright (c) 2025 Salvatore D'Angelo, Code4Projects
# Licensed under the MIT License. See LICENSE.md for details.
# -----------------------------------------------------------------------------
from flask import render_template, request, redirect, url_for, flash
from dto import ETF
from pydantic import ValidationError
from sqlalchemy.exc import SQLAlchemyError
from services import EtfService
from core.log import LoggerManager


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

    def index(self):
        """Display list of all ETFs"""
        self.logger.info("Fetching all ETFs for index page")
        etfs: list[ETF] = self.etf_service.get_all()
        self.logger.info(f"Retrieved {len(etfs)} ETFs")
        return render_template(template_name_or_list="etf/index.html", etfs=etfs)

    def create(self):
        """Display form to create a new ETF"""
        return render_template(template_name_or_list="etf/create.html")

    def store(self):
        """Save a new ETF to database"""
        ticker = request.form.get("ticker")
        self.logger.info(f"Attempting to create new ETF with ticker: {ticker}")

        try:
            # Create DTO from form data with validation
            etf_dto: ETF = ETF(
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
            self.logger.info(f"ETF {etf_dto.ticker} created successfully")
            flash(message=f"ETF {etf_dto.ticker} creato con successo!", category="success")

        except ValidationError as e:
            # Handle Pydantic validation errors
            errors = "; ".join([f"{err['loc'][0]}: {err['msg']}" for err in e.errors()])
            self.logger.warning(f"Validation error creating ETF {ticker}: {errors}")
            flash(message=f"Errori di validazione: {errors}", category="danger")
        except SQLAlchemyError as e:
            # Handle database errors (from context manager)
            self.logger.error(f"Database error creating ETF {ticker}: {str(e)}")
            flash(message=f"Errore database: {str(e)}", category="danger")
        except ValueError as e:
            # Handle business logic errors
            self.logger.warning(f"Business logic error creating ETF {ticker}: {str(e)}")
            flash(message=f"Errore: {str(e)}", category="danger")
        except Exception as e:
            # Catch-all for unexpected errors
            self.logger.exception(f"Unexpected error creating ETF {ticker}: {str(e)}")
            flash(message=f"Errore imprevisto: {str(e)}", category="danger")

        return redirect(location=url_for(endpoint="etf.index"))

    def edit(self, ticker):
        """Display form to edit an ETF"""
        self.logger.info(f"Fetching ETF {ticker} for editing")
        etf: ETF | None = self.etf_service.get_by_ticker(ticker)
        if not etf:
            self.logger.warning(f"ETF {ticker} not found for editing")
            flash(message="ETF non trovato", category="danger")
            return redirect(location=url_for(endpoint="etf.index"))
        return render_template(template_name_or_list="etf/edit.html", etf=etf)

    def update(self, ticker):
        """Update an existing ETF"""
        self.logger.info(f"Attempting to update ETF {ticker}")
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
            self.logger.info(f"ETF {ticker} updated successfully")
            flash(f"ETF {ticker} aggiornato con successo!", "success")

        except ValidationError as e:
            errors = "; ".join([f"{err['loc'][0]}: {err['msg']}" for err in e.errors()])
            self.logger.warning(f"Validation error updating ETF {ticker}: {errors}")
            flash(f"Errori di validazione: {errors}", "danger")
        except SQLAlchemyError as e:
            self.logger.error(f"Database error updating ETF {ticker}: {str(e)}")
            flash(f"Errore database: {str(e)}", "danger")
        except ValueError as e:
            self.logger.warning(f"Business logic error updating ETF {ticker}: {str(e)}")
            flash(f"Errore: {str(e)}", "danger")
        except Exception as e:
            self.logger.exception(f"Unexpected error updating ETF {ticker}: {str(e)}")
            flash(f"Errore imprevisto: {str(e)}", "danger")

        return redirect(url_for("etf.index"))

    def delete(self, ticker):
        """Delete an ETF"""
        self.logger.info(f"Attempting to delete ETF {ticker}")
        try:
            self.etf_service.delete(ticker)
            self.logger.info(f"ETF {ticker} deleted successfully")
            flash(f"ETF {ticker} eliminato con successo!", "success")
        except SQLAlchemyError as e:
            self.logger.error(f"Database error deleting ETF {ticker}: {str(e)}")
            flash(f"Errore database: {str(e)}", "danger")
        except ValueError as e:
            self.logger.warning(f"ETF {ticker} not found for deletion")
            flash(f"Errore: {str(e)}", "danger")
        except Exception as e:
            self.logger.exception(f"Unexpected error deleting ETF {ticker}: {str(e)}")
            flash(f"Errore imprevisto: {str(e)}", "danger")

        return redirect(url_for("etf.index"))

    def show(self, ticker):
        """Display ETF details"""
        self.logger.info(f"Fetching ETF {ticker} details")
        etf: ETF | None = self.etf_service.get_by_ticker(ticker)
        if not etf:
            self.logger.warning(f"ETF {ticker} not found")
            flash(message=f"ETF {ticker} non trovato!", category="danger")
            return redirect(location=url_for("etf.index"))

        return render_template(template_name_or_list="etf/show.html", etf=etf)
