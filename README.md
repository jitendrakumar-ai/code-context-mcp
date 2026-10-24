# 🧠 code-context-mcp

> **Python MCP Server for AST Codebase Intelligence, Symbol Extraction, Cyclomatic Complexity & Refactoring Analysis — compatible with Cursor, Claude Code, Windsurf & AI Agents.**

---

## 🌟 Overview

`code-context-mcp` empowers Large Language Models and autonomous coding agents with deep, structural understanding of target software repositories. Instead of reading entire raw source files, LLMs can leverage AST parsing, static complexity metrics, architectural summaries, and hotspot discovery via Model Context Protocol (MCP).

---

## 🛠️ Tools Included

1. **`summarize_repository_architecture`**
   - Scans directory paths, generates file structure breakdown by extension, and computes total lines of code.
2. **`extract_python_ast_symbols`**
   - Parses Python files into Abstract Syntax Trees (AST) to extract classes, base classes, methods, docstrings, function signatures, and line markers.
3. **`analyze_cyclomatic_complexity`**
   - Calculates cyclomatic complexity scores for all functions/methods to identify refactoring candidates and branch depth.
4. **`search_code_todos_and_hotspots`**
   - Detects code comments containing `TODO`, `FIXME`, `HACK`, and `XXX` across the codebase with exact file and line references.

---

## ⚙️ MCP Installation & Setup Configs

### 1. Claude Desktop (`claude_desktop_config.json`)

Add the following to your `claude_desktop_config.json`:

```json
{
  "mcpServers": {
    "code-context-mcp": {
      "command": "python3",
      "args": [
        "/path/to/code-context-mcp/code_context_mcp.py"
      ]
    }
  }
}
```

### 2. Cursor (`.cursor/mcp.json`)

Add the following to your project's `.cursor/mcp.json`:

```json
{
  "mcpServers": {
    "code-context-mcp": {
      "command": "python3",
      "args": [
        "${workspaceFolder}/code_context_mcp.py"
      ]
    }
  }
}
```

---

## 🚀 Quickstart

Run directly from terminal:

```bash
python3 code_context_mcp.py
```

---

## 📄 License

MIT License © jitendrakumarvoicex-art (Dhruv)
