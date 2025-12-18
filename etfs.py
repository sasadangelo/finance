# -----------------------------------------------------------------------------
# Copyright (c) 2025 Salvatore D'Angelo, Code4Projects
# Licensed under the MIT License. See LICENSE.md for details.
# -----------------------------------------------------------------------------
from database import db


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

    def __init__(
        self,
        ticker,
        name,
        isin,
        launchDate,
        capital,
        replication,
        volatility,
        currency,
        dividend,
        dividendFrequency,
        yeld,
    ):
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
