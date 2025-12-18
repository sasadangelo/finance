import os
from database import db
from flask import Flask

# SqlAlchemy Database Configuration With SqlLite
project_dir = os.path.dirname(os.path.abspath(__file__))
database_file = "sqlite:///{}".format(os.path.join(project_dir, "database/etfs.db"))

app = Flask(__name__)
app.secret_key = "Secret Key"
app.config["SQLALCHEMY_DATABASE_URI"] = database_file
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

# Initialize db with app
db.init_app(app)

# Import routes after app and db initialization
with app.app_context():
    import etfs_routes

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)
