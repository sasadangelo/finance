# -----------------------------------------------------------------------------
# Copyright (c) 2025 Salvatore D'Angelo, Code4Projects
# Licensed under the MIT License. See LICENSE.md for details.
# -----------------------------------------------------------------------------
from database import db


class Etf(db.Model):
    """ETF Model - rappresenta un ETF nel database"""

    __tablename__ = "etfs"

    ticker = db.Column(db.String(10), primary_key=True)
    name = db.Column(db.String(50), nullable=False)
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
        isin=None,
        launchDate=None,
        capital=None,
        replication=None,
        volatility=None,
        currency=None,
        dividend=None,
        dividendFrequency=None,
        yeld=None,
    ):
        self.ticker = ticker
        self.name = name
        self.isin = isin
        self.launchDate = launchDate
        self.capital = capital
        self.replication = replication
        self.volatility = volatility
        self.currency = currency
        self.dividend = dividend
        self.dividendFrequency = dividendFrequency
        self.yeld = yeld

    def to_dict(self):
        """Converte l'oggetto ETF in un dizionario"""
        return {
            "ticker": self.ticker,
            "name": self.name,
            "isin": self.isin,
            "launchDate": self.launchDate,
            "capital": self.capital,
            "replication": self.replication,
            "volatility": self.volatility,
            "currency": self.currency,
            "dividend": self.dividend,
            "dividendFrequency": self.dividendFrequency,
            "yeld": self.yeld,
        }

    def __repr__(self):
        return f"<ETF {self.ticker}: {self.name}>"


# Made with Bob
