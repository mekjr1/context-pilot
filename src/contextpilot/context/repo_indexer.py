import hashlib
from pathlib import Path

IGNORE = {".git", "node_modules", ".venv", "__pycache__", "vendor", "dist", "build"}


def guess_language(path: Path) -> str:
    mapping = {".py": "python", ".ts": "typescript", ".js": "javascript", ".md": "markdown"}
    return mapping.get(path.suffix.lower(), "text")


def index_repo(path: str):
    output = []
    for file_path in Path(path).rglob("*"):
        if not file_path.is_file() or any(part in IGNORE for part in file_path.parts):
            continue
        content_hash = ""
        try:
            content_hash = hashlib.sha256(file_path.read_bytes()).hexdigest()
        except OSError:
            content_hash = ""
        output.append(
            {
                "path": str(file_path),
                "size": file_path.stat().st_size,
                "language": guess_language(file_path),
                "hash": content_hash,
            }
        )
    return output


def search_repo(path: str, query: str):
    matches = []
    for row in index_repo(path):
        try:
            text = Path(row["path"]).read_text(errors="ignore")
        except OSError:
            continue
        if query.lower() in text.lower():
            matches.append(row)
    return matches
