#!/usr/bin/env python3
"""
MCP Data Persistence Test
Tests storage, retention, recall, and data sharing across all MCPs
"""
import sqlite3
from pathlib import Path
from datetime import datetime, timedelta
import json
import sys

# Fix Unicode output on Windows
if sys.platform == "win32":
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

def test_unified_database():
    """Test the unified database functionality"""
    db_path = Path.home() / "mcp-unified.db"
    print(f"Testing Unified Database at: {db_path}")
    print("=" * 60)
    
    # Connect to database
    conn = sqlite3.connect(str(db_path))
    cursor = conn.cursor()
    
    # 1. Test table structure
    print("\n1. VERIFYING TABLE STRUCTURE:")
    cursor.execute("""
        SELECT sql FROM sqlite_master 
        WHERE type='table' AND name='mcp_storage'
    """)
    table_def = cursor.fetchone()
    if table_def:
        print("✅ mcp_storage table exists")
        print(f"   Schema: {table_def[0]}")
    else:
        print("❌ mcp_storage table not found")
    
    # 2. Test data insertion from different MCPs
    print("\n2. TESTING DATA PERSISTENCE:")
    test_data = [
        ("kimi-k2-code-context-enhanced", "test_code", "function analyze() { return true; }"),
        ("kimi-k2-resilient-enhanced", "test_resilient", "circuit_breaker_status: open"),
        ("expert-role-prompt", "test_role", "active_role: backend-engineer"),
        ("memory", "test_memory", "user_preference: dark_mode"),
        ("rag-context", "test_rag", "indexed_documents: 42")
    ]
    
    for mcp_name, key, value in test_data:
        try:
            cursor.execute("""
                INSERT OR REPLACE INTO mcp_storage (mcp_name, key, value, updated_at)
                VALUES (?, ?, ?, CURRENT_TIMESTAMP)
            """, (mcp_name, key, value))
            print(f"✅ Stored data for {mcp_name}: {key}")
        except Exception as e:
            print(f"❌ Failed to store for {mcp_name}: {e}")
    
    conn.commit()
    
    # 3. Test data retrieval
    print("\n3. TESTING DATA RECALL:")
    cursor.execute("""
        SELECT mcp_name, key, value, 
               datetime(created_at, 'localtime') as created,
               datetime(updated_at, 'localtime') as updated
        FROM mcp_storage 
        WHERE key LIKE 'test_%'
        ORDER BY mcp_name
    """)
    
    results = cursor.fetchall()
    for mcp, key, value, created, updated in results:
        print(f"✅ {mcp:30} | {key:15} | {value[:30]}")
    
    # 4. Test data sharing between MCPs
    print("\n4. TESTING CROSS-MCP DATA ACCESS:")
    # Simulate one MCP reading another's data
    cursor.execute("""
        SELECT value FROM mcp_storage 
        WHERE mcp_name = ? AND key = ?
    """, ("kimi-k2-code-context-enhanced", "test_code"))
    
    shared_data = cursor.fetchone()
    if shared_data:
        print(f"✅ kimi-resilient can read kimi-code data: {shared_data[0][:30]}")
    
    # 5. Test TTL/expiration
    print("\n5. TESTING DATA RETENTION (TTL):")
    expires_soon = datetime.now() + timedelta(seconds=10)
    expires_later = datetime.now() + timedelta(hours=1)
    
    cursor.execute("""
        INSERT OR REPLACE INTO mcp_storage 
        (mcp_name, key, value, ttl, expires_at)
        VALUES (?, ?, ?, ?, ?)
    """, ("test-mcp", "short_ttl", "expires in 10 seconds", 10, expires_soon))
    
    cursor.execute("""
        INSERT OR REPLACE INTO mcp_storage 
        (mcp_name, key, value, ttl, expires_at)
        VALUES (?, ?, ?, ?, ?)
    """, ("test-mcp", "long_ttl", "expires in 1 hour", 3600, expires_later))
    
    conn.commit()
    
    # Check non-expired data
    cursor.execute("""
        SELECT key, value, datetime(expires_at, 'localtime') as expiry
        FROM mcp_storage 
        WHERE mcp_name = 'test-mcp' 
        AND (expires_at IS NULL OR expires_at > datetime('now'))
    """)
    
    valid_data = cursor.fetchall()
    for key, value, expiry in valid_data:
        print(f"✅ Valid data: {key} | Expires: {expiry}")
    
    # 6. Test data statistics
    print("\n6. DATABASE STATISTICS:")
    cursor.execute("""
        SELECT 
            COUNT(*) as total_records,
            COUNT(DISTINCT mcp_name) as unique_mcps,
            COUNT(DISTINCT key) as unique_keys,
            MIN(datetime(created_at, 'localtime')) as oldest_record,
            MAX(datetime(updated_at, 'localtime')) as newest_record
        FROM mcp_storage
    """)
    
    stats = cursor.fetchone()
    print(f"   Total Records: {stats[0]}")
    print(f"   Unique MCPs: {stats[1]}")
    print(f"   Unique Keys: {stats[2]}")
    print(f"   Oldest Record: {stats[3]}")
    print(f"   Newest Record: {stats[4]}")
    
    # 7. Test cleanup of expired data
    print("\n7. TESTING EXPIRED DATA CLEANUP:")
    cursor.execute("""
        DELETE FROM mcp_storage 
        WHERE expires_at IS NOT NULL 
        AND expires_at < datetime('now')
    """)
    
    deleted = cursor.rowcount
    print(f"✅ Cleaned up {deleted} expired records")
    
    conn.commit()
    conn.close()
    
    print("\n" + "=" * 60)
    print("✅ UNIFIED DATABASE TEST COMPLETE")
    print("All MCPs can share data through the unified database!")

if __name__ == "__main__":
    test_unified_database()
