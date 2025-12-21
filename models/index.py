# -----------------------------------------------------------------------------
# Copyright (c) 2025 Salvatore D'Angelo, Code4Projects
# Licensed under the MIT License. See LICENSE.md for details.
# -----------------------------------------------------------------------------
from core.database import db


class IndexDAO(db.Model):
    """Index Model - represents a market index in the database"""

    __tablename__ = "indices"

    # Required fields (NOT NULL)
    ticker = db.Column(db.String(10), primary_key=True)
    name = db.Column(db.String(200), nullable=False)

    def __repr__(self):
        return f"<IndexDAO {self.ticker}: {self.name}>"


# Made with Bob
