#!/usr/bin/env python3
"""
Database Manager for MCP Federation Core
Initializes all databases with proper schemas
"""

import sqlite3
import json
import logging
from pathlib import Path
from typing import Dict, List, Optional
from datetime import datetime

class DatabaseManager:
    def __init__(self, mcp_base: Path):
        self.mcp_base = mcp_base
        self.databases_dir = mcp_base / 'databases'
        self.logger = logging.getLogger(__name__)

        # Database configurations
        self.db_configs = {
            'mcp-unified.db': {
                'description': 'Main unified database for cross-MCP communication',
                'schemas': self._get_unified_schemas()
            },
            'expert-roles.db': {
                'description': 'Expert role prompts and capabilities',
                'schemas': self._get_expert_roles_schemas()
            },
            'memory-graph.db': {
                'description': 'Graph-based memory storage',
                'schemas': self._get_memory_schemas()
            },
            'rag-context.db': {
                'description': 'RAG vector storage and embeddings',
                'schemas': self._get_rag_schemas()
            }
        }

    def _get_unified_schemas(self) -> List[str]:
        """Get schemas for the main unified database"""
        return [
            """
            CREATE TABLE IF NOT EXISTS mcp_metadata (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                mcp_name TEXT NOT NULL,
                version TEXT,
                installed_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                config TEXT, -- JSON configuration
                status TEXT DEFAULT 'active'
            )
            """,
            """
            CREATE TABLE IF NOT EXISTS mcp_storage (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                mcp_name TEXT NOT NULL,
                key TEXT NOT NULL,
                value TEXT, -- JSON or text data
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                ttl INTEGER, -- Time to live in seconds
                UNIQUE(mcp_name, key)
            )
            """,
            """
            CREATE TABLE IF NOT EXISTS mcp_logs (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                mcp_name TEXT NOT NULL,
                level TEXT NOT NULL, -- INFO, WARNING, ERROR, DEBUG
                message TEXT NOT NULL,
                context TEXT, -- JSON context
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
            """,
            """
            CREATE INDEX IF NOT EXISTS idx_mcp_storage_name_key
            ON mcp_storage(mcp_name, key)
            """,
            """
            CREATE INDEX IF NOT EXISTS idx_mcp_logs_name_level
            ON mcp_logs(mcp_name, level)
            """,
            """
            CREATE INDEX IF NOT EXISTS idx_mcp_logs_created
            ON mcp_logs(created_at)
            """
        ]

    def _get_expert_roles_schemas(self) -> List[str]:
        """Get schemas for expert roles database"""
        return [
            """
            CREATE TABLE IF NOT EXISTS expert_roles (
                id TEXT PRIMARY KEY,
                name TEXT NOT NULL,
                category TEXT NOT NULL,
                description TEXT NOT NULL,
                capabilities TEXT, -- JSON array
                frameworks TEXT, -- JSON array
                best_for TEXT, -- JSON array
                confidence_keywords TEXT, -- JSON array for matching
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
            """,
            """
            CREATE TABLE IF NOT EXISTS role_interactions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                role_id TEXT NOT NULL,
                task_description TEXT NOT NULL,
                confidence_score REAL,
                success BOOLEAN,
                feedback TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (role_id) REFERENCES expert_roles(id)
            )
            """,
            """
            CREATE INDEX IF NOT EXISTS idx_roles_category
            ON expert_roles(category)
            """,
            """
            CREATE INDEX IF NOT EXISTS idx_interactions_role
            ON role_interactions(role_id)
            """
        ]

    def _get_memory_schemas(self) -> List[str]:
        """Get schemas for memory graph database"""
        return [
            """
            CREATE TABLE IF NOT EXISTS entities (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL UNIQUE,
                entity_type TEXT NOT NULL,
                properties TEXT, -- JSON properties
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
            """,
            """
            CREATE TABLE IF NOT EXISTS relationships (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                from_entity_id INTEGER NOT NULL,
                to_entity_id INTEGER NOT NULL,
                relationship_type TEXT NOT NULL,
                properties TEXT, -- JSON properties
                strength REAL DEFAULT 1.0,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (from_entity_id) REFERENCES entities(id),
                FOREIGN KEY (to_entity_id) REFERENCES entities(id)
            )
            """,
            """
            CREATE TABLE IF NOT EXISTS observations (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                entity_id INTEGER NOT NULL,
                content TEXT NOT NULL,
                source TEXT, -- Which MCP created this observation
                confidence REAL DEFAULT 1.0,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (entity_id) REFERENCES entities(id)
            )
            """,
            """
            CREATE INDEX IF NOT EXISTS idx_entities_name
            ON entities(name)
            """,
            """
            CREATE INDEX IF NOT EXISTS idx_relationships_from
            ON relationships(from_entity_id)
            """,
            """
            CREATE INDEX IF NOT EXISTS idx_relationships_to
            ON relationships(to_entity_id)
            """,
            """
            CREATE INDEX IF NOT EXISTS idx_observations_entity
            ON observations(entity_id)
            """
        ]

    def _get_rag_schemas(self) -> List[str]:
        """Get schemas for RAG context database"""
        return [
            """
            CREATE TABLE IF NOT EXISTS contexts (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                key TEXT NOT NULL UNIQUE,
                content TEXT NOT NULL,
                metadata TEXT, -- JSON metadata
                vector_embedding BLOB, -- Stored vector
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
            """,
            """
            CREATE TABLE IF NOT EXISTS search_history (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                query TEXT NOT NULL,
                results_count INTEGER,
                execution_time_ms REAL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
            """,
            """
            CREATE INDEX IF NOT EXISTS idx_contexts_key
            ON contexts(key)
            """,
            """
            CREATE INDEX IF NOT EXISTS idx_search_history_query
            ON search_history(query)
            """
        ]

    def initialize_database(self, db_name: str) -> bool:
        """Initialize a single database with its schemas"""
        if db_name not in self.db_configs:
            self.logger.error(f"Unknown database: {db_name}")
            return False

        db_path = self.databases_dir / db_name
        config = self.db_configs[db_name]

        try:
            # Create databases directory
            self.databases_dir.mkdir(parents=True, exist_ok=True)

            # Connect and create schemas
            with sqlite3.connect(db_path) as conn:
                conn.execute("PRAGMA foreign_keys = ON")  # Enable foreign keys

                for schema in config['schemas']:
                    conn.execute(schema)

                conn.commit()

            # Verify database was created successfully
            if db_path.exists() and db_path.stat().st_size > 0:
                self.logger.info(f"✓ Initialized {db_name} ({config['description']})")
                return True
            else:
                self.logger.error(f"✗ Failed to create {db_name}")
                return False

        except Exception as e:
            self.logger.error(f"Error initializing {db_name}: {e}")
            return False

    def initialize_all_databases(self) -> bool:
        """Initialize all required databases"""
        self.logger.info("Initializing database schemas...")

        success_count = 0
        total_count = len(self.db_configs)

        for db_name in self.db_configs:
            if self.initialize_database(db_name):
                success_count += 1

        if success_count == total_count:
            self.logger.info(f"✓ All {total_count} databases initialized successfully")
            self._seed_initial_data()
            return True
        else:
            self.logger.error(f"✗ Only {success_count}/{total_count} databases initialized")
            return False

    def _seed_initial_data(self):
        """Seed databases with initial data"""
        # Seed unified database with MCP metadata
        unified_db = self.databases_dir / 'mcp-unified.db'

        initial_mcps = [
            {'name': 'sqlite-data-warehouse', 'version': '1.0.0', 'status': 'active'},
            {'name': 'expert-role-prompt', 'version': '1.0.0', 'status': 'active'},
            {'name': 'kimi-k2-resilient', 'version': '1.0.0', 'status': 'active'},
            {'name': 'converse-enhanced', 'version': '3.3.0', 'status': 'active'},
            {'name': 'filesystem', 'version': '1.0.0', 'status': 'active'},
            {'name': 'memory', 'version': '1.0.0', 'status': 'active'},
            {'name': 'sequential-thinking', 'version': '1.0.0', 'status': 'active'},
            {'name': 'desktop-commander', 'version': '1.0.0', 'status': 'active'},
            {'name': 'playwright', 'version': '0.0.37', 'status': 'active'},
            {'name': 'git-ops', 'version': '1.0.0', 'status': 'active'}
        ]

        try:
            with sqlite3.connect(unified_db) as conn:
                for mcp in initial_mcps:
                    conn.execute(
                        "INSERT OR REPLACE INTO mcp_metadata (mcp_name, version, status) VALUES (?, ?, ?)",
                        (mcp['name'], mcp['version'], mcp['status'])
                    )
                conn.commit()

            self.logger.info("✓ Seeded initial MCP metadata")
        except Exception as e:
            self.logger.warning(f"Could not seed initial data: {e}")

    def validate_databases(self) -> Dict[str, bool]:
        """Validate all databases are properly initialized"""
        results = {}

        for db_name in self.db_configs:
            db_path = self.databases_dir / db_name

            if not db_path.exists():
                results[db_name] = False
                continue

            try:
                with sqlite3.connect(db_path) as conn:
                    # Check if main tables exist
                    cursor = conn.execute(
                        "SELECT name FROM sqlite_master WHERE type='table'"
                    )
                    tables = [row[0] for row in cursor.fetchall()]

                    # Each database should have at least one table
                    results[db_name] = len(tables) > 0

            except Exception as e:
                self.logger.error(f"Validation error for {db_name}: {e}")
                results[db_name] = False

        return results

    def get_unified_db_path(self) -> Path:
        """Get the path to the unified database"""
        return self.databases_dir / 'mcp-unified.db'

if __name__ == '__main__':
    # Test database initialization
    from pathlib import Path

    mcp_base = Path('test_mcp_base')
    db_manager = DatabaseManager(mcp_base)

    if db_manager.initialize_all_databases():
        print("✓ Database initialization test passed")

        # Validate
        results = db_manager.validate_databases()
        for db_name, valid in results.items():
            print(f"  {db_name}: {'✓' if valid else '✗'}")
    else:
        print("✗ Database initialization test failed")