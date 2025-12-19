# -----------------------------------------------------------------------------
# Copyright (c) 2025 Salvatore D'Angelo, Code4Projects
# Licensed under the MIT License. See LICENSE.md for details.
# -----------------------------------------------------------------------------
import os
from flask import Flask
from core.database import db
from bootstrap import init_app

# SqlAlchemy Database Configuration With SqlLite
project_dir = os.path.dirname(os.path.abspath(__file__))
database_file = "sqlite:///{}".format(os.path.join(project_dir, "database/etfs.db"))

app = Flask(__name__)
app.secret_key = "Secret Key"
app.config["SQLALCHEMY_DATABASE_URI"] = database_file
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

# Initialize db with app
db.init_app(app)

# Initialize application (services and controllers)
init_app(app, db)

# Import and register blueprints
with app.app_context():
    from routes.etf_routes import etf_bp

    app.register_blueprint(etf_bp)

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5001)
