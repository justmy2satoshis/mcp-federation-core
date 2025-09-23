# Testing Guide

## Overview

This guide covers testing procedures for MCP Federation Core to ensure all components work correctly after installation.

## Quick Test

Run the automated test suite:

```bash
# Basic installation test
python ~/mcp-servers/installers/unified/test_installation.py

# Complete cycle test (install/uninstall/reinstall)
python ~/mcp-servers/installers/unified/test_complete_cycle.py

# Validation test
python ~/mcp-servers/installers/unified/validator.py
```

## Component Testing

### 1. Database Federation

Test the unified database:

```python
# test_database.py
import sqlite3
import os

db_path = os.path.expanduser("~/mcp-servers/mcp_base/databases/mcp-unified.db")
conn = sqlite3.connect(db_path)
cursor = conn.cursor()

# Check tables
cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
tables = cursor.fetchall()
print(f"Tables found: {len(tables)}")
for table in tables:
    print(f"  - {table[0]}")

# Test write
cursor.execute("INSERT INTO test_data (key, value) VALUES ('test', 'success')")
conn.commit()

# Test read
cursor.execute("SELECT * FROM test_data WHERE key='test'")
result = cursor.fetchone()
print(f"Test result: {result}")

conn.close()
```

### 2. Individual MCP Testing

Test each MCP in Claude Desktop:

#### SQLite MCP
```
@sqlite
Create a test table and insert data
```

#### Expert Role Prompt
```
@expert-role-prompt
List available expert roles
```

#### Web Search
```
@web-search
Search for "MCP Federation Core"
```

#### Converse MCP (with Ollama)
```
@converse
Test Ollama model detection
```

#### GitHub Manager
```
@github-manager
Search for repositories about MCP
```

#### File System
```
@filesystem
List files in current directory
```

### 3. Federation Testing

Test cross-MCP data sharing:

```python
# test_federation.py
import json
import sqlite3
import os

db_path = os.path.expanduser("~/mcp-servers/mcp_base/databases/mcp-unified.db")

def test_cross_mcp_data():
    """Test that multiple MCPs can share data"""
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    # Write from one MCP perspective
    cursor.execute("""
        INSERT INTO mcp_data (mcp_name, data_key, data_value)
        VALUES ('memory', 'shared_test', '{"test": "data"}')
    """)
    conn.commit()

    # Read from another MCP perspective
    cursor.execute("""
        SELECT data_value FROM mcp_data
        WHERE data_key = 'shared_test'
    """)
    result = cursor.fetchone()

    if result:
        print("[PASS] Cross-MCP data sharing works")
        print(f"Data: {result[0]}")
    else:
        print("[FAIL] Cross-MCP data sharing failed")

    conn.close()

test_cross_mcp_data()
```

### 4. Performance Testing

Test response times and throughput:

```python
# test_performance.py
import time
import sqlite3
import os
from concurrent.futures import ThreadPoolExecutor

db_path = os.path.expanduser("~/mcp-servers/mcp_base/databases/mcp-unified.db")

def test_query_performance():
    """Test database query performance"""
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    # Test read performance
    start = time.time()
    for _ in range(1000):
        cursor.execute("SELECT 1")
    read_time = (time.time() - start) * 1000

    print(f"1000 reads: {read_time:.2f}ms")
    print(f"Average: {read_time/1000:.4f}ms per query")

    # Test write performance
    start = time.time()
    for i in range(100):
        cursor.execute(
            "INSERT INTO test_perf (id, data) VALUES (?, ?)",
            (i, f"test_{i}")
        )
    conn.commit()
    write_time = (time.time() - start) * 1000

    print(f"100 writes: {write_time:.2f}ms")
    print(f"Average: {write_time/100:.2f}ms per write")

    conn.close()

def concurrent_test():
    """Test concurrent access"""
    def worker(id):
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        for i in range(10):
            cursor.execute(
                "INSERT INTO concurrent_test (worker, value) VALUES (?, ?)",
                (id, i)
            )
        conn.commit()
        conn.close()

    start = time.time()
    with ThreadPoolExecutor(max_workers=10) as executor:
        futures = [executor.submit(worker, i) for i in range(10)]
        for future in futures:
            future.result()

    elapsed = time.time() - start
    print(f"Concurrent test (10 workers, 100 writes): {elapsed:.2f}s")

test_query_performance()
concurrent_test()
```

## Integration Testing

### Install-Uninstall-Reinstall Cycle

```bash
# Full cycle test
cd ~/mcp-servers/installers/unified

# 1. Fresh install
python installer.py

# 2. Verify installation
python validator.py

# 3. Uninstall (selective)
python uninstall.py --mode selective

# 4. Verify removal
python validator.py

# 5. Reinstall
python installer.py

# 6. Final verification
python validator.py
```

### API Key Validation

```python
# test_api_keys.py
import os
import requests
from dotenv import load_dotenv

load_dotenv(os.path.expanduser("~/mcp-servers/.env"))

def test_brave_api():
    api_key = os.getenv("BRAVE_SEARCH_API_KEY")
    if not api_key:
        return "No Brave API key found"

    headers = {"X-Subscription-Token": api_key}
    response = requests.get(
        "https://api.search.brave.com/res/v1/web/search",
        params={"q": "test"},
        headers=headers
    )

    if response.status_code == 200:
        return "[PASS] Brave API working"
    else:
        return f"[FAIL] Brave API: {response.status_code}"

def test_github_api():
    token = os.getenv("GITHUB_TOKEN")
    if not token:
        return "No GitHub token found"

    headers = {"Authorization": f"token {token}"}
    response = requests.get(
        "https://api.github.com/user",
        headers=headers
    )

    if response.status_code == 200:
        return "[PASS] GitHub API working"
    else:
        return f"[FAIL] GitHub API: {response.status_code}"

print(test_brave_api())
print(test_github_api())
```

## Ollama Integration Testing

```bash
# Check Ollama installation
ollama list

# Test Ollama with Converse MCP
python -c "
from converse_enhanced.ollama_detector import OllamaDetector
detector = OllamaDetector()
models = detector.get_available_models()
print(f'Found {len(models)} Ollama models')
for model in models:
    print(f'  - {model['name']}')
"
```

## Stress Testing

### High Load Test

```python
# stress_test.py
import threading
import time
import random
from concurrent.futures import ThreadPoolExecutor

def stress_worker(worker_id, duration=60):
    """Simulate MCP operations"""
    start = time.time()
    operations = 0

    while time.time() - start < duration:
        # Simulate different MCP operations
        operation = random.choice([
            'database_read',
            'database_write',
            'file_read',
            'api_call'
        ])

        # Add small delay to simulate real work
        time.sleep(random.uniform(0.01, 0.1))
        operations += 1

    return operations

def run_stress_test():
    """Run stress test with multiple workers"""
    workers = 20
    duration = 10  # seconds

    print(f"Starting stress test: {workers} workers for {duration}s")

    with ThreadPoolExecutor(max_workers=workers) as executor:
        futures = [
            executor.submit(stress_worker, i, duration)
            for i in range(workers)
        ]

        results = [f.result() for f in futures]

    total_ops = sum(results)
    print(f"Completed: {total_ops} operations")
    print(f"Rate: {total_ops/duration:.1f} ops/sec")

run_stress_test()
```

## Automated Test Suite

Run all tests automatically:

```bash
# Create test runner
cat > ~/mcp-servers/run_all_tests.py << 'EOF'
#!/usr/bin/env python3
import subprocess
import sys
import os

def run_test(name, command):
    print(f"\n{'='*60}")
    print(f"Running: {name}")
    print('='*60)

    result = subprocess.run(
        command,
        shell=True,
        capture_output=True,
        text=True
    )

    if result.returncode == 0:
        print(f"[PASS] {name}")
        print(result.stdout)
    else:
        print(f"[FAIL] {name}")
        print(result.stderr)

    return result.returncode == 0

def main():
    tests = [
        ("Installation Test", "python ~/mcp-servers/installers/unified/test_installation.py"),
        ("Validator", "python ~/mcp-servers/installers/unified/validator.py"),
        ("Database Test", "python ~/mcp-servers/test_database.py"),
        ("API Keys Test", "python ~/mcp-servers/test_api_keys.py"),
        ("Performance Test", "python ~/mcp-servers/test_performance.py"),
    ]

    passed = 0
    failed = 0

    for name, command in tests:
        if run_test(name, command):
            passed += 1
        else:
            failed += 1

    print(f"\n{'='*60}")
    print(f"Test Results: {passed} passed, {failed} failed")
    print('='*60)

    return 0 if failed == 0 else 1

if __name__ == "__main__":
    sys.exit(main())
EOF

# Make executable and run
chmod +x ~/mcp-servers/run_all_tests.py
python ~/mcp-servers/run_all_tests.py
```

## CI/CD Integration

### GitHub Actions Workflow

```yaml
# .github/workflows/test.yml
name: Test MCP Federation

on:
  push:
    branches: [ main ]
  pull_request:
    branches: [ main ]

jobs:
  test:
    runs-on: ${{ matrix.os }}
    strategy:
      matrix:
        os: [ubuntu-latest, windows-latest, macos-latest]
        python: [3.8, 3.9, 3.10, 3.11]
        node: [18, 20]

    steps:
    - uses: actions/checkout@v3

    - name: Setup Python
      uses: actions/setup-python@v4
      with:
        python-version: ${{ matrix.python }}

    - name: Setup Node
      uses: actions/setup-node@v3
      with:
        node-version: ${{ matrix.node }}

    - name: Install dependencies
      run: |
        python -m pip install --upgrade pip
        pip install -r requirements.txt
        npm install

    - name: Run tests
      run: |
        python installers/unified/test_installation.py
        python installers/unified/validator.py

    - name: Test uninstaller
      run: |
        python installers/unified/uninstall.py --mode dry-run
```

## Test Checklist

Before releasing or after major changes:

- [ ] All 15 MCPs detected by validator
- [ ] Database operations work (read/write)
- [ ] API keys validated (if configured)
- [ ] Ollama auto-detection works
- [ ] Uninstaller removes only Federation MCPs
- [ ] Reinstallation works after uninstall
- [ ] Cross-MCP data sharing works
- [ ] Performance meets targets (<50ms queries)
- [ ] No errors in Claude Desktop console
- [ ] All documentation links work

## Debugging

### Enable Debug Logging

```python
# Add to any test script
import logging
logging.basicConfig(level=logging.DEBUG)
```

### Check MCP Logs

```bash
# Windows
type %APPDATA%\Claude\logs\*.log

# macOS/Linux
tail -f ~/Library/Logs/Claude/*.log
```

### Database Inspection

```bash
# Open database for inspection
sqlite3 ~/mcp-servers/mcp_base/databases/mcp-unified.db

# SQLite commands
.tables
.schema mcp_data
SELECT * FROM mcp_data LIMIT 10;
.quit
```

## Reporting Issues

When reporting test failures:

1. Run validator and save output:
   ```bash
   python ~/mcp-servers/installers/unified/validator.py > validation_report.txt
   ```

2. Include:
   - OS and version
   - Python version
   - Node.js version
   - Claude Desktop version
   - Full error messages
   - Validation report

3. Create issue: [GitHub Issues](https://github.com/justmy2satoshis/mcp-federation-core/issues)

## Success Criteria

Installation is successful when:

1. ✅ All 15 MCPs show in Claude Desktop
2. ✅ Database at correct path (mcp-unified.db)
3. ✅ No SQLITE_NOTADB errors
4. ✅ API keys loaded (for configured MCPs)
5. ✅ Ollama models detected (if installed)
6. ✅ Cross-MCP data sharing works
7. ✅ Query performance <50ms
8. ✅ Uninstaller preserves user MCPs

---

*For more help, see [TROUBLESHOOTING.md](../TROUBLESHOOTING.md)*