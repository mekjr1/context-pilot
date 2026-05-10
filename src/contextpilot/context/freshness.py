import hashlib
import os

import httpx

from contextpilot.storage.repositories import write_freshness_check


def check_source(source: str):
    if source.startswith("http"):
        response = httpx.head(source, follow_redirects=True, timeout=5)
        result = {
            "type": "web_url",
            "status": response.status_code,
            "etag": response.headers.get("etag"),
            "last_modified": response.headers.get("last-modified"),
        }
        write_freshness_check(source, "web_url", result)
        return result
    if os.path.exists(source):
        with open(source, "rb") as file_handle:
            payload = file_handle.read()
        result = {
            "type": "local_file",
            "hash": hashlib.sha256(payload).hexdigest(),
            "mtime": os.path.getmtime(source),
        }
        write_freshness_check(source, "local_file", result)
        return result
    result = {"type": "git_repo", "source": source}
    write_freshness_check(source, "git_repo", result)
    return result
