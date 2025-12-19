# -----------------------------------------------------------------------------
# Copyright (c) 2025 Salvatore D'Angelo, Code4Projects
# Licensed under the MIT License. See LICENSE.md for details.
# -----------------------------------------------------------------------------
from flask import Flask
from pathlib import Path
from core.database import db
from core.config import get_settings
from bootstrap import init_app
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Get project directory
project_dir = Path(__file__).parent

# Load settings (from .env + config.yml)
settings = get_settings()

app = Flask(__name__)
app.config["SECRET_KEY"] = settings.app.secret_key
app.config["SQLALCHEMY_DATABASE_URI"] = settings.database.get_absolute_uri(project_dir)
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = settings.database.track_modifications

# Initialize db with app
db.init_app(app)

# Initialize application (services and controllers)
init_app(app, db)

# Import and register blueprints
with app.app_context():
    from routes.etf_routes import etf_bp

    app.register_blueprint(etf_bp)

if __name__ == "__main__":
    app.run(debug=settings.app.debug, host=settings.app.host, port=settings.app.port)

# Made with Bob
