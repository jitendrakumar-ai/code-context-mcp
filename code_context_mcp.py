import sys
import json
import os
import ast

def handle_request(request):
    method = request.get("method")
    req_id = request.get("id")

    if method == "initialize":
        return {
            "jsonrpc": "2.0",
            "id": req_id,
            "result": {
                "protocolVersion": "2024-11-05",
                "capabilities": {"tools": {}},
                "serverInfo": {"name": "code-context-mcp", "version": "1.0.0"}
            }
        }

    elif method == "notifications/initialized":
        return None

    elif method == "tools/list":
        return {
            "jsonrpc": "2.0",
            "id": req_id,
            "result": {
                "tools": [
                    {
                        "name": "summarize_repository_architecture",
                        "description": "Analyze directory architecture, file structure, extensions, and lines of code.",
                        "inputSchema": {
                            "type": "object",
                            "properties": {
                                "root_path": {"type": "string", "default": "."}
                            }
                        }
                    },
                    {
                        "name": "extract_python_ast_symbols",
                        "description": "Extract AST classes, functions, docstrings, decorators, and signatures from Python source.",
                        "inputSchema": {
                            "type": "object",
                            "properties": {
                                "file_path": {"type": "string"},
                                "code_content": {"type": "string"}
                            }
                        }
                    },
                    {
                        "name": "analyze_cyclomatic_complexity",
                        "description": "Calculate cyclomatic complexity score for Python functions and methods using AST.",
                        "inputSchema": {
                            "type": "object",
                            "properties": {
                                "file_path": {"type": "string"},
                                "code_content": {"type": "string"}
                            }
                        }
                    },
                    {
                        "name": "search_code_todos_and_hotspots",
                        "description": "Find TODO, FIXME, HACK comments, and high-complexity refactoring hotspots.",
                        "inputSchema": {
                            "type": "object",
                            "properties": {
                                "root_path": {"type": "string", "default": "."}
                            }
                        }
                    }
                ]
            }
        }

    elif method == "tools/call":
        params = request.get("params", {})
        tool_name = params.get("name")
        args = params.get("arguments", {})

        if tool_name == "summarize_repository_architecture":
            res = summarize_repository_architecture(args.get("root_path", "."))
        elif tool_name == "extract_python_ast_symbols":
            res = extract_python_ast_symbols(args.get("file_path"), args.get("code_content"))
        elif tool_name == "analyze_cyclomatic_complexity":
            res = analyze_cyclomatic_complexity(args.get("file_path"), args.get("code_content"))
        elif tool_name == "search_code_todos_and_hotspots":
            res = search_code_todos_and_hotspots(args.get("root_path", "."))
        else:
            res = {"error": f"Unknown tool: {tool_name}"}

        return {
            "jsonrpc": "2.0",
            "id": req_id,
            "result": {
                "content": [{"type": "text", "text": json.dumps(res, indent=2)}]
            }
        }

    return {
        "jsonrpc": "2.0",
        "id": req_id,
        "error": {"code": -32601, "message": "Method not found"}
    }

def summarize_repository_architecture(root_path="."):
    if not os.path.exists(root_path):
        return {"error": f"Path '{root_path}' does not exist."}
    extension_counts = {}
    total_files = 0
    total_lines = 0
    for root, dirs, files in os.walk(root_path):
        dirs[:] = [d for d in dirs if not d.startswith('.') and d not in ('node_modules', '__pycache__', 'venv')]
        for file in files:
            total_files += 1
            ext = os.path.splitext(file)[1] or 'no_ext'
            extension_counts[ext] = extension_counts.get(ext, 0) + 1
            fp = os.path.join(root, file)
            try:
                with open(fp, 'r', encoding='utf-8', errors='ignore') as f:
                    total_lines += sum(1 for _ in f)
            except Exception:
                pass
    return {
        "root_path": root_path,
        "total_files": total_files,
        "total_lines_of_code": total_lines,
        "file_extensions": extension_counts
    }

def extract_python_ast_symbols(file_path=None, code_content=None):
    code = ""
    if file_path and os.path.exists(file_path):
        with open(file_path, 'r', encoding='utf-8') as f:
            code = f.read()
    elif code_content:
        code = code_content
    else:
        return {"error": "No Python file or code content provided."}
    try:
        tree = ast.parse(code)
    except Exception as e:
        return {"error": f"Syntax / Parse Error: {str(e)}"}
    classes = []
    functions = []
    for node in ast.walk(tree):
        if isinstance(node, ast.ClassDef):
            classes.append({
                "name": node.name,
                "bases": [b.id for b in node.bases if isinstance(b, ast.Name)],
                "docstring": ast.get_docstring(node),
                "line": node.lineno
            })
        elif isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
            functions.append({
                "name": node.name,
                "args": [a.arg for a in node.args.args],
                "docstring": ast.get_docstring(node),
                "line": node.lineno
            })
    return {"classes": classes, "functions": functions}

def analyze_cyclomatic_complexity(file_path=None, code_content=None):
    code = ""
    if file_path and os.path.exists(file_path):
        with open(file_path, 'r', encoding='utf-8') as f:
            code = f.read()
    elif code_content:
        code = code_content
    else:
        return {"error": "No source code provided."}
    try:
        tree = ast.parse(code)
    except Exception as e:
        return {"error": f"AST Parse Error: {str(e)}"}
    complexity_results = []
    for node in ast.walk(tree):
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
            complexity = 1
            for child in ast.walk(node):
                if isinstance(child, (ast.If, ast.For, ast.While, ast.And, ast.Or, ast.ExceptHandler, ast.With)):
                    complexity += 1
            complexity_results.append({
                "function_name": node.name,
                "line": node.lineno,
                "cyclomatic_complexity": complexity,
                "rating": "Low" if complexity <= 5 else "Moderate" if complexity <= 10 else "High"
            })
    return {"functions_complexity": complexity_results}

def search_code_todos_and_hotspots(root_path="."):
    if not os.path.exists(root_path):
        return {"error": f"Path '{root_path}' does not exist."}
    todos = []
    keywords = ["TODO", "FIXME", "HACK", "XXX"]
    for root, dirs, files in os.walk(root_path):
        dirs[:] = [d for d in dirs if not d.startswith('.') and d not in ('node_modules', '__pycache__', 'venv')]
        for file in files:
            if file.endswith(('.py', '.js', '.ts', '.md', '.go', '.rs')):
                fp = os.path.join(root, file)
                try:
                    with open(fp, 'r', encoding='utf-8', errors='ignore') as f:
                        for idx, line in enumerate(f, 1):
                            for kw in keywords:
                                if kw in line:
                                    todos.append({"file": fp, "line": idx, "keyword": kw, "content": line.strip()})
                except Exception:
                    pass
    return {"total_todos_found": len(todos), "todos": todos[:20]}

def main():
    for line in sys.stdin:
        if not line.strip():
            continue
        try:
            req = json.loads(line)
            res = handle_request(req)
            if res:
                sys.stdout.write(json.dumps(res) + "\n")
                sys.stdout.flush()
        except Exception as e:
            err_res = {
                "jsonrpc": "2.0",
                "id": None,
                "error": {"code": -32700, "message": f"Parse error: {str(e)}"}
            }
            sys.stdout.write(json.dumps(err_res) + "\n")
            sys.stdout.flush()

if __name__ == "__main__":
    main()
