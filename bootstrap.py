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
from controllers.index_controller import IndexController
from services import EtfService, QuoteService
from services.index_service import IndexService


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
    index_service: IndexService = IndexService(db_manager)

    # Initialize Controllers (Presentation Layer)
    etf_controller: EtfController = EtfController(etf_service, index_service)
    quote_controller: QuoteController = QuoteController(quote_service, etf_service)
    index_controller: IndexController = IndexController(index_service)

    # Attach controllers to app instance
    # This allows access via current_app in routes
    app.etf_controller = etf_controller
    app.quote_controller = quote_controller
    app.index_controller = index_controller
