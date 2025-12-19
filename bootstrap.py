# -----------------------------------------------------------------------------
# Copyright (c) 2025 Salvatore D'Angelo, Code4Projects
# Licensed under the MIT License. See LICENSE.md for details.
# -----------------------------------------------------------------------------
"""
Application bootstrap module.
Handles initialization of services and controllers using the init_app pattern.
"""
from core.database import DatabaseManager
from services import EtfService
from controllers import EtfController


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
    db_manager = DatabaseManager(db)

    # Initialize Services
    etf_service = EtfService(db_manager)

    # Initialize Controllers
    etf_controller = EtfController(etf_service)

    # Attach controllers to app instance
    # This allows access via current_app.etf_controller in routes
    app.etf_controller = etf_controller
