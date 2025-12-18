# -----------------------------------------------------------------------------
# Copyright (c) 2025 Salvatore D'Angelo, Code4Projects
# Licensed under the MIT License. See LICENSE.md for details.
# -----------------------------------------------------------------------------
from database import db


class Etf(db.Model):
    """ETF Model - represents an ETF in the database"""

    __tablename__ = "etfs"

    # Required fields (NOT NULL)
    ticker = db.Column(db.String(10), primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    isin = db.Column(db.String(15), nullable=False)
    launchDate = db.Column(db.String(20), nullable=False)
    currency = db.Column(db.String(10), nullable=False)
    dividendType = db.Column(db.String(20), nullable=False)

    # Optional fields (can be NULL)
    dividendFrequency = db.Column(db.Integer)
    yeld = db.Column(db.Float)
    capital = db.Column(db.Float)
    replication = db.Column(db.String(30))
    volatility = db.Column(db.Float)

    def __init__(
        self,
        ticker: str,
        name: str,
        isin: str,
        launchDate: str,
        currency: str,
        dividendType: str,
        dividendFrequency: int | None = None,
        yeld: float | None = None,
        capital: float | None = None,
        replication: str | None = None,
        volatility: float | None = None,
    ):
        self.ticker = ticker
        self.name = name
        self.isin = isin
        self.launchDate = launchDate
        self.currency = currency
        self.dividendType = dividendType
        self.dividendFrequency = dividendFrequency
        self.yeld = yeld
        self.capital = capital
        self.replication = replication
        self.volatility = volatility

    def to_dict(self):
        """Convert ETF object to dictionary"""
        return {
            "ticker": self.ticker,
            "name": self.name,
            "isin": self.isin,
            "launchDate": self.launchDate,
            "capital": self.capital,
            "replication": self.replication,
            "volatility": self.volatility,
            "currency": self.currency,
            "dividendType": self.dividendType,
            "dividendFrequency": self.dividendFrequency,
            "yeld": self.yeld,
        }

    def __repr__(self):
        return f"<ETF {self.ticker}: {self.name}>"


# Made with Bob
