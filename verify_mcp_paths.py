#!/usr/bin/env python3
"""
MCP Path Verification Script
Ensures all MCP servers have correct entry points
"""

import os
import json
from pathlib import Path

# Correct MCP entry points
CORRECT_PATHS = {
    "expert-role-prompt": {
        "type": "node",
        "entry": "server.js",
        "test_indicator": "main().catch",  # Should have main function, not test code
    },
    "converse-enhanced": {
        "type": "python",
        "entry": "src/mcp_server.py",  # NOT server.py which has test code
        "test_indicator": "stdio_server",  # Should use stdio_server
    },
    "kimi-k2-code-context": {
        "type": "python", 
        "entry": "server.py",
        "test_indicator": "stdio_server",
    },
    "kimi-k2-resilient": {
        "type": "python",
        "entry": "server.py",
        "test_indicator": "stdio_server",
    },
    "rag-context": {
        "type": "python",
        "entry": "server.py",
        "test_indicator": "stdio_server",
    }
}

def check_mcp_server(name, config, base_dir):
    """Check if an MCP server has the correct entry point"""
    mcp_dir = base_dir / name.replace("-enhanced", "").replace("-mcp", "")
    
    if not mcp_dir.exists():
        mcp_dir = base_dir / (name + "-enhanced")
    if not mcp_dir.exists():
        mcp_dir = base_dir / name
    
    entry_path = mcp_dir / config["entry"]
    
    print(f"\nChecking {name}:")
    print(f"  Directory: {mcp_dir}")
    print(f"  Entry point: {entry_path}")
    
    if not entry_path.exists():
        print(f"  ❌ Entry point not found: {entry_path}")
        return False
    
    # Check for test code
    with open(entry_path, 'r', encoding='utf-8') as f:
        content = f.read()
        
    # Check for correct indicator
    if config["test_indicator"] in content:
        print(f"  ✅ Has correct indicator: {config['test_indicator']}")
    else:
        print(f"  ⚠️  Missing indicator: {config['test_indicator']}")
    
    # Check for problematic test code
    if config["type"] == "python":
        if 'if __name__ == "__main__"' in content:
            if 'asyncio.run(test())' in content:
                print("  ❌ WARNING: Has test code that will exit!")
                return False
            elif 'asyncio.run(main())' in content:
                print("  ✅ Has proper main() function")
            else:
                print("  ⚠️  Has __main__ block - check content")
    
    return True

def verify_claude_config():
    """Verify Claude Desktop configuration"""
    config_path = Path.home() / "AppData" / "Roaming" / "Claude" / "claude_desktop_config.json"
    
    if not config_path.exists():
        print("\n⚠️  Claude Desktop config not found")
        return
    
    with open(config_path, 'r') as f:
        config = json.load(f)
    
    print("\n=== Claude Desktop Configuration ===")
    mcps = config.get("mcpServers", {})
    
    for name, mcp_config in mcps.items():
        if name in ["converse-enhanced", "expert-role-prompt"]:
            args = mcp_config.get("args", [])
            if args:
                entry_file = Path(args[0]).name
                expected = "mcp_server.py" if name == "converse-enhanced" else "server.js"
                
                if entry_file == expected:
                    print(f"✅ {name}: Correct entry point ({entry_file})")
                else:
                    print(f"❌ {name}: Wrong entry point ({entry_file}), should be {expected}")

def main():
    """Main verification"""
    print("=== MCP Path Verification ===")
    print("\nThis script verifies that MCP servers have correct entry points")
    print("and don't contain test code that causes them to exit.\n")
    
    base_dir = Path(__file__).parent.parent
    
    # Check each MCP
    all_good = True
    for name, config in CORRECT_PATHS.items():
        if not check_mcp_server(name, config, base_dir):
            all_good = False
    
    # Check Claude config
    verify_claude_config()
    
    if all_good:
        print("\n✅ All MCP paths are correct!")
    else:
        print("\n❌ Some MCPs need fixes - see above")
    
    print("\n=== Key Findings ===")
    print("1. converse-enhanced must use mcp_server.py, NOT server.py")
    print("2. server.py contains test code that exits after running")
    print("3. expert-role-prompt uses server.js correctly")
    print("4. Other MCPs use server.py as their entry point")

if __name__ == "__main__":
    main()