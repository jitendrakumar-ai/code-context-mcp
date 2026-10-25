# Development Guidelines for CLAUDE.md

## Repository Overview
`code-context-mcp` provides high-speed AST analysis, symbol extraction, cyclomatic complexity calculations, and refactoring context for MCP clients.

## Commands
- **Self-Test:** `python3 code_context_mcp.py --self-test`
- **Run Server:** `python3 code_context_mcp.py`
- **Docker Build:** `docker build -t code-context-mcp .`

## Code Style & Rules
- Standard Python 3.10+ standard library (no external heavy dependencies required).
- Maintain 3-layer MCP tool responses (Summary, Detailed Data, Actionable Recommendations).
- Zero external data transmission (strictly local AST parsing).
