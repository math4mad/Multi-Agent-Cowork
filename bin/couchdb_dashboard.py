#!/usr/bin/env python3
"""Serve the dashboard and proxy read-only requests to local CouchDB."""

from __future__ import annotations

import http.server
import json
import urllib.error
import urllib.request
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DOCS = ROOT / "docs"
COUCHDB = "http://127.0.0.1:5984"


class DashboardHandler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=str(DOCS), **kwargs)

    def do_GET(self) -> None:
        if self.path.startswith("/api/"):
            self.proxy_couchdb()
            return
        if self.path == "/":
            self.path = "/couchdb.html"
        super().do_GET()

    def proxy_couchdb(self) -> None:
        target = COUCHDB + self.path.removeprefix("/api")
        try:
            with urllib.request.urlopen(target, timeout=3) as response:
                body = response.read()
                self.send_response(response.status)
                self.send_header("Content-Type", response.headers.get("Content-Type", "application/json"))
                self.send_header("Content-Length", str(len(body)))
                self.end_headers()
                self.wfile.write(body)
        except (urllib.error.URLError, TimeoutError, OSError) as error:
            body = json.dumps({"error": "couchdb_unavailable", "reason": str(error)}).encode()
            self.send_response(503)
            self.send_header("Content-Type", "application/json")
            self.send_header("Content-Length", str(len(body)))
            self.end_headers()
            self.wfile.write(body)


if __name__ == "__main__":
    server = http.server.ThreadingHTTPServer(("127.0.0.1", 8766), DashboardHandler)
    print("CouchDB dashboard: http://127.0.0.1:8766")
    server.serve_forever()