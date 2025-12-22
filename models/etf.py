# -----------------------------------------------------------------------------
# Copyright (c) 2025 Salvatore D'Angelo, Code4Projects
# Licensed under the MIT License. See LICENSE.md for details.
# -----------------------------------------------------------------------------
from core.database import db


class EtfDAO(db.Model):
    """ETF Model - represents an ETF in the database"""

    __tablename__ = "etfs"

    # Required fields (NOT NULL)
    ticker = db.Column(db.String(10), primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    isin = db.Column(db.String(15), nullable=False)
    launchDate = db.Column(db.String(10), nullable=False)  # YYYY-MM-DD format
    currency = db.Column(db.String(3), nullable=False)  # USD, EUR
    dividendType = db.Column(db.String(20), nullable=False)

    # Optional fields (can be NULL)
    assetType = db.Column(db.String(30))
    dividendFrequency = db.Column(db.Integer)
    yeld = db.Column(db.Float)
    capital = db.Column(db.Float)
    replication = db.Column(db.String(30))  # Stores enum value
    volatility = db.Column(db.Float)
    indexTicker = db.Column(db.String(10), db.ForeignKey("indices.ticker"), nullable=True)

    # Relationship to Index
    index = db.relationship("IndexDAO", backref="etfs", lazy=True)

    def __repr__(self):
        return f"<EtfDAO {self.ticker}: {self.name}>"
