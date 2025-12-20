# -----------------------------------------------------------------------------
# Copyright (c) 2025 Salvatore D'Angelo, Code4Projects
# Licensed under the MIT License. See LICENSE.md for details.
# -----------------------------------------------------------------------------
from typing import cast
from flask import Blueprint, current_app
from core import ApplicationContainer

# Create a Blueprint for ETF routes
etf_bp = Blueprint("etf", __name__)

# Type hint per current_app
app = cast(ApplicationContainer, current_app)


# Route to display all ETFs
@etf_bp.route("/")
@etf_bp.route("/etfs")
def index():
    return app.etf_controller.index()


# Route to show the creation form
@etf_bp.route("/etfs/create")
def create():
    return app.etf_controller.create()


# Route to save a new ETF
@etf_bp.route("/etfs/store", methods=["POST"])
def store():
    return app.etf_controller.store()


# Route to show ETF details
@etf_bp.route("/etfs/<string:ticker>")
def show(ticker):
    return app.etf_controller.show(ticker)


# Route to show the edit form
@etf_bp.route("/etfs/<string:ticker>/edit")
def edit(ticker):
    return app.etf_controller.edit(ticker)


# Route to update an ETF
@etf_bp.route("/etfs/<string:ticker>/update", methods=["POST"])
def update(ticker):
    return app.etf_controller.update(ticker)


# Route to delete an ETF
@etf_bp.route("/etfs/<string:ticker>/delete", methods=["POST"])
def delete(ticker):
    return app.etf_controller.delete(ticker)


# Route to get quote data (JSON API)
@etf_bp.route("/etfs/<string:ticker>/quotes")
def get_quotes(ticker):
    return app.quote_controller.get_quotes(ticker)


# Route to update quotes for a single ETF
@etf_bp.route("/etfs/<string:ticker>/quotes/update", methods=["POST"])
def update_quotes_single(ticker):
    return app.quote_controller.update_single(ticker)


# Route to update quotes for all ETFs
# @etf_bp.route("/etfs/quotes/update-all", methods=["POST"])
# def update_quotes_all():
#     return app.quote_controller.update_all()


# Route to update quotes for all ETFs with SSE (Server-Sent Events)
@etf_bp.route("/etfs/quotes/update-all-stream")
def update_quotes_all_stream():
    return app.quote_controller.update_all_stream()
