# -----------------------------------------------------------------------------
# Copyright (c) 2025 Salvatore D'Angelo, Code4Projects
# Licensed under the MIT License. See LICENSE.md for details.
# -----------------------------------------------------------------------------
from models.index import IndexDAO
from core.database import DatabaseManager
from core.log import LoggerManager
from dto.index import Index
from mappers.index_mapper import IndexMapper


class IndexService:
    """Application Service for Index management"""

    def __init__(self, db_manager: DatabaseManager) -> None:
        """
        Initialize IndexService with dependencies

        Args:
            db_manager: DatabaseManager instance for session handling
        """
        self.db_manager = db_manager
        self.logger = LoggerManager.get_logger(name=self.__class__.__name__)
        self.logger.info("IndexService initialized")

    def get_all(self) -> list[Index]:
        """
        Retrieve all indices from database

        Returns:
            List of Index DTOs
        """
        self.logger.debug("Fetching all indices from database")
        index_daos: list[IndexDAO] = IndexDAO.query.all()
        self.logger.info(f"Retrieved {len(index_daos)} indices from database")
        return [IndexMapper.to_dto(dao) for dao in index_daos]

    def get_by_ticker(self, ticker: str) -> Index | None:
        """
        Retrieve a specific index by ticker

        Args:
            ticker: Index ticker symbol

        Returns:
            Index DTO if found, None otherwise
        """
        self.logger.debug(f"Fetching index with ticker: {ticker}")
        index_dao: IndexDAO | None = IndexDAO.query.get(ident=ticker)
        if index_dao:
            self.logger.debug(f"Index {ticker} found in database")
            return IndexMapper.to_dto(dao=index_dao)
        else:
            self.logger.debug(f"Index {ticker} not found in database")
            return None

    def create(self, index_dto: Index) -> None:
        """
        Create a new index

        Args:
            index_dto: Index DTO with validated data

        Raises:
            SQLAlchemyError: On database errors
        """
        self.logger.info(f"Creating new index: {index_dto.ticker}")
        with self.db_manager.get_session() as session:
            index_dao: IndexDAO = IndexMapper.to_dao(index_dto)
            session.add(instance=index_dao)
            self.logger.info(f"Index {index_dto.ticker} created successfully in database")

    def update(self, index_dto: Index) -> None:
        """
        Update an existing index

        Args:
            index_dto: Index DTO with new validated data (ticker identifies the record)

        Raises:
            ValueError: If index not found
            SQLAlchemyError: On database errors
        """
        self.logger.info(f"Updating index: {index_dto.ticker}")
        with self.db_manager.get_session():
            index_dao: IndexDAO | None = IndexDAO.query.get(ident=index_dto.ticker)
            if not index_dao:
                self.logger.error(f"Index {index_dto.ticker} not found for update")
                raise ValueError(f"Index {index_dto.ticker} not found")

            # Update DAO using mapper
            IndexMapper.to_dao(index_dto, dao=index_dao)
            self.logger.info(f"Index {index_dto.ticker} updated successfully in database")

    def delete(self, ticker: str) -> None:
        """
        Delete an index

        Args:
            ticker: Ticker of the index to delete

        Raises:
            ValueError: If index not found
            SQLAlchemyError: On database errors
        """
        self.logger.info(f"Deleting index: {ticker}")
        with self.db_manager.get_session() as session:
            index_dao: IndexDAO | None = IndexDAO.query.get(ticker)
            if not index_dao:
                self.logger.error(f"Index {ticker} not found for deletion")
                raise ValueError(f"Index {ticker} not found")

            session.delete(instance=index_dao)
            self.logger.info(f"Index {ticker} deleted successfully from database")

    def exists(self, ticker: str) -> bool:
        """
        Check if an index exists

        Args:
            ticker: Index ticker symbol

        Returns:
            True if exists, False otherwise
        """
        exists: bool = IndexDAO.query.get(ident=ticker) is not None
        self.logger.debug(f"Index {ticker} exists: {exists}")
        return exists


# Made with Bob
