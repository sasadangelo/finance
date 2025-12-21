# -----------------------------------------------------------------------------
# Copyright (c) 2025 Salvatore D'Angelo, Code4Projects
# Licensed under the MIT License. See LICENSE.md for details.
# -----------------------------------------------------------------------------
from core.database import db


class QuoteDAO(db.Model):
    """SQLAlchemy model for ETF quotes"""

    __tablename__ = "quotes"

    Ticker = db.Column(
        db.String(10),
        db.ForeignKey("etfs.ticker", ondelete="CASCADE"),
        primary_key=True,
        nullable=False,
    )
    Date = db.Column(db.String(20), primary_key=True, nullable=False)
    Open = db.Column(db.Float)
    High = db.Column(db.Float)
    Low = db.Column(db.Float)
    Close = db.Column(db.Float, nullable=False)
    Adj_Close = db.Column(db.Float)
    Volume = db.Column(db.Integer)

    def __repr__(self):
        return f"<QuoteDAO {self.Ticker} {self.Date}: {self.Close}>"
