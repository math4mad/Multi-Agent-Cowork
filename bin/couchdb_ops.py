#!/usr/bin/env python3
"""Small authenticated CouchDB operations for the cowork wire."""

from __future__ import annotations

import argparse
import base64
import json
import os
import sys
import urllib.error
import urllib.parse
import urllib.request
from pathlib import Path


DEFAULT_URL = "http://127.0.0.1:5984"
WIRE_DATABASES = ("cowork_presence", "cowork_board", "cowork_inbox")
INDEX_DATABASE = "cowork_index"
ROOT = Path(__file__).resolve().parents[1]
WIRE_SOURCE_DIRECTORIES = {
    "cowork_board": ROOT / "docs" / "board",
    "cowork_inbox": ROOT / "docs" / "inbox",
}


class CouchDBError(RuntimeError):
    pass


class CouchDB:
    def __init__(self, url: str, user: str, password: str):
        self.url = url.rstrip("/")
        self.auth = base64.b64encode(f"{user}:{password}".encode()).decode()

    def request(self, method: str, path: str, body: object | None = None) -> object:
        payload = None if body is None else json.dumps(body).encode()
        request = urllib.request.Request(
            f"{self.url}{path}",
            data=payload,
            method=method,
            headers={
                "Accept": "application/json",
                "Authorization": f"Basic {self.auth}",
                "Content-Type": "application/json",
            },
        )
        try:
            with urllib.request.urlopen(request, timeout=5) as response:
                raw = response.read()
        except urllib.error.HTTPError as error:
            detail = error.read().decode(errors="replace")
            raise CouchDBError(f"{error.code} {error.reason}: {detail}") from error
        except urllib.error.URLError as error:
            raise CouchDBError(f"cannot reach CouchDB: {error.reason}") from error
        return json.loads(raw) if raw else {}

    def ensure_database(self, name: str) -> object:
        encoded = urllib.parse.quote(name, safe="")
        try:
            return self.request("PUT", f"/{encoded}")
        except CouchDBError as error:
            if str(error).startswith("412 "):
                return {"ok": True, "already_exists": True, "db": name}
            raise

    def put_document(self, database: str, document_id: str, document: dict[str, object]) -> object:
        encoded_database = urllib.parse.quote(database, safe="")
        encoded_id = urllib.parse.quote(document_id, safe="")
        return self.request("PUT", f"/{encoded_database}/{encoded_id}", document)

    def upsert_document(self, database: str, document_id: str, document: dict[str, object]) -> object:
        try:
            existing = self.get_document(database, document_id)
            if isinstance(existing, dict) and "_rev" in existing:
                document = {**document, "_rev": existing["_rev"]}
        except CouchDBError as error:
            if not str(error).startswith("404 "):
                raise
        return self.put_document(database, document_id, document)

    def get_document(self, database: str, document_id: str) -> object:
        encoded_database = urllib.parse.quote(database, safe="")
        encoded_id = urllib.parse.quote(document_id, safe="")
        return self.request("GET", f"/{encoded_database}/{encoded_id}")

    def changes(self, database: str, limit: int) -> object:
        encoded_database = urllib.parse.quote(database, safe="")
        return self.request("GET", f"/{encoded_database}/_changes?limit={limit}")


def client_from_environment(args: argparse.Namespace) -> CouchDB:
    password = os.environ.get("COUCHDB_PASSWORD")
    if not password:
        raise CouchDBError("set COUCHDB_PASSWORD; credentials are never read from source files")
    return CouchDB(
        args.url or os.environ.get("COUCHDB_URL", DEFAULT_URL),
        os.environ.get("COUCHDB_USER", "admin"),
        password,
    )


def print_json(value: object) -> None:
    print(json.dumps(value, indent=2, sort_keys=True))


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--url", help="CouchDB URL; defaults to COUCHDB_URL or localhost")
    subparsers = parser.add_subparsers(dest="command", required=True)

    subparsers.add_parser("init-wire", help="create the standard cowork wire databases")

    put_parser = subparsers.add_parser("put", help="write one JSON document owned by a writer")
    put_parser.add_argument("database")
    put_parser.add_argument("document_id")
    put_parser.add_argument("json_file", help="JSON object to write")

    get_parser = subparsers.add_parser("get", help="read one document")
    get_parser.add_argument("database")
    get_parser.add_argument("document_id")

    changes_parser = subparsers.add_parser("changes", help="read recent database changes")
    changes_parser.add_argument("database")
    changes_parser.add_argument("--limit", type=int, default=25)

    index_parser = subparsers.add_parser("sync-index", help="upsert _index/files.json into CouchDB")
    index_parser.add_argument("index_file", nargs="?", default="_index/files.json")

    subparsers.add_parser("seed-wire", help="upsert committed board and inbox records into CouchDB")

    args = parser.parse_args()
    try:
        couch = client_from_environment(args)
        if args.command == "init-wire":
            print_json({name: couch.ensure_database(name) for name in (*WIRE_DATABASES, INDEX_DATABASE)})
        elif args.command == "put":
            document = json.loads(open(args.json_file, encoding="utf-8").read())
            if not isinstance(document, dict):
                raise CouchDBError("document JSON must be an object")
            print_json(couch.put_document(args.database, args.document_id, document))
        elif args.command == "get":
            print_json(couch.get_document(args.database, args.document_id))
        elif args.command == "changes":
            print_json(couch.changes(args.database, args.limit))
        elif args.command == "sync-index":
            index = json.loads(open(args.index_file, encoding="utf-8").read())
            records = index.get("records") if isinstance(index, dict) else None
            if not isinstance(records, list):
                raise CouchDBError("index file must contain a records list")
            couch.ensure_database(INDEX_DATABASE)
            results = [
                couch.upsert_document(INDEX_DATABASE, record["_id"], record)
                for record in records
                if isinstance(record, dict) and isinstance(record.get("_id"), str)
            ]
            print_json({"database": INDEX_DATABASE, "upserted": len(results)})
        else:
            seeded = {}
            for database, directory in WIRE_SOURCE_DIRECTORIES.items():
                couch.ensure_database(database)
                documents = []
                for path in sorted(directory.glob("*.json")):
                    document = json.loads(path.read_text(encoding="utf-8"))
                    if not isinstance(document, dict):
                        raise CouchDBError(f"{path} must contain a JSON object")
                    documents.append(couch.upsert_document(database, path.stem, document))
                seeded[database] = len(documents)
            print_json({"seeded": seeded})
    except (CouchDBError, OSError, json.JSONDecodeError) as error:
        print(f"ERROR: {error}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())