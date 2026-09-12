# Multi-Agent-Cowork

A distributed cowork workspace for three bench repositories:

- Research / Irene: paper indexes and pinned sample data
- EDA / Nikos: reproducible visualization notes
- Audit / Thea: data-flow, ownership, and sync evidence

Git is the record. CouchDB is the rebuildable local wire. The static project
homepage is in [`docs/index.html`](docs/index.html), and the dedicated EDA note
is [`docs/eda.html`](docs/eda.html).

## Local views

```bash
python3 -m http.server 8766 --directory docs
```

Then open `http://127.0.0.1:8766/`.

The CouchDB dashboard is served by `bin/couchdb_dashboard.py` when CouchDB is
running on port 5984. Team membership steps are in
[`docs/team-onboarding.md`](docs/team-onboarding.md).

## Benches

The bench repositories are published separately:

- https://github.com/math4mad/research-irene
- https://github.com/math4mad/eda-nikos
- https://github.com/math4mad/audit-thea
