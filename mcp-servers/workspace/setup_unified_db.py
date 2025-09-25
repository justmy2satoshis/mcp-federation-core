#!/usr/bin/env python3
"""Setup the unified MCP federation database"""

import sqlite3
import json
from pathlib import Path
from datetime import datetime

# Database path
DB_PATH = Path(r"C:\Users\User\mcp-servers\databases\mcp-federation.db")
DB_PATH.parent.mkdir(parents=True, exist_ok=True)

print(f"Setting up unified database at: {DB_PATH}")

# Connect to database
conn = sqlite3.connect(DB_PATH)
cursor = conn.cursor()

# Drop old test table if exists
cursor.execute("DROP TABLE IF EXISTS mcp_test_data")

# Create the unified context table
cursor.execute("""
CREATE TABLE IF NOT EXISTS mcp_context (
    id TEXT PRIMARY KEY,
    mcp_source TEXT NOT NULL,
    key TEXT NOT NULL,
    content TEXT NOT NULL,
    metadata TEXT,
    vector_data BLOB,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UNIQUE(mcp_source, key)
)
""")

# Create indexes for performance
cursor.execute("CREATE INDEX IF NOT EXISTS idx_mcp_source ON mcp_context(mcp_source)")
cursor.execute("CREATE INDEX IF NOT EXISTS idx_key ON mcp_context(key)")
cursor.execute("CREATE INDEX IF NOT EXISTS idx_created ON mcp_context(created_at)")

# Create federation view
cursor.execute("""
CREATE VIEW IF NOT EXISTS federation_view AS 
SELECT mcp_source, key, content, metadata, created_at 
FROM mcp_context 
ORDER BY created_at DESC
""")

# Create cross-MCP access table for tracking
cursor.execute("""
CREATE TABLE IF NOT EXISTS mcp_access_log (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    accessing_mcp TEXT NOT NULL,
    target_mcp TEXT NOT NULL,
    key TEXT NOT NULL,
    operation TEXT NOT NULL,
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
)
""")

conn.commit()

# Verify tables were created
cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
tables = cursor.fetchall()
print(f"\nCreated tables: {[t[0] for t in tables]}")

# Check if we have data from RAG Context
cursor.execute("SELECT COUNT(*) FROM mcp_context WHERE mcp_source='rag-context'")
rag_count = cursor.fetchone()[0]
print(f"RAG Context entries: {rag_count}")

# Display sample data
cursor.execute("SELECT mcp_source, key, substr(content, 1, 50) as preview FROM mcp_context LIMIT 5")
samples = cursor.fetchall()
if samples:
    print("\nSample entries:")
    for source, key, preview in samples:
        print(f"  - [{source}] {key}: {preview}...")
else:
    print("\nNo data yet in unified database")

conn.close()
print(f"\n✅ Unified database ready at: {DB_PATH}")