import sqlite3
import json

db_path = r'C:\Users\User\mcp-unified.db'

# Connect to database
conn = sqlite3.connect(db_path)
cursor = conn.cursor()

print("=" * 60)
print("MCP UNIFIED DATABASE VERIFICATION")
print("=" * 60)

# Check tables
cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
tables = cursor.fetchall()
print(f"\nTables in database: {[t[0] for t in tables]}")

# Check mcp_storage schema
cursor.execute("PRAGMA table_info(mcp_storage)")
schema = cursor.fetchall()
print("\nTable 'mcp_storage' schema:")
for col in schema:
    print(f"  Column: {col[1]}, Type: {col[2]}")

# Check data in mcp_storage
cursor.execute("SELECT * FROM mcp_storage")
data = cursor.fetchall()
print(f"\nTotal records in mcp_storage: {len(data)}")

if data:
    print("\nSample records:")
    for i, row in enumerate(data[:5]):  # Show first 5 records
        print(f"\nRecord {i+1}:")
        print(f"  ID: {row[0]}")
        print(f"  MCP: {row[1]}")
        print(f"  Key: {row[2]}")
        print(f"  Value: {row[3][:100] if len(row[3]) > 100 else row[3]}")  # Truncate long values
        print(f"  Created: {row[4]}")
        print(f"  TTL: {row[5]}")

# Check cross-MCP data
print("\n" + "=" * 60)
print("CROSS-MCP DATA CHECK")
print("=" * 60)

cursor.execute("SELECT DISTINCT mcp_name FROM mcp_storage")
mcps = cursor.fetchall()
print(f"\nMCPs with stored data: {[m[0] for m in mcps]}")

for mcp in mcps:
    cursor.execute("SELECT COUNT(*) FROM mcp_storage WHERE mcp_name=?", (mcp[0],))
    count = cursor.fetchone()[0]
    print(f"  {mcp[0]}: {count} records")

conn.close()
print("\n✅ Database verification complete!")
