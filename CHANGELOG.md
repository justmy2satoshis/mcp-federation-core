# Changelog

All notable changes to the MCP Federation Core project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [0.1.4] - 2025-01-24

### CRITICAL FIXES
- **FIXED**: Directory nesting bug that created triple-nested mcp-federation-core folders
- **FIXED**: Incorrect npm package names causing warning triangles in Claude Desktop
- **FIXED**: Uninstaller now completely removes all installed files and directories
- **FIXED**: Python command compatibility on Windows (python3 → python)

### Major Changes
- **Installer v0.1.4**:
  - Added `check_installation_location()` to prevent directory nesting
  - Fixed perplexity package: `perplexity-mcp-server` → `server-perplexity-ask`
  - Changed converse-enhanced from GitHub to npm: `converse-mcp-server`
  - Platform-specific Python commands (Windows uses 'python')
  - Enhanced error handling and validation

- **Uninstaller v0.1.4**:
  - Three-level removal options: config-only, data files, or complete removal
  - Added `remove_installed_directories()` for complete artifact removal
  - Now removes entire mcp-servers directory when complete removal is selected
  - Preserves user choice through interactive prompts

- **New Diagnostic Tool**:
  - Created `verify_mcps.py` to test all MCPs for green checkmarks
  - Validates npm packages and script locations
  - Provides detailed fix suggestions for common issues
  - Saves verification results to JSON for debugging

### Package Corrections
- perplexity: Uses `server-perplexity-ask` (npm)
- converse-enhanced: Uses `converse-mcp-server` (npm)
- All other packages verified against working Claude Desktop configuration

## [0.1.3] - 2025-01-23

### CRITICAL FIX - Data Preservation
- **FIXED**: Data loss bug - uninstaller was removing pre-existing user MCPs
- Added installation manifest tracking to differentiate pre-existing vs newly installed MCPs
- Implemented safe uninstallation that only removes federation-installed MCPs

### Major Changes
- Installation manifest (`installation_manifest.json`) tracks:
  - Pre-existing MCPs (preserved during uninstall)
  - Newly installed MCPs (safe to remove)
  - Installation date and version
  - Failed installations

## [0.1.0] - 2025-01-22

### Added
- Initial release of MCP Federation Core
- Lightweight orchestrator for 15 production-ready MCP servers
- Selective database unification for 4 MCPs (40% memory savings)
- Automated installation from original sources (11 npm, 4 GitHub)
- Wrapper script generation for database path injection
- Cross-platform support (Windows/macOS/Linux)
- Comprehensive uninstaller with preservation options
- Zero bundled MCP code - pure orchestration approach

### Technical Architecture
- Federation pattern: thin coordinator, not monolithic bundle
- Sources MCPs from original repositories
- Environment variable configuration for npm MCPs
- Wrapper scripts for GitHub MCPs that don't support env vars
- Unified database for: memory, kimi-k2-code-context, kimi-k2-heavy-processor, rag-context
- Independent database for: sqlite (user operations)
- Stateless operation for: 10 remaining MCPs

### The 15 Federated MCPs
**From npm (11):**
- sequential-thinking, memory, filesystem, sqlite
- github-manager, web-search, playwright
- git-ops, desktop-commander, rag-context, perplexity

**From GitHub (4):**
- kimi-k2-heavy-processor-mcp
- converse-mcp-enhanced
- kimi-k2-code-context-mcp
- expert-role-prompt-mcp

---

For migration from earlier versions or bundled installations, see the README.