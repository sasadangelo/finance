# -----------------------------------------------------------------------------
# Copyright (c) 2025 Salvatore D'Angelo, Code4Projects
# Licensed under the MIT License. See LICENSE.md for details.
# -----------------------------------------------------------------------------
from enum import Enum


class ETFReplicationType(str, Enum):
    """
    Enumeration for ETF replication types
    """

    FISICA_TOTALE = "Fisica (Replica totale)"
    FISICA_CAMPIONAMENTO = "Fisica (Campionamento)"
    SINTETICA = "Sintetica"
    IBRIDA = "Ibrida"

    @classmethod
    def get_display_name(cls, value: str) -> str:
        """Get display name for a replication type value"""
        try:
            return cls(value).value
        except ValueError:
            return value

    @classmethod
    def get_all_values(cls) -> list[str]:
        """Get all replication type values"""
        return [member.value for member in cls]


# Made with Bob
