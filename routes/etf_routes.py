# -----------------------------------------------------------------------------
# Copyright (c) 2025 Salvatore D'Angelo, Code4Projects
# Licensed under the MIT License. See LICENSE.md for details.
# -----------------------------------------------------------------------------
from flask import Blueprint
from controllers import EtfController

# Create a Blueprint for ETF routes
etf_bp = Blueprint("etf", __name__)


# Route to display all ETFs
@etf_bp.route("/")
@etf_bp.route("/etfs")
def index():
    return EtfController.index()


# Route to show the creation form
@etf_bp.route("/etfs/create")
def create():
    return EtfController.create()


# Route to save a new ETF
@etf_bp.route("/etfs/store", methods=["POST"])
def store():
    return EtfController.store()


# Route to show ETF details
@etf_bp.route("/etfs/<string:ticker>")
def show(ticker):
    return EtfController.show(ticker)


# Route to show the edit form
@etf_bp.route("/etfs/<string:ticker>/edit")
def edit(ticker):
    return EtfController.edit(ticker)


# Route to update an ETF
@etf_bp.route("/etfs/<string:ticker>/update", methods=["POST"])
def update(ticker):
    return EtfController.update(ticker)


# Route to delete an ETF
@etf_bp.route("/etfs/<string:ticker>/delete", methods=["POST"])
def delete(ticker):
    return EtfController.delete(ticker)


# Route to get quote data (JSON API)
@etf_bp.route("/etfs/<string:ticker>/quotes")
def get_quotes(ticker):
    return EtfController.get_quotes(ticker)
