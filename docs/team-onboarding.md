# Add A Team Member

Use this guide when adding another person or Mac to the cowork fleet. The new
member gets its own machine ID and owns its own presence, claims, acknowledgements,
and bench work. Do not reuse `m1-16g` or `m1pro-32g`.

## 1. Choose A Machine ID

Machine IDs are minted from hardware identity. First check the existing IDs:

```bash
find docs/presence -name '*.json' -maxdepth 1 -print
```

Choose a new ID only after confirming it is not already present. Record the
hardware model and first-seen UTC time in the new claim document before using
the ID in a board item.

## 2. Clone The Record And Benches

```bash
git clone https://github.com/math4mad/Multi-Agent-Cowork.git cowork
cd cowork
git clone https://github.com/math4mad/research-irene.git research-irene
git clone https://github.com/math4mad/eda-nikos.git eda-nikos
git clone https://github.com/math4mad/audit-thea.git audit-thea
```

If the workspace repository is not published, obtain the current workspace
bundle from the owner and verify its SHA-256 before consuming it.

## 3. Probe The New Machine

Record these facts in `docs/presence/<machine-id>.json`:

```bash
uname -m
sw_vers -productVersion
sysctl -n hw.model hw.memsize hw.ncpu
date -u +%Y-%m-%dT%H:%M:%SZ
df -k / | awk 'NR==2 {printf "free_bytes_gib=%.1f\\n", ($4 * 1024) / (1024^3)}'
```

The record must include `machine`, `hwid`, `state`, `beat_iso`, `head`,
`free_bytes_gib`, `ram_bytes`, and `running_pids`. Add accelerator, trainer
slot, timezone, clock, Python, NumPy, and Torch details when available.

## 4. Verify Before Joining

Run the local checks before publishing membership:

```bash
python3 bin/build_index.py
python3 bin/audit.py
python3 audit-thea/checks/sync_smoke.py
python3 audit-thea/checks/data_flow.py
```

Independently verify at least one indexed byte that the new member did not
produce. Compare its SHA-256 with `_index/files.json`; a successful clone alone
is not membership proof.

## 5. Restore Drill

Before doing risky work, obtain the newest bundle set and restore each bench in
a temporary directory. Compare the restored HEAD with the recorded bundle HEAD.
Publish the result in `audit-thea/runs/` and state whether the drill ran on this
machine. A drill on only one machine is not the final fleet proof.

## 6. Publish Presence

Ask the local CouchDB owner for the admin password and type it directly into the
terminal. Never put it in a file or chat:

```bash
export COUCHDB_USER=admin
read -s COUCHDB_PASSWORD
export COUCHDB_PASSWORD
python3 bin/couchdb_ops.py init-wire
python3 bin/couchdb_ops.py put cowork_presence <machine-id> docs/presence/<machine-id>.json
python3 bin/couchdb_ops.py changes cowork_presence --limit 25
unset COUCHDB_PASSWORD COUCHDB_USER
```

The new member is not considered active until its presence document is visible
and its record commit is available to the other member.

## 7. Take A Task

Choose a board item whose requirements fit the new machine's capability vector.
Before writing, check that no other writer owns the same path and that the
machine has a free trainer slot. Write the board item and all results under the
new machine's own document ID, then commit and push the bench repository.

For a first low-risk task, run the read-only workhorse cycle:

```bash
python3 eda-nikos/bin/analyze.py
python3 audit-thea/checks/cross_project_operation.py
python3 audit-thea/checks/data_flow.py
python3 audit-thea/checks/sync_smoke.py
python3 bin/build_index.py
python3 bin/audit.py
```

## 8. Heartbeat And Handoff

Refresh `beat_iso` while working and set `state` to `quiet` when stopping. If
heartbeats expire, the fleet must show `silent since <t>`, not silently remove
the member. For every inbox announcement, the receiver publishes an ack naming
the record commit and the letter IDs it read.

A successful onboarding ends with these facts published:

- unique machine ID and claim
- verified presence record
- at least one independently verified indexed byte
- restore-drill result
- current heartbeat
- first task result and owning commit
- acknowledgement of the onboarding announcement
