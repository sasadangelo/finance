-- -----------------------------------------------------------------------------
-- Copyright (c) 2025 Salvatore D'Angelo, Code4Projects
-- Licensed under the MIT License. See LICENSE.md for details.
-- -----------------------------------------------------------------------------
-- Migration: Add indexTicker column to etfs table
-- Description: Adds a nullable foreign key column to link ETFs to their reference index

-- Add the indexTicker column (nullable)
ALTER TABLE etfs ADD COLUMN indexTicker VARCHAR(10);

-- Note: SQLite doesn't support adding foreign key constraints to existing tables
-- The foreign key constraint is defined in the model and will be enforced by SQLAlchemy
-- For a fresh database, the constraint will be created when the table is created

-- Made with Bob
