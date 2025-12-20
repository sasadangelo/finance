# -----------------------------------------------------------------------------
# Copyright (c) 2025 Salvatore D'Angelo, Code4Projects
# Licensed under the MIT License. See LICENSE.md for details.
# -----------------------------------------------------------------------------
"""
Core infrastructure package.
Contains database management, configuration, and utilities.
"""
from .database import db, DatabaseManager
from .config import get_settings, Settings
from .log import LoggerManager

__all__ = [
    "db",
    "DatabaseManager",
    "get_settings",
    "Settings",
    "LoggerManager",
]
