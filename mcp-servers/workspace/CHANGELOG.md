# Changelog

All notable changes to the MCP Federation Core project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [0.1.0] - 2025-01-24

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