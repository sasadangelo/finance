# -----------------------------------------------------------------------------
# Copyright (c) 2025 Salvatore D'Angelo, Code4Projects
# Licensed under the MIT License. See LICENSE.md for details.
# -----------------------------------------------------------------------------
from flask.app import Flask
from pathlib import Path
from core.database import db
from core.config import Settings, get_settings
from core.log import setup_logging
from bootstrap import init_app
from dotenv import load_dotenv

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

app: Flask = Flask(import_name=__name__)
app.config["SECRET_KEY"] = settings.app.secret_key
app.config["SQLALCHEMY_DATABASE_URI"] = settings.database.get_absolute_uri(project_dir)
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

# Initialize db with app
db.init_app(app)

# Initialize application (services and controllers)
init_app(app, db)

# Import and register blueprints
with app.app_context():
    from routes.etf_routes import etf_bp
    from routes.index_routes import index_bp

    app.register_blueprint(blueprint=etf_bp)
    app.register_blueprint(blueprint=index_bp)

if __name__ == "__main__":
    app.run(debug=settings.app.debug, host=settings.app.host, port=settings.app.port)
