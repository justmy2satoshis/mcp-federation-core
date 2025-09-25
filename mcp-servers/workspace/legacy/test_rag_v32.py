#!/usr/bin/env python3
"""Test script for RAG Context v3.2"""

import sys
import os
sys.path.insert(0, r'C:\Users\User\mcp-servers\workspace\rag-context-v3.2')

import numpy as np
print(f"NumPy version: {np.__version__}")

from server import VectorStorage

# Initialize storage
vs = VectorStorage()

# Test 1: Store data
print("\n=== TEST 1: Storage ===")
success = vs.store('production_test_v32', 'This is critical production test data that MUST be retrievable')
print(f"Storage success: {success}")

success2 = vs.store('client_deployment', 'Client XYZ requires selective MCP installation with Ollama priority')
print(f"Storage success 2: {success2}")

success3 = vs.store('federation_test', 'Unified database enables cross-MCP data sharing and federation')
print(f"Storage success 3: {success3}")

# Test 2: Search data
print("\n=== TEST 2: Retrieval ===")
results = vs.search('critical production test', 5)
print(f"Search for 'critical production test': {len(results)} results")
for r in results:
    print(f"  - {r['key']}: score={r['score']:.3f}")

results2 = vs.search('client deployment ollama', 5)
print(f"\nSearch for 'client deployment ollama': {len(results2)} results")
for r in results2:
    print(f"  - {r['key']}: score={r['score']:.3f}")

results3 = vs.search('unified database federation', 5)
print(f"\nSearch for 'unified database federation': {len(results3)} results")
for r in results3:
    print(f"  - {r['key']}: score={r['score']:.3f}")

# Test 3: Verify persistence
print("\n=== TEST 3: Persistence ===")
vs2 = VectorStorage()  # New instance should load from disk
results4 = vs2.search('production', 5)
print(f"New instance search for 'production': {len(results4)} results")
for r in results4:
    print(f"  - {r['key']}: score={r['score']:.3f}")

print("\n✅ RAG Context v3.2 is WORKING!" if len(results) > 0 else "\n❌ RAG Context FAILED - empty results")