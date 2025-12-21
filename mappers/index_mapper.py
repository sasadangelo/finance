# -----------------------------------------------------------------------------
# Copyright (c) 2025 Salvatore D'Angelo, Code4Projects
# Licensed under the MIT License. See LICENSE.md for details.
# -----------------------------------------------------------------------------
from models.index import IndexDAO
from dto.index import Index


class IndexMapper:
    """Mapper class for converting between Index DTO and DAO"""

    @staticmethod
    def to_dao(index_dto: Index, dao: IndexDAO | None = None) -> IndexDAO:
        """
        Convert Index DTO to DAO

        Args:
            index_dto: Index DTO to convert
            dao: Optional existing DAO to update (for update operations)

        Returns:
            IndexDAO instance
        """
        if dao is None:
            dao = IndexDAO()

        # Map all fields from DTO to DAO
        dao.ticker = index_dto.ticker
        dao.name = index_dto.name

        return dao

    @staticmethod
    def to_dto(dao: IndexDAO) -> Index:
        """
        Convert Index DAO to DTO

        Args:
            dao: IndexDAO to convert

        Returns:
            Index DTO instance
        """
        # Use Pydantic's model_validate to create DTO from DAO
        # This leverages Pydantic's from_attributes=True configuration
        return Index.model_validate(dao)


# Made with Bob
