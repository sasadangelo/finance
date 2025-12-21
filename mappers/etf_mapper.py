# -----------------------------------------------------------------------------
# Copyright (c) 2025 Salvatore D'Angelo, Code4Projects
# Licensed under the MIT License. See LICENSE.md for details.
# -----------------------------------------------------------------------------
from models.etf import EtfDAO
from dto.etf import ETF


class EtfMapper:
    """Mapper class for converting between ETF DTO and DAO"""

    @staticmethod
    def to_dao(etf_dto: ETF, dao: EtfDAO | None = None) -> EtfDAO:
        """
        Convert ETF DTO to DAO

        Args:
            etf_dto: ETF DTO to convert
            dao: Optional existing DAO to update (for update operations)

        Returns:
            EtfDAO instance
        """
        if dao is None:
            dao = EtfDAO()

        # Map all fields from DTO to DAO
        dao.ticker = etf_dto.ticker
        dao.name = etf_dto.name
        dao.isin = etf_dto.isin
        dao.launchDate = etf_dto.launchDate
        dao.capital = etf_dto.capital
        dao.replication = etf_dto.replication
        dao.volatility = etf_dto.volatility
        dao.currency = etf_dto.currency
        dao.dividendType = etf_dto.dividendType
        dao.dividendFrequency = etf_dto.dividendFrequency
        dao.yeld = etf_dto.yeld
        dao.assetType = etf_dto.assetType.value if etf_dto.assetType else None
        dao.indexTicker = etf_dto.indexTicker

        return dao

    @staticmethod
    def to_dto(dao: EtfDAO) -> ETF:
        """
        Convert ETF DAO to DTO

        Args:
            dao: EtfDAO to convert

        Returns:
            ETF DTO instance
        """
        # Use Pydantic's model_validate to create DTO from DAO
        # This leverages Pydantic's from_attributes=True configuration
        return ETF.model_validate(dao)
