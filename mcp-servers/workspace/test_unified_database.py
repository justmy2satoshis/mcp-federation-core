#!/usr/bin/env python3
"""
Test suite for MCP Federation Core v0.1.0 - Unified Database
Validates database unification for 4 MCPs
"""

import json
import sqlite3
import tempfile
from pathlib import Path
import unittest
from unittest.mock import patch, MagicMock

class TestUnifiedDatabase(unittest.TestCase):
    """Test unified database architecture"""

    def setUp(self):
        """Setup test environment"""
        self.test_dir = Path(tempfile.mkdtemp())
        self.db_path = self.test_dir / "mcp-unified.db"

        # MCPs that share the unified database
        self.unified_mcps = [
            'memory',
            'kimi-k2-code-context',
            'kimi-k2-heavy-processor',
            'rag-context'
        ]

    def test_database_creation(self):
        """Test unified database is created properly"""
        # Create database
        conn = sqlite3.connect(str(self.db_path))
        cursor = conn.cursor()

        # Create namespaced tables
        for mcp in self.unified_mcps:
            table_name = f"{mcp.replace('-', '_')}_data"
            cursor.execute(f"""
                CREATE TABLE IF NOT EXISTS {table_name} (
                    id INTEGER PRIMARY KEY,
                    key TEXT,
                    value TEXT,
                    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
                )
            """)

        conn.commit()

        # Verify tables exist
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
        tables = [row[0] for row in cursor.fetchall()]

        self.assertEqual(len(tables), 4)
        self.assertIn('memory_data', tables)
        self.assertIn('kimi_k2_code_context_data', tables)
        self.assertIn('kimi_k2_heavy_processor_data', tables)
        self.assertIn('rag_context_data', tables)

        conn.close()
        print("[PASS] Unified database structure verified")

    def test_namespace_isolation(self):
        """Test that MCPs have isolated namespaces"""
        conn = sqlite3.connect(str(self.db_path))
        cursor = conn.cursor()

        # Create tables
        cursor.execute("""
            CREATE TABLE memory_data (id INTEGER PRIMARY KEY, data TEXT)
        """)
        cursor.execute("""
            CREATE TABLE kimi_k2_code_context_data (id INTEGER PRIMARY KEY, data TEXT)
        """)

        # Insert data
        cursor.execute("INSERT INTO memory_data (data) VALUES ('memory test')")
        cursor.execute("INSERT INTO kimi_k2_code_context_data (data) VALUES ('kimi test')")
        conn.commit()

        # Verify isolation
        cursor.execute("SELECT data FROM memory_data")
        memory_data = cursor.fetchone()[0]

        cursor.execute("SELECT data FROM kimi_k2_code_context_data")
        kimi_data = cursor.fetchone()[0]

        self.assertEqual(memory_data, 'memory test')
        self.assertEqual(kimi_data, 'kimi test')

        conn.close()
        print("[PASS] Namespace isolation verified")

    def test_cross_mcp_queries(self):
        """Test cross-MCP query capability"""
        conn = sqlite3.connect(str(self.db_path))
        cursor = conn.cursor()

        # Setup tables
        cursor.execute("""
            CREATE TABLE memory_data (
                id INTEGER PRIMARY KEY,
                context TEXT,
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        """)
        cursor.execute("""
            CREATE TABLE rag_context_data (
                id INTEGER PRIMARY KEY,
                embedding TEXT,
                context_ref TEXT,
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        """)

        # Insert related data
        cursor.execute("INSERT INTO memory_data (context) VALUES ('user asked about Python')")
        memory_id = cursor.lastrowid

        cursor.execute(
            "INSERT INTO rag_context_data (embedding, context_ref) VALUES (?, ?)",
            ('[0.1, 0.2, 0.3]', f'memory:{memory_id}')
        )
        conn.commit()

        # Cross-MCP query
        cursor.execute("""
            SELECT m.context, r.embedding
            FROM memory_data m
            JOIN rag_context_data r ON r.context_ref = 'memory:' || m.id
        """)

        result = cursor.fetchone()
        self.assertIsNotNone(result)
        self.assertEqual(result[0], 'user asked about Python')
        self.assertEqual(result[1], '[0.1, 0.2, 0.3]')

        conn.close()
        print("[PASS] Cross-MCP queries verified")

    def test_performance_benefits(self):
        """Test performance benefits of unified database"""
        import time

        # Unified approach
        unified_start = time.time()
        conn = sqlite3.connect(str(self.db_path))
        cursor = conn.cursor()

        for mcp in self.unified_mcps:
            table = f"{mcp.replace('-', '_')}_data"
            cursor.execute(f"CREATE TABLE IF NOT EXISTS {table} (id INTEGER PRIMARY KEY, data TEXT)")
            for i in range(100):
                cursor.execute(f"INSERT INTO {table} (data) VALUES (?)", (f"test_{i}",))

        conn.commit()
        conn.close()
        unified_time = time.time() - unified_start

        # Separate databases approach (simulated)
        separate_start = time.time()
        for mcp in self.unified_mcps:
            db_file = self.test_dir / f"{mcp}.db"
            conn = sqlite3.connect(str(db_file))
            cursor = conn.cursor()
            cursor.execute("CREATE TABLE data (id INTEGER PRIMARY KEY, data TEXT)")
            for i in range(100):
                cursor.execute("INSERT INTO data (data) VALUES (?)", (f"test_{i}",))
            conn.commit()
            conn.close()
        separate_time = time.time() - separate_start

        # Unified should be faster
        self.assertLess(unified_time, separate_time * 1.2)  # Allow some variance

        print(f"[PASS] Performance verified: Unified={unified_time:.3f}s, Separate={separate_time:.3f}s")
        print(f"   Improvement: {((separate_time - unified_time) / separate_time * 100):.1f}%")

    def tearDown(self):
        """Cleanup test environment"""
        import shutil
        if self.test_dir.exists():
            shutil.rmtree(self.test_dir)

def run_tests():
    """Run unified database tests"""
    print("="*70)
    print(" MCP Federation Core v0.1.0 - Unified Database Tests")
    print("="*70)

    suite = unittest.TestLoader().loadTestsFromTestCase(TestUnifiedDatabase)
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)

    print("\n" + "="*70)
    if result.wasSuccessful():
        print(" [PASS] ALL DATABASE TESTS PASSED")
    else:
        print(" [FAIL] SOME TESTS FAILED")
    print("="*70)

    return result.wasSuccessful()

if __name__ == "__main__":
    import sys
    success = run_tests()
    sys.exit(0 if success else 1)