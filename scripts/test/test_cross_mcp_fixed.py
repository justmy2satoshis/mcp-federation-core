#!/usr/bin/env python3
"""Test cross-MCP retrieval after fix"""

import sqlite3
from pathlib import Path

def test_cross_mcp_simulation():
    """Simulate what the fixed MCPs should do"""
    db_path = Path.home() / "mcp-unified.db"
    
    with sqlite3.connect(str(db_path)) as conn:
        # Test 1: Retrieve specific MCP data
        cursor = conn.execute("""
            SELECT value FROM mcp_storage 
            WHERE mcp_name = ? AND key = ?
        """, ("kimi-k2-resilient-enhanced", "test_resilient"))
        row = cursor.fetchone()
        print(f"Direct retrieval from kimi-resilient: {row[0] if row else 'NOT FOUND'}")
        
        # Test 2: Retrieve from any MCP (wildcard)
        cursor = conn.execute("""
            SELECT value, mcp_name FROM mcp_storage 
            WHERE key = ?
            ORDER BY updated_at DESC
            LIMIT 1
        """, ("test_resilient",))
        row = cursor.fetchone()
        print(f"Wildcard retrieval: {row[0] if row else 'NOT FOUND'} from {row[1] if row else 'N/A'}")
        
        # Test 3: Cross-MCP retrieval
        cursor = conn.execute("""
            SELECT value FROM mcp_storage 
            WHERE mcp_name = ? AND key = ?
        """, ("kimi-k2-code-context-enhanced", "test_code"))
        row = cursor.fetchone()
        print(f"Direct retrieval from kimi-code: {row[0] if row else 'NOT FOUND'}")
        
        # Show all stored data
        print("\nAll stored data:")
        cursor = conn.execute("""
            SELECT mcp_name, key, substr(value, 1, 30) as value_preview, created_at
            FROM mcp_storage
            ORDER BY created_at DESC
            LIMIT 10
        """)
        for row in cursor.fetchall():
            print(f"  {row[0]}: {row[1]} = {row[2]}...")

if __name__ == "__main__":
    test_cross_mcp_simulation()
