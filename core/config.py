# -----------------------------------------------------------------------------
# Copyright (c) 2025 Salvatore D'Angelo, Code4Projects
# Licensed under the MIT License. See LICENSE.md for details.
# -----------------------------------------------------------------------------
"""
Configuration management using Pydantic Settings.
Loads configuration from config.yml file only.
Only SECRET_KEY is loaded from environment variable.
"""
from pydantic_settings import BaseSettings
from pydantic import Field
import yaml
from pathlib import Path
from functools import lru_cache
import os


class DatabaseConfig(BaseSettings):
    """Database configuration"""

    relative_path: str = Field(default="database/etfs.db", description="Database relative path")

    def get_absolute_uri(self, project_dir: Path) -> str:
        """
        Convert relative database path to absolute SQLite URI.

        Args:
            project_dir: Project root directory

        Returns:
            Absolute SQLite URI (e.g., sqlite:////absolute/path/to/db.db)
        """
        abs_path = project_dir / self.relative_path
        return f"sqlite:///{abs_path}"


class AppConfig(BaseSettings):
    """Application configuration"""

    secret_key: str = Field(..., description="Flask secret key (from environment)")
    debug: bool = Field(default=False, description="Debug mode")
    host: str = Field(default="0.0.0.0", description="Host to bind")
    port: int = Field(default=5001, description="Port to bind")


class LogConfig(BaseSettings):
    """Logging configuration"""

    level: str = Field(default="INFO", description="Log level (DEBUG, INFO, WARNING, ERROR, CRITICAL)")
    console: bool = Field(default=True, description="Enable console logging")
    file: str | None = Field(default=None, description="Log file path (None to disable)")
    rotation: str = Field(default="10 MB", description="Log rotation size")
    retention: str = Field(default="7 days", description="Log retention period")
    compression: str = Field(default="zip", description="Compression format for rotated logs")


class Settings(BaseSettings):
    """
    Main application settings.
    Loads configuration from config.yml file only.
    SECRET_KEY must be provided via environment variable.
    """

    app: AppConfig
    database: DatabaseConfig
    log: LogConfig

    @classmethod
    def from_yaml(cls, config_path: str | Path = "config.yml") -> "Settings":
        """
        Load settings from YAML file.
        All parameters are optional with defaults except SECRET_KEY which comes from environment.

        Args:
            config_path: Path to config.yml file

        Returns:
            Settings instance

        Raises:
            ValueError: If SECRET_KEY environment variable is not set
        """
        # Get SECRET_KEY from environment (required)
        secret_key = os.getenv("SECRET_KEY")
        if not secret_key:
            raise ValueError(
                "SECRET_KEY environment variable is required. " "Copy .env.example to .env and set your secret key."
            )

        # Load from YAML if exists, otherwise use empty dict
        config_data: dict = {}
        config_path = Path(config_path)
        if config_path.exists():
            with open(config_path, "r", encoding="utf-8") as f:
                config_data = yaml.safe_load(f) or {}

        # Get sections with defaults
        app_data = config_data.get("app", {})
        db_data = config_data.get("database", {})
        log_data = config_data.get("log", {})

        # Add secret_key to app config
        app_data["secret_key"] = secret_key

        # Handle database config - convert 'uri' to 'relative_path' if present
        if "uri" in db_data:
            db_data["relative_path"] = db_data.pop("uri")

        # Remove track_modifications if present (not used anymore)
        db_data.pop("track_modifications", None)

        # Create and return Settings with all defaults applied by Pydantic
        return cls(app=AppConfig(**app_data), database=DatabaseConfig(**db_data), log=LogConfig(**log_data))


@lru_cache
def get_settings() -> Settings:
    """
    Get application settings (cached singleton).

    This function uses lru_cache to ensure only one Settings instance
    is created and reused throughout the application lifecycle.

    The first call:
    1. Loads SECRET_KEY from environment variable (required)
    2. Loads config.yml (all parameters optional with defaults)
    3. Validates with Pydantic
    4. Returns Settings instance

    Subsequent calls return the cached instance.

    Returns:
        Settings instance

    Raises:
        ValueError: If SECRET_KEY environment variable is not set

    Usage:
        from core.config import get_settings

        settings = get_settings()
        db_uri = settings.database.get_absolute_uri(project_dir)
        secret = settings.app.secret_key
        debug = settings.app.debug
    """
    return Settings.from_yaml()
