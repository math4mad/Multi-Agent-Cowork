# Cowork Completion Checklist

This checklist is the current execution view of `RealWork.md` and `AGENTS.md`.
The database is a rebuildable wire; Git records remain authoritative.

## Current Cycle

- [x] Run the Research -> EDA analysis on `m1-16g`.
- [x] Produce the EDA report and citation figure.
- [x] Record the cross-project operation in Audit.
- [x] Run the six-check data-flow audit.
- [x] Run the four-check ownership smoke test.
- [x] Rebuild the 32-record workspace index.
- [x] Validate both machine presence records.
- [x] Commit and push the refreshed Audit evidence (`77a1328`).
- [ ] Publish the board and inbox records to CouchDB. The seed command is ready;
      the local terminal is waiting for the admin password.
- [ ] Verify CouchDB document counts for `cowork_presence`, `cowork_board`,
      `cowork_inbox`, and `cowork_index`.

## Membership And Liveness

- [x] Keep one unique presence record per machine.
- [x] Record the `m1-16g` workhorse capabilities and one trainer slot.
- [x] Run the presence audit.
- [ ] Make `docs/status.json` agree with `docs/presence/m1-16g.json` (`working`
      versus `quiet`).
- [ ] Add a repeatable heartbeat command that refreshes `beat_iso` and publishes
      the presence document.
- [ ] Demonstrate the third liveness state: `silent since <t>` from the other
      machine after a heartbeat expires.
- [ ] Add machine claim records before accepting new machine IDs.
- [ ] Record Python, NumPy, Torch, MPS/CUDA, network, timezone, and clock ID
      capabilities where available.

## Wire And Records

- [x] Create the committed board source record.
- [x] Create the committed inbox source record.
- [x] Add the reproducible `seed-wire` command.
- [ ] Seed `cowork_board` and `cowork_inbox` from Git.
- [ ] Publish both presence records to `cowork_presence`.
- [ ] Sync `_index/files.json` to `cowork_index`.
- [ ] Add `git_anchor` and `sha256` to every cross-project board and inbox
      document, then verify the digests against Git bytes.
- [ ] Add a queue snapshot under `docs/queue/` and commit it daily.
- [ ] Add an `_acks` representation and record a receiver acknowledgement for
      the current inbox announcement.
- [ ] Add claim records for machine, task, and letter IDs before use.
- [ ] Delete all wire databases and prove they rebuild byte-for-byte from Git.

## Dashboard

- [x] Keep the static homepage available without CouchDB.
- [x] Keep the local CouchDB dashboard available on port `8766`.
- [ ] Make the dashboard proxy authenticate to admin-protected CouchDB databases.
- [ ] Show per-machine presence and `silent since` state.
- [ ] Show board columns and unacked inbox count.
- [ ] Show the last verified byte-audit timestamp.
- [ ] Verify the dashboard with populated databases, not only the empty-db state.

## Reversibility And Cross-Machine Proof

- [x] Keep Git remotes and pushed bench history.
- [ ] Create a dated pause tag on all three bench repositories before the next
      damaging or experimental thread.
- [ ] Create bundles outside the repositories and a `SHA256SUMS` file.
- [x] Complete a restore drill on `m1-16g`.
- [ ] Complete the same restore drill on `m1pro-32g`.
- [ ] Publish the bundle SHAs and drill results in Audit.
- [ ] Test a two-writer conflict and retain/display the conflict without forcing
      a winner.

## Acceptance Tests Still Missing

- [ ] A1: answer law, dirty bench, mail, unacked work, and machine liveness from
      indexes/queries without opening prose files.
- [ ] A2: prove `silent since` from the other machine.
- [ ] A3: query an inbox event and its acknowledgement.
- [ ] A4: delete both wire databases, rebuild from Git, and compare digests.
- [ ] A5: retain and display a write-domain conflict.
- [ ] A6: race two claims for the same ID and make one lose before commit.
- [ ] A7: reject a changed pinned file without a matching re-pin.
- [ ] A8: run the existing programme-law checks with the database populated.
- [ ] A9: pass the rollback drill on both machines using the same day's bundles.

## Recommended Next Actions

1. Enter the CouchDB admin password in the waiting terminal and run the pending
   seed and count verification.
2. Add hashes and Git anchors to the board/inbox source records, then reseed.
3. Fix the status/presence state mismatch and add heartbeat publication.
4. Add queue, ack, claim, and restore-drill records.
5. Authenticate the custom dashboard and run the populated-dashboard check.