#!/bin/bash
# Safe Uninstaller for MCP Federation Core (Unix/Linux/macOS)
# Default: Selective removal - preserves user MCPs

echo "===================================================================="
echo "MCP Federation Core - Safe Uninstaller"
echo "===================================================================="
echo ""

# Check for Python
if ! command -v python3 &> /dev/null; then
    echo "ERROR: Python 3 is not installed"
    echo "Please install Python 3.8+ to continue"
    exit 1
fi

# Get the directory of this script
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

# Function to show help
show_help() {
    echo ""
    echo "Usage: $0 [mode] [options]"
    echo ""
    echo "Modes:"
    echo "  selective   Remove Federation MCPs only (default, recommended)"
    echo "  complete    Remove ALL MCPs (use with caution!)"
    echo "  restore     Restore from backup"
    echo "  dry-run     Show what would be removed without making changes"
    echo "  help        Show this help message"
    echo ""
    echo "Options:"
    echo "  --mcp-base PATH    Path to mcp_base directory"
    echo "  --backup-dir PATH  Specific backup to restore"
    echo "  --force           Skip confirmation prompts"
    echo ""
    echo "Examples:"
    echo "  $0                         # Interactive mode"
    echo "  $0 selective               # Remove Federation only"
    echo "  $0 complete --force        # Remove everything, no prompts"
    echo "  $0 restore                 # Restore from backup"
    echo "  $0 dry-run                 # Preview changes"
    echo ""
}

# Check for command-line arguments
if [ $# -eq 0 ]; then
    # Run interactive mode
    python3 "$SCRIPT_DIR/uninstall.py"
else
    case "$1" in
        selective)
            echo "Running SELECTIVE uninstall - Federation components only..."
            shift
            python3 "$SCRIPT_DIR/uninstall.py" --mode selective "$@"
            ;;
        complete)
            echo "WARNING: Complete uninstall will remove ALL MCPs!"
            shift
            python3 "$SCRIPT_DIR/uninstall.py" --mode complete "$@"
            ;;
        restore)
            echo "Restoring from backup..."
            shift
            python3 "$SCRIPT_DIR/uninstall.py" --mode restore "$@"
            ;;
        dry-run)
            echo "Running dry-run (no changes will be made)..."
            shift
            python3 "$SCRIPT_DIR/uninstall.py" --mode dry-run "$@"
            ;;
        help|-h|--help)
            show_help
            ;;
        *)
            echo "Unknown mode: $1"
            show_help
            exit 1
            ;;
    esac
fi