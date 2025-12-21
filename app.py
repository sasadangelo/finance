# -----------------------------------------------------------------------------
# Copyright (c) 2025 Salvatore D'Angelo, Code4Projects
# Licensed under the MIT License. See LICENSE.md for details.
# -----------------------------------------------------------------------------
from __future__ import annotations
from flask.app import Flask
from pathlib import Path
from core.database import db
from core.config import Settings, get_settings
from core.log import setup_logging, LoggerManager
from bootstrap import init_app
from dotenv import load_dotenv
from routes.etf_routes import etf_bp
from routes.index_routes import index_bp
import atexit

# Load environment variables from .env file
load_dotenv()

# Get project directory
project_dir: Path = Path(__file__).parent

# Load settings (from .env + config.yml)
settings: Settings = get_settings()

# Initialize logging
setup_logging(
    level=settings.log.level,
    console=settings.log.console,
    file=settings.log.file,
    rotation=settings.log.rotation,
    retention=settings.log.retention,
    compression=settings.log.compression,
)

logger = LoggerManager.get_logger(name="App")

app: Flask = Flask(import_name=__name__)
app.config["SECRET_KEY"] = settings.app.secret_key
app.config["SQLALCHEMY_DATABASE_URI"] = settings.database.get_absolute_uri(project_dir)
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

# Initialize db with app
db.init_app(app)

# Initialize application (services, controllers, and cron jobs)
# Import and register blueprints
# Start cron job
with app.app_context():

    init_app(app, db)
    app.register_blueprint(blueprint=etf_bp)
    app.register_blueprint(blueprint=index_bp)
    logger.info("Starting UpdateQuotesCronJob...")
    app.update_quotes_cronjob.run()  # type: ignore[attr-defined]

# Register cleanup function to stop cron job on exit
def cleanup() -> None:
    """Stop cron job when application exits"""
    if hasattr(app, "update_quotes_cronjob"):
        logger.info("Stopping UpdateQuotesCronJob...")
        app.update_quotes_cronjob.stop()  # type: ignore[attr-defined]


atexit.register(cleanup)

if __name__ == "__main__":
    try:
        app.run(debug=settings.app.debug, host=settings.app.host, port=settings.app.port)
    except KeyboardInterrupt:
        logger.info("Application stopped by user (Ctrl+C)")
    finally:
        cleanup()
