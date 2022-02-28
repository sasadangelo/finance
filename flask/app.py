import os
from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
 
# SqlAlchemy Database Configuration With SqlLite
project_dir = os.path.dirname(os.path.abspath(__file__))
database_file = "sqlite:///{}".format(os.path.join(project_dir, "../database/etfs.db"))

app = Flask(__name__)
app.secret_key = "Secret Key"
app.config["SQLALCHEMY_DATABASE_URI"] = database_file 

db = SQLAlchemy(app)

import etfs
import etfs_routes
