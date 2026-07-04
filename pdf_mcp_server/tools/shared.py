from __future__ import annotations

from pathlib import Path

# Root folder the MCP server is allowed to access.
# Keep all test PDFs inside this folder for safety.
WORKSPACE = Path(__file__).resolve().parents[1] / "workspace"
WORKSPACE.mkdir(exist_ok=True)


def _safe_path(relative_path: str) -> Path:
    """Resolve a path inside WORKSPACE and prevent path traversal."""
    path = (WORKSPACE / relative_path).resolve()
    workspace_root = WORKSPACE.resolve()
    if not str(path).startswith(str(workspace_root)):
        raise ValueError("Access denied: path must stay inside the workspace folder.")
    return path


def _ensure_pdf(path: Path) -> None:
    if path.suffix.lower() != ".pdf":
        raise ValueError("Only PDF files are allowed.")
