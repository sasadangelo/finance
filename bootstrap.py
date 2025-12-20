# -----------------------------------------------------------------------------
# Copyright (c) 2025 Salvatore D'Angelo, Code4Projects
# Licensed under the MIT License. See LICENSE.md for details.
# -----------------------------------------------------------------------------
"""
Application bootstrap module.
Handles initialization of services and controllers using the init_app pattern.
"""
from core.database import DatabaseManager
from controllers import QuoteController, EtfController
from services import EtfService, QuoteService


def init_app(app, db):
    """
    Initialize application with all services and controllers.

    This function follows the Flask extension pattern (init_app),
    allowing for flexible application factory setup.

    Args:
        app: Flask application instance
        db: SQLAlchemy database instance

    Returns:
        None (modifies app in place by adding attributes)
    """
    # Initialize DatabaseManager
    db_manager: DatabaseManager = DatabaseManager(db)

    # Initialize Services (Domain Services first, then Application Services)
    quote_service: QuoteService = QuoteService(db_manager)
    etf_service: EtfService = EtfService(db_manager, quote_service)

    # Initialize Controllers (Presentation Layer)
    etf_controller: EtfController = EtfController(etf_service)
    quote_controller: QuoteController = QuoteController(quote_service, etf_service)

    # Attach controllers to app instance
    # This allows access via current_app.etf_controller and current_app.quote_controller in routes
    app.etf_controller = etf_controller
    app.quote_controller = quote_controller
