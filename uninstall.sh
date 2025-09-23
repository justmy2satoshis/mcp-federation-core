#!/bin/bash
# MCP Federation Core - Safe Uninstaller Script
# This script removes ONLY Federation MCPs, preserving user configurations

echo "===================================================================="
echo "MCP Federation Core - Safe Uninstaller"
echo "===================================================================="
echo ""

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "ERROR: Python 3 is not installed"
    echo "Please install Python 3.8+ to continue"
    exit 1
fi

echo "Python detected: $(python3 --version)"

# Define installation path
MCP_BASE_PATH="$HOME/mcp-servers/installers/unified"
UNINSTALLER_SCRIPT="$MCP_BASE_PATH/uninstall.py"

# Check if uninstaller exists
if [ ! -f "$UNINSTALLER_SCRIPT" ]; then
    echo "ERROR: Uninstaller not found at $UNINSTALLER_SCRIPT"
    echo ""
    echo "The Federation Core may not be installed, or installation is incomplete."
    echo "If you need to manually remove MCPs, edit:"
    echo "  ~/Library/Application Support/Claude/claude_desktop_config.json (macOS)"
    echo "  ~/.config/claude/claude_desktop_config.json (Linux)"
    exit 1
fi

echo "Found uninstaller at: $UNINSTALLER_SCRIPT"
echo ""

# Run the uninstaller with selective mode by default
echo "Starting selective uninstall (preserves your other MCPs)..."
echo ""

# Execute Python uninstaller
python3 "$UNINSTALLER_SCRIPT" --mode selective

# Check exit code
if [ $? -eq 0 ]; then
    echo ""
    echo "===================================================================="
    echo "Uninstallation completed successfully!"
    echo "===================================================================="
    echo ""
    echo "Next steps:"
    echo "1. Restart Claude Desktop to apply changes"
    echo "2. Your other MCPs remain untouched"
    echo ""
else
    echo ""
    echo "Uninstallation encountered issues. Please check the output above."
    echo "You may need to run this script with sudo."
fi