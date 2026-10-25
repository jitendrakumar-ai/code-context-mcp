<div align="center">
  <img src="assets/banner.svg" width="100%" alt="code-context-mcp Banner" />
</div>

<p align="center">
  <img src="https&#58;//img.shields.io/badge/MCP-2025--03--26-7928CA?style=for-the-badge" alt="MCP Spec" />
  <img src="https&#58;//img.shields.io/badge/Python-3.10+-3776AB?style=for-the-badge&logo=python&logoColor=white" alt="Python Version" />
  <img src="https&#58;//img.shields.io/badge/Zero_API_Keys-Required-00F2FE?style=for-the-badge" alt="Zero API Keys" />
  <img src="https&#58;//img.shields.io/badge/NexusVibe_AI-Jitendra_Kumar-FF0080?style=for-the-badge" alt="NexusVibe AI" />
  <img src="https&#58;//img.shields.io/badge/License-MIT-green?style=for-the-badge" alt="License" />
</p>

---

> **AST Codebase Intelligence, Symbol Extraction, Cyclomatic Complexity & Refactoring Analysis for LLMs & AI Coding Agents.**

---

## 💡 Why This Exists & Token Efficiency

Traditional AI coding assistants dump entire raw source files into context windows, wasting tens of thousands of tokens on boilerplate, imports, and irrelevant functions. **`code-context-mcp`** introduces a **`claude-mem` style 3-layer workflow** that provides surgical code context before editing.

### ⚡ 3-Layer Context Workflow

1. **Layer 1: Structural Scan (`summarize_repository_architecture`)** — High-level file structure, line counts, and extensions map.
2. **Layer 2: AST Symbol Outline (`extract_python_ast_symbols`)** — Class definitions, method signatures, docstrings, and line ranges without dumping raw code.
3. **Layer 3: Targeted Analysis (`analyze_cyclomatic_complexity` & `search_code_todos_and_hotspots`)** — Cyclomatic complexity scores and TODO/FIXME hotspot discovery to pinpoint refactoring targets.

### 📊 Token Savings Comparison

| Approach | Context Injected | Token Usage | Accuracy | Savings |
| :--- | :--- | :--- | :--- | :--- |
| **Naive Raw File Dumping** | Entire source files | ~45,000 tokens | Moderate | 0% |
| **Naive Grep Search** | Raw line matches | ~18,000 tokens | Low | ~60% |
| **`code-context-mcp` AST Workflow** | Exact AST symbols & complexity | ~6,500 tokens | **High** | **~85% Savings** 🚀 |

---

## 🏗️ Architecture Diagram

```mermaid
flowchart TD
    A[AI Coding Agent / LLM] -->|1. Request Repo Summary| B[summarize_repository_architecture]
    A -->|2. Extract AST Symbols| C[extract_python_ast_symbols]
    A -->|3. Analyze Complexity| D[analyze_cyclomatic_complexity]
    A -->|4. Scan Hotspots| E[search_code_todos_and_hotspots]

    subgraph MCP Server Engine: code-context-mcp
        B --> F[AST & Static Code Parser]
        C --> F
        D --> F
        E --> F
    end

    F -->|Compact Structural Context| A
```

---

## 🛠️ Tools Included

1. `summarize_repository_architecture`: Scans directory paths, generates file structure breakdown by extension, and computes total lines of code.
2. `extract_python_ast_symbols`: Parses Python files into Abstract Syntax Trees (AST) to extract classes, base classes, methods, docstrings, function signatures, and line markers.
3. `analyze_cyclomatic_complexity`: Calculates cyclomatic complexity scores for all functions/methods to identify refactoring candidates and branch depth.
4. `search_code_todos_and_hotspots`: Detects code comments containing `TODO`, `FIXME`, `HACK`, and `XXX` across the codebase with exact file and line references.

---

## 🚀 Quick Start (1-Click & 1-Command Setup)

### 1. Claude Code CLI
```bash
claude mcp add code-context-mcp -- python -m code_context_mcp
```

### 2. Cursor (`.cursor/mcp.json`)
```json
{
  "mcpServers": {
    "code-context-mcp": {
      "command": "python",
      "args": ["-m", "code_context_mcp"]
    }
  }
}
```

### 3. OpenAI Codex CLI (`~/.codex/config.toml`)
```toml
[mcp_servers.code-context-mcp]
command = "python"
args = ["-m", "code_context_mcp"]
```

### 4. Google Antigravity IDE (`mcp_config.json`)
```json
{
  "mcpServers": {
    "code-context-mcp": {
      "command": "python",
      "args": ["-m", "code_context_mcp"]
    }
  }
}
```

### 5. Windsurf / Cline
```json
{
  "mcpServers": {
    "code-context-mcp": {
      "command": "python",
      "args": ["-m", "code_context_mcp"]
    }
  }
}
```

---

<div align="center">
  <sub>Built with ❤️ by <b>Jitendra_Kumar • NexusVibe AI</b></sub>
</div>
