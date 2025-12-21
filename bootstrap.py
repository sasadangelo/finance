# -----------------------------------------------------------------------------
# Copyright (c) 2025 Salvatore D'Angelo, Code4Projects
# Licensed under the MIT License. See LICENSE.md for details.
# -----------------------------------------------------------------------------
"""
Application bootstrap module.
Handles initialization of services, controllers, and cron jobs using the init_app pattern.
"""
from core.database import DatabaseManager
from controllers import QuoteController, EtfController, IndexController
from services import EtfService, QuoteService, UpdateQuotesCronJob, IndexService


def init_app(app, db) -> None:
    """
    Initialize application with all services, controllers, and cron jobs.

    This function follows the Flask extension pattern (init_app),
    allowing for flexible application factory setup.

    Args:
        app: Flask application instance
        db: SQLAlchemy database instance

    Returns:
        None (modifies app in place by adding attributes)
    """
    # Initialize DatabaseManager
    db_manager: DatabaseManager = DatabaseManager(db_instance=db)

    # Initialize Services (Domain Services first, then Application Services)
    quote_service: QuoteService = QuoteService(db_manager)
    etf_service: EtfService = EtfService(db_manager, quote_service)
    index_service: IndexService = IndexService(db_manager)

    # Initialize Controllers (Presentation Layer)
    etf_controller: EtfController = EtfController(etf_service, index_service)
    quote_controller: QuoteController = QuoteController(quote_service, etf_service)
    index_controller: IndexController = IndexController(index_service)

    # Initialize Cron Jobs (pass app for context)
    update_quotes_cronjob: UpdateQuotesCronJob = UpdateQuotesCronJob(db_manager, app)

    # Attach controllers to app instance
    # This allows access via current_app in routes
    app.etf_controller = etf_controller
    app.quote_controller = quote_controller
    app.index_controller = index_controller

    # Attach cron job to app instance
    app.update_quotes_cronjob = update_quotes_cronjob
