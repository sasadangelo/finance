# -----------------------------------------------------------------------------
# Copyright (c) 2025 Salvatore D'Angelo, Code4Projects
# Licensed under the MIT License. See LICENSE.md for details.
# -----------------------------------------------------------------------------
"""
Configuration management using Pydantic Settings.
Loads configuration from config.yml and environment variables.
"""
from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import Field
from typing import Optional
import yaml
from pathlib import Path
from functools import lru_cache
import os


class DatabaseConfig(BaseSettings):
    """Database configuration"""

    uri: str = Field(default="database/etfs.db", description="Database URI (relative path)")
    track_modifications: bool = Field(default=False, description="Track modifications")

    model_config = SettingsConfigDict(env_prefix="DATABASE_", case_sensitive=False)

    def get_absolute_uri(self, project_dir: Path) -> str:
        """
        Convert relative database path to absolute SQLite URI.

        Args:
            project_dir: Project root directory

        Returns:
            Absolute SQLite URI (e.g., sqlite:////absolute/path/to/db.db)
        """
        # If already a full URI (starts with sqlite://), return as-is
        if self.uri.startswith("sqlite://"):
            return self.uri

        # Otherwise, treat as relative path and make absolute
        abs_path = project_dir / self.uri
        return f"sqlite:///{abs_path}"


class AppConfig(BaseSettings):
    """Application configuration"""

    secret_key: str = Field(..., description="Flask secret key (from environment)")
    debug: bool = Field(default=False, description="Debug mode")
    host: str = Field(default="0.0.0.0", description="Host to bind")
    port: int = Field(default=5001, description="Port to bind")

    model_config = SettingsConfigDict(env_prefix="", case_sensitive=False)


class LogConfig(BaseSettings):
    """Logging configuration"""

    level: str = Field(default="INFO", description="Log level (DEBUG, INFO, WARNING, ERROR, CRITICAL)")
    console: bool = Field(default=True, description="Enable console logging")
    file: Optional[str] = Field(default=None, description="Log file path (None to disable)")
    rotation: str = Field(default="10 MB", description="Log rotation size")
    retention: str = Field(default="7 days", description="Log retention period")
    compression: str = Field(default="zip", description="Compression format for rotated logs")

    model_config = SettingsConfigDict(env_prefix="LOG_", case_sensitive=False)


class Settings(BaseSettings):
    """
    Main application settings.
    Loads configuration from:
    1. Environment variables (.env file)
    2. config.yml file
    """

    app: AppConfig
    database: DatabaseConfig
    log: LogConfig

    @classmethod
    def from_yaml_and_env(cls, config_path: str | Path = "config.yml") -> "Settings":
        """
        Load settings from YAML file and environment variables.
        Environment variables override YAML values.

        Args:
            config_path: Path to config.yml file

        Returns:
            Settings instance
        """
        # Load from YAML if exists
        config_data = {}
        config_path = Path(config_path)
        if config_path.exists():
            with open(config_path, "r", encoding="utf-8") as f:
                config_data = yaml.safe_load(f) or {}

        # Create configs with env override
        app_data = config_data.get("app", {})
        db_data = config_data.get("database", {})
        log_data = config_data.get("log", {})

        # Environment variables override YAML
        # SECRET_KEY must come from environment
        secret_key = os.getenv("SECRET_KEY")
        if not secret_key:
            raise ValueError(
                "SECRET_KEY environment variable is required. " "Copy .env.example to .env and set your secret key."
            )

        app_data["secret_key"] = secret_key
        app_data["debug"] = os.getenv("DEBUG", str(app_data.get("debug", False))).lower() == "true"
        app_data["host"] = os.getenv("HOST", app_data.get("host", "0.0.0.0"))
        app_data["port"] = int(os.getenv("PORT", app_data.get("port", 5001)))

        db_data["uri"] = os.getenv("DATABASE_URI", db_data.get("uri", "sqlite:///database/etfs.db"))
        db_data["track_modifications"] = (
            os.getenv("DATABASE_TRACK_MODIFICATIONS", str(db_data.get("track_modifications", False))).lower() == "true"
        )

        log_data["level"] = os.getenv("LOG_LEVEL", log_data.get("level", "INFO"))
        log_data["console"] = os.getenv("LOG_CONSOLE", str(log_data.get("console", True))).lower() == "true"
        log_data["file"] = os.getenv("LOG_FILE", log_data.get("file"))
        log_data["rotation"] = os.getenv("LOG_ROTATION", log_data.get("rotation", "10 MB"))
        log_data["retention"] = os.getenv("LOG_RETENTION", log_data.get("retention", "7 days"))
        log_data["compression"] = os.getenv("LOG_COMPRESSION", log_data.get("compression", "zip"))

        return cls(app=AppConfig(**app_data), database=DatabaseConfig(**db_data), log=LogConfig(**log_data))


@lru_cache
def get_settings() -> Settings:
    """
    Get application settings (cached singleton).

    This function uses lru_cache to ensure only one Settings instance
    is created and reused throughout the application lifecycle.

    The first call:
    1. Loads .env file (if exists)
    2. Loads config.yml
    3. Merges with environment variables (env vars have priority)
    4. Validates with Pydantic
    5. Returns Settings instance

    Subsequent calls return the cached instance.

    Returns:
        Settings instance

    Usage:
        from core.config import get_settings

        settings = get_settings()
        db_uri = settings.database.uri
        secret = settings.app.secret_key
    """
    return Settings.from_yaml_and_env()


# Made with Bob
