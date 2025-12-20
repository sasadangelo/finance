# -----------------------------------------------------------------------------
# Copyright (c) 2025 Salvatore D'Angelo, Code4Projects
# Licensed under the MIT License. See LICENSE.md for details.
# -----------------------------------------------------------------------------
from app_types import ApplicationContainer
from controllers.types import WebResponse, APIResponse
from flask.wrappers import Response
from typing import cast
from flask import Blueprint, current_app

# Create a Blueprint for ETF routes
etf_bp: Blueprint = Blueprint(name="etf", import_name=__name__)

# Type hint per current_app
app: ApplicationContainer = cast(ApplicationContainer, current_app)


# Route to display all ETFs
@etf_bp.route(rule="/")
@etf_bp.route(rule="/etfs")
def index() -> WebResponse:
    return app.etf_controller.index()


# Route to show the creation form
@etf_bp.route(rule="/etfs/create")
def create() -> WebResponse:
    return app.etf_controller.create()


# Route to save a new ETF
@etf_bp.route(rule="/etfs/store", methods=["POST"])
def store() -> WebResponse:
    return app.etf_controller.store()


# Route to show ETF details
@etf_bp.route(rule="/etfs/<string:ticker>")
def show(ticker) -> WebResponse:
    return app.etf_controller.show(ticker)


# Route to show the edit form
@etf_bp.route(rule="/etfs/<string:ticker>/edit")
def edit(ticker) -> WebResponse:
    return app.etf_controller.edit(ticker)


# Route to update an ETF
@etf_bp.route(rule="/etfs/<string:ticker>/update", methods=["POST"])
def update(ticker) -> WebResponse:
    return app.etf_controller.update(ticker)


# Route to delete an ETF
@etf_bp.route(rule="/etfs/<string:ticker>/delete", methods=["POST"])
def delete(ticker) -> WebResponse:
    return app.etf_controller.delete(ticker)


# Route to get quote data (JSON API)
@etf_bp.route(rule="/etfs/<string:ticker>/quotes")
def get_quotes(ticker) -> APIResponse:
    return app.quote_controller.get_quotes(ticker)


# Route to update quotes for a single ETF
@etf_bp.route(rule="/etfs/<string:ticker>/quotes/update", methods=["POST"])
def update_quotes_single(ticker) -> APIResponse:
    return app.quote_controller.update_single(ticker)


# Route to update quotes for all ETFs with SSE (Server-Sent Events)
@etf_bp.route(rule="/etfs/quotes/update_all")
def update_quotes_all() -> Response:
    return app.quote_controller.update_all()
