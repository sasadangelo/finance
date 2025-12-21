# -----------------------------------------------------------------------------
# Copyright (c) 2025 Salvatore D'Angelo, Code4Projects
# Licensed under the MIT License. See LICENSE.md for details.
# -----------------------------------------------------------------------------
from app_types import ApplicationContainer
from controllers.types import WebResponse
from typing import cast
from flask import Blueprint, current_app

# Create a Blueprint for Index routes
index_bp: Blueprint = Blueprint(name="index", import_name=__name__)

# Type hint per current_app
app: ApplicationContainer = cast(ApplicationContainer, current_app)


# Route to display all indices
@index_bp.route(rule="/indices")
def index() -> WebResponse:
    return app.index_controller.index()


# Route to show the creation form
@index_bp.route(rule="/indices/create")
def create() -> WebResponse:
    return app.index_controller.create()


# Route to save a new index
@index_bp.route(rule="/indices/store", methods=["POST"])
def store() -> WebResponse:
    return app.index_controller.store()


# Route to show index details
@index_bp.route(rule="/indices/<string:ticker>")
def show(ticker) -> WebResponse:
    return app.index_controller.show(ticker)


# Route to show the edit form
@index_bp.route(rule="/indices/<string:ticker>/edit")
def edit(ticker) -> WebResponse:
    return app.index_controller.edit(ticker)


# Route to update an index
@index_bp.route(rule="/indices/<string:ticker>/update", methods=["POST"])
def update(ticker) -> WebResponse:
    return app.index_controller.update(ticker)


# Route to delete an index
@index_bp.route(rule="/indices/<string:ticker>/delete", methods=["POST"])
def delete(ticker) -> WebResponse:
    return app.index_controller.delete(ticker)


# Made with Bob
