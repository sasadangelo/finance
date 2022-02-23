import os
from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy

 
#SqlAlchemy Database Configuration With Mysql
project_dir = os.path.dirname(os.path.abspath(__file__))
database_file = "sqlite:///{}".format(os.path.join(project_dir, "../database/etfs.db"))
print(database_file)

app = Flask(__name__)
app.secret_key = "Secret Key"
app.config["SQLALCHEMY_DATABASE_URI"] = database_file 

db = SQLAlchemy(app)

# Creating model table for our CRUD database
class Etf(db.Model):
   __tablename__ = "etfs"
   ticker = db.Column(db.String(10), primary_key=True)
   name = db.Column(db.String(50))
   isin = db.Column(db.String(15))
   launchDate = db.Column(db.String(20))
   capital = db.Column(db.Float)
   replication = db.Column(db.String(30))
   volatility = db.Column(db.Float)
   currency = db.Column(db.String(10))
   dividend = db.Column(db.String(20))
   dividendFrequency = db.Column(db.Integer)
   yeld = db.Column(db.Float)

   def __init__(self, ticker, name, isin, launchDate, 
                      capital, replication, volatility,
                      currency, dividend, dividendFrequency, 
                      yeld):
       self.ticker = ticker
       self.name = name
       self.isin = isin
       self.launchDate = launchDate
       self.capital = capital
       self.replication = replication
       self.currency = currency
       self.dividend = dividend
       self.dividendFrequency = dividendFrequency
       self.yeld = yeld

@app.route('/')
def Index():
    all_etfs = Etf.query.all()
    print(all_etfs)
    return render_template("index.html", etfs = all_etfs)
