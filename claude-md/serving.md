# CLAUDE.md — serving/

Project-specific rules for the qagents AWS cloud-base. Assumes the repo-root `qagents/CLAUDE.md`.

## 1. Single source of truth for AWS

Scope charter: `data/charters/serving/cloud-base/CHARTER.md` (minted 2026-07-20, operator-directed) — the serving governance home: scope map, ownership boundaries, and the spec-family relocation roster (zero relocated at mint; the layers below stay normative until the anchor family closes).

Three layers, each with a distinct job:

- [`data/charters/serving/cloud-base/aws-contract.md`](../data/charters/serving/cloud-base/aws-contract.md) — the **target contract**. Every cloud resource (S3, CloudFront, ACM, Route 53, IAM, EC2, KMS, SSM, CloudWatch) — current and forward-looking — described as we want it to be. Locked decisions, identity model, deploy contracts, scale-up paths, operational runbooks, open work. Companion tests at `data/specs/serving-2026-05-26/tests/`.
- [`INVENTORY.md`](./INVENTORY.md) — the **curated narrative** of current AWS reality. § 8 records known drift items cross-referenced to the spec's § 9 OE-* identifiers. When the spec and reality diverge in a way that's NOT a tracked drift item, the spec is wrong — fix it in the same PR.
- [`inventory/<YYYY-MM-DD>/`](./inventory/) — the **verifiable backing** for INVENTORY.md. Exhaustive structural dump captured by `serving/scripts/aws-snapshot.sh` as **root in CloudShell** (deploy-principal MFA-Deny blocks ACM/R53/IAM/KMS/GuardDuty/SNS/Budgets enumeration). `MANIFEST.md` summarizes census + drift + gaps. Re-run at every phase boundary; the **git diff between two dated snapshots is the canonical change report**.

Two refresh paths:
- Curated (deploy-principal, fast): `pnpm -C serving inventory:fetch` (under `aws-vault exec qagents-deploy --`); prints what `qagents-deploy` can read + a "GAPS" footer enumerating console-only items.
- Ground truth (root, exhaustive): upload `serving/scripts/aws-snapshot.sh` to CloudShell root, `bash aws-snapshot.sh`, download tarball, extract under `serving/inventory/<date>/`, regenerate MANIFEST.md.

Other subprojects' CLAUDE.md files MAY name a single resource (e.g. `documenting/CLAUDE.md` § 5 cites the femfas.net bucket name) but never document AWS configuration — that is `serving/`'s job exclusively.

## 2. Locked decisions live in the spec § 2

The eight locked decisions + the naming-conventions table are load-bearing and live in [`aws-contract.md`](../data/charters/serving/cloud-base/aws-contract.md) §§ Locked decisions / Naming. Change them only by deliberate amendment through the charter lane; never a one-off script tweak.

## 3. Universal tags (every taggable AWS resource)

Tag set, naming table + the `applyUniversalTags(this, {component})` rule (lint checks tag *presence*, not value — an inline `Tags.of(...)` drifts silently): [`aws-contract.md`](../data/charters/serving/cloud-base/aws-contract.md) § Naming (single owner). Reference impl: `cdk/lib/{shared/tags.ts,clips-backup-stack.ts}`.

## 4. Diagram kit (`serving/diagrams/kit/`)

`@qagents/diagram-kit`, the chartered shared-code seam (§ 6) — emit-kind contract, design-bundle location + sync + P4 re-target, and the consumer `pre-X` rebuild rule: `serving/diagrams/kit/README.md` (single owner).

## 5. Diagram prompts are voice-controlled

`serving/diagrams/0X-*.prompt.md` are Claude Design prompts — branding/voice/primitive rules + the Design-round promotion pin: `serving/diagrams/kit/README.md` § "Diagram prompts (voice-controlled)".

## 6. Scope boundary — absolute, no staging

`serving/` does not import from any other subproject; the reverse is also forbidden. The rule is absolute: **no temporary cross-imports, no Phase-A staging step, no workspace-package-as-data-shim.** Cross-subproject contracts are JSON/parquet under `data/<topic>/<sub>.*` only.

The single allowed shared-code seam is `@qagents/diagram-kit`. Both producers (a subproject's `status_emit` script, etc.) and consumers (`designing/web`'s `/status` page) may depend on the kit. That is **not** a cross-subproject import — it's everyone-imports-from-shared-kit.

The CDK app is the only place that references AWS account IDs, ARN literals, or distribution IDs. Subprojects continue to read their bucket name + distribution ID from `serving/sites/<host>.env`, never inline (`INVENTORY.md` § 2 is the curated mirror).

## 7. Status emit (`data/status/serving.json`)

`scripts/status_emit.ts` writes `data/status/serving.json`: three graph-shaped architecture diagrams transcribed from `serving/diagrams/0[1-3]-*.prompt.md` (static-sites / app-api / identity), plus `TableEmit` + `DashboardEmit` panels and a live-state strip, interleaved via an explicit `panels[]` ordering. The exact panel set is pinned by `data/specs/serving-2026-05-26/tests/cases/80-status-emit-shape.sh` — extend the test with the emit.

Per-node `details` is an **HTML string** (rendered by the consumer via Astro's `set:html`, not `{expr}` which would escape entities). Keep detail prose factual — services + costs + scope phrasing matching `data/charters/serving/cloud-base/aws-contract.md`.

Diagram-vs-`TableEmit`-vs-`DashboardEmit` choice: memory `project_diagram_kit` § grid/Table/Dashboard judgment (a rule for every emitter); none of serving's panels is edgeless today.

The summary diagram surfaced on the index card is `static-sites`. Status-pill for serving: `OK` steady-state; `BUILDING` only while a `cdk deploy` is in flight.

## 8. AWS deploys (S3 + CloudFront sites)

Every Astro site under qagents (four today — see `./sites/*.env`; any future sibling) follows the same deploy contract. Per-site bucket + CloudFront distribution differ; the script shape, credential workflow, and verification cadence do not.

**Credential workflow — aws-vault + macOS Keychain (no plaintext keys on disk):**

- **Single unified IAM principal `qagents-deploy`** — one IAM user, two virtual MFA devices (primary + backup), one aws-vault profile, one Keychain entry. Locked at `data/charters/serving/cloud-base/aws-contract.md` § Locked decisions 7 + 8. Blast-radius isolation lives in policy-level MFA-Deny + 1h STS window, not principal multiplication.

  Each site's `<sub>/web/.env` pins `AWS_PROFILE=qagents-deploy` (per-site bucket + distribution IDs stay in `./sites/<host>.env` only — § 6); unified profile block at `./templates/aws-config.snippet`. Same principal pushes to CodeCommit for `qagents` + `dot.claude` (§ 9).

- `aws-vault add <profile>` — long-term IAM keys go to Keychain. `~/.aws/credentials` stays empty.
- `~/.aws/config` is metadata only (no credentials) — shape owned by `./templates/aws-config.snippet`, which says **do NOT add a `[default]` block**: with none, an unwrapped command errors `NoCredentials` instead of silently routing somewhere. A `[default]` drift is invisible precisely because every deploy path is wrapped — live instance (both workstations, removed 2026-08-06): `serving/runbooks/root-account-access.md`. Every deploy command selects `qagents-deploy` explicitly.
- IAM principal carries TWO scoped customer-managed policies (`./policies/qagents-deploy{,-aux}.json`). Split rationale, the 6,144-char cap, Sid list + the self-serve version-push runbook (5-version cap, `LimitExceeded` recovery): `data/charters/serving/cloud-base/aws-contract.md` § Policy model → `./runbooks/policy-version-push.md` § C. **Never** `AmazonS3FullAccess`; never `put-user-policy` against this user — that recreates the retired inline-policy shape (`reference_iam_user_inline_policy_2kb_cap`). **"New grants land in aux" governs NEW grants; a REPAIR to an existing Sid's `Resource`/`Condition` stays in main** — splitting one logical grant across two policies is how the two drift. **Read the ARN in the denial message, never the one you wrote** — a Sid can match live Sid-for-Sid and still be INERT on the one action it names (the v18 account-less `snapshot/*` case: memory `project_serving_subproject`).

**Deploy script shape — `./scripts/deploy-site.sh <host>`** (full contract — env keys, cache policy, invalidation — pinned by `data/specs/serving-2026-05-26/tests/`): sources the committed per-site `./sites/<host>.env`, wipes the bucket (skip: `DEPLOY_NO_WIPE=1`; reversible via bucket versioning), two-pass `aws s3 sync --delete`, then invalidates `/*`. Each site's `package.json` `deploy` runs `pnpm build && bash ../../serving/scripts/deploy-site.sh <host>`.

**Gotcha:** the script adds `--profile` only when **not** running under aws-vault (marker: `AWS_VAULT` env var) — under aws-vault, ambient credentials are present and `--profile` would trigger an empty `~/.aws/credentials` lookup → `Unable to locate credentials`.

Standard invocation: `aws-vault exec qagents-deploy -- pnpm -C <sub>/web deploy`.

**Large binary media — five paths depending on shape** (video-CDN / small-media / clips-backup / archive-backup / CDN-mirror): `data/charters/serving/cloud-base/aws-contract.md` § Media-path routing owns the table + per-path detail.

**Hazard + structural fix — `PROTECTED_PATHS`** (small-media path). Worktrees don't carry gitignored binaries, so a `pnpm deploy` from a fresh worktree runs the wipe + `s3 sync --delete` without them, 404ing the live asset. Fix: a per-site `PROTECTED_PATHS` bash array in `./sites/<host>.env`, threaded as `--exclude` through the wipe AND both sync passes (set on `quantapix.com.env`; femfas.net needs none). Deletion-guard only — binary updates still go via `aws s3 cp` + targeted invalidation.

**Sibling hazard — archive `dir` bundles from canonical only** (root § Canonical-shared gitignored content: walkers must dereference or hard-refuse; a worktree push would tar the link entry alone). `bundle_dir()` hard-fails on a symlinked source and prints the canonical re-invocation; `file` bundles are immune. **Push `parquet` from canonical.** Detail: `data/specs/serving-2026-05-26/artifact-archive-s3-2026-05-29/`; memory `project_parquet_gitignored_ground_truth`.

**`verify` vs `verify-content`.** Different claims — `verify` hashes the compressed TAR (moves with container + mtimes), `verify-content` downloads and compares bytes. Ruling + the DRIFT rules (never re-push to silence, never compare counts across hosts): `data/charters/serving/cloud-base/aws-contract.md` § Archive verify discipline; mechanics + the 80-of-84 pre-pax audit: memory `project_serving_subproject`. **A shared verb whose new flag consumers must adopt to keep a check meaningful owes a "consumers owing adoption" note here** (wrapper axes: `proving/dau.sh`, `accounting/dat.sh`, …).

**CLEAR-4 push-ledger completeness gate — `verify-push-ledger.sh`** (ruling: signoff-framework SPEC § 11 q.2; modes + surfaces in `serving/sites/quantapix.com.env`; pinned by `data/specs/serving-2026-05-26/tests/cases/21-push-ledger-gate.sh`). `deploy-site.sh` runs it **before the wipe** for any site setting `SIGNOFF_LEDGER_GATE=1` (only `quantapix.com.env` today), diffing live S3 objects against `data/publishing/push-ledger.jsonl` — canonical ∪ the `QAGENTS_PENDING_ROOT` overlay (R5). A live object with no ledger line is a breach; **STRICT** on `cdn` aborts pre-wipe (exit 3), `site-thumb` stays report-only pending R16 (spec § 5.4). `push-ledger.jsonl` is a GENERATED projection of `ledger.push_event` — never hand-append. Managing does NOT run this (observe-only on AWS). **Say WHAT you hash:** this ledger's `content_sha256` digests the **pushed binary object itself**; `evaluating/`'s identically-named clearance-record field is a roll-up over that record's `faces[]`. Two digests one level apart sharing a field name is a silent false-negative generator — it read a properly-cleared CDN push as a FALSE `UngatedPush` in `/dao` CLEAR-3f.

**Pre-deploy inventory gate — `predeploy-inventory-gate.sh`** (op:signoff-inventory-home-ruling, sitting 2026-08-18 § O; pinned by `tests/cases/22-predeploy-inventory-gate.sh`). Every-site, before the wipe: live-vs-pinned diff of the resources this deploy touches (bucket reachable · versioning Enabled — the wipe's reversibility · distribution enabled + an origin naming the bucket). Unexplained drift = exit 3 pre-wipe; explained drift escapes via `DEPLOY_SKIP_INVENTORY=1`, printed loudly. Managing reports standing reds, never runs the diff.

**Testing the deploy script — `DEPLOY_DRY_RUN=1`.** Echoes each `aws ...` command instead of executing it and skips the `pnpm build` pre-step. Whole suite: `bash data/specs/serving-2026-05-26/tests/run.sh` (case `20-deploy-site-protected.sh` guards `PROTECTED_PATHS` propagation + `DEPLOY_NO_WIPE=1`, pure bash, no AWS). Companion live-URL e2e: `designing/web/tests/e2e/site.spec.ts` § `large media URLs`.

**Bucket hardening — once per bucket:** `aws-vault exec qagents-deploy -- bash <sub>/web/scripts/setup-bucket-hardening.sh` enables versioning + 30-day noncurrent-version expiration + 7-day multipart-abort. Reference JSON at `./templates/s3-lifecycle-noncurrent-30d.json`.

**New-CloudFront-distribution checklist** → `./runbooks/new-cloudfront-distribution.md`. Pins `reference_cloudfront_function_redirect_pattern`, `reference_cloudfront_404_needs_dest_page`.

**Anchor links need the trailing slash before the hash** (`/route/#x`) — memory `project_playwright_e2e_stack`.

**Live-site smoke test after every deploy.** A clean `pnpm deploy` exit only proves S3 was written + invalidation accepted — not that the site is live. The Playwright suite at `<sub>/web/tests/e2e/` doubles as a deploy verifier; `playwright.config.ts` reads `PW_BASE_URL` and, when set, switches `baseURL` to the remote URL and omits the local `webServer` block entirely:

```
aws-vault exec qagents-deploy -- pnpm -C <sub>/web deploy
PW_BASE_URL=https://<site> pnpm -C <sub>/web test:e2e
```

Mandatory after first-time deploy to a new distribution and any origin/policy touch.

**CI lane — `.github/workflows/deploy-site.yml`** (self-documenting header owns the trigger + `resolve-matrix` detail; pinned by `data/specs/serving-2026-05-26/tests/cases/30-deploy-workflow.sh`). Runs the same `deploy-site.sh` under OIDC role `qagents-deploy-ci` — no long-lived secrets. Two invariants: CI never reimplements deploy mechanics (it shells into `serving/scripts/deploy-site.sh`), and per-site concurrency is `cancel-in-progress: false` — parallel across sites, queued within one, because a half-applied wipe+sync is worse than waiting.

## 8.5. App server deploys (EC2 + Caddy + FastAPI)

Different surface from § 8 static-site deploys. EC2 instance `qagents-app-1` hosts both `verifying/` (qnarre, :8787) and `evaluating/` (qresev, :8788) FastAPI servers behind Caddy on `api.{qnarre,qresev}.quantapix.com`; t4g.small sizing assumes mathlib-free kernels. Full topology: `serving/INVENTORY.md` § 2.5; AMI-drift + the 6-step replacement cycle (incl. the `LEAN_TOOLCHAIN` lockstep bootstrap pre-warms): `data/charters/serving/cloud-base/aws-contract.md` § App-server replacement cycle. Live-state items tracked in `data/next-steps/serving.md`.

**Deploy contract (`aws-contract.md` § Locked decisions — no repo credentials on EC2):**

```bash
aws-vault exec qagents-deploy -- bash serving/scripts/deploy-app.sh {qnarre|qresev|both}
```

- rsync server/ → tarball → `s3://qagents-artifacts/releases/<app>/<sha>.tar.gz` + `latest.tar.gz` pointer
- `aws ssm send-command` runs fetch + atomic-swap + `pip install -r requirements.txt` (only when the tarball ships one — qresev does for pyarrow, qnarre ships none; the EC2 step echoes a loud skip when absent) + `systemctl reload <app>.service`
- Rollback = one-line `aws s3 cp` of the prior tarball over `latest.tar.gz` + re-run deploy-app.sh

**Provisioning the qresev deps + data.** Bootstrap installs only fastapi+uvicorn; `deploy-app.sh qresev` stages `evaluating/requirements.txt` (pyarrow) for the SSM pip step, and the OHLCV tree ships out-of-band via `serving/scripts/ship-parquet.sh` (operator-fired; `SHIP_DRY_RUN=1` dry-run flag). Instance replacement = `bootstrap → deploy-app.sh qresev → ship-parquet.sh`, not archaeology.

**Hazard — kernel rotation wipes post-bootstrap state.** `deploy-app.sh` rotates `/srv/qagents/<kernel>/` into `<kernel>.previous/`, so it must migrate `.lake/` back + `install -d` post-rotation. Failure signature if either step is missing: systemd preflight `status=226/NAMESPACE`. Detail: `feedback_kernel_rotation_cache_hazard`.

**Shell access** is SSM Session Manager only (no SSH on the box):

```bash
aws-vault exec qagents-deploy -- bash serving/scripts/ssm-shell.sh
```

Filters on tag `Name=qagents-app-1`. Requires `session-manager-plugin` installed locally (`brew install --cask session-manager-plugin`).

**Shared ledger store — LAN primary qred `18-main` @ 5432, direct LAN links, no tunnel; qblk `18-main` @ 5432 is the backup/restore-verify peer** (owner: `data/specs/shared-ledger-store-2026-07-09/ledger-lan-primary-2026-07-19/` — topology, TLS/role model, two-tier backups, cutover phases; D-6 residual risk: `data/charters/serving/ledger-lan-primary/d6-disk-encryption-residual-risk.md`). Tooling `serving/scripts/pg-lan/` + `migrate-ledger-to-lan.sh`; runbook `serving/runbooks/ledger-lan-cutover.md`. **RDS frozen + final-snapshotted 2026-08-06; only the date-gated destroy remains** (`ns:serving/30`) — the SSM tunnel machinery SURVIVES it (retirement removes the RDS endpoint, not the lane). DB-gated suites use a disposable DB on qred, never prod. **DSN handling:** one at-rest copy, `~/.config/qagents/ledger.dsn` mode 600, injected per invocation, NEVER exported from a shell profile — `.zshenv` is sourced by every zsh, leaking the password to every process (`data/specs/memsearch-pg-flip-2026-07-21/` amendment).

**Smoke** (live HTTPS via Let's Encrypt cert):

```bash
curl -fsS https://api.qnarre.quantapix.com/api/health
curl -fsS https://api.qresev.quantapix.com/api/health
```

**Operator-policy gaps** — surviving items tracked in `INVENTORY.md` § 8 + `data/next-steps/serving.md` § A; bundled into the next policy-version push per `feedback_operator_policy_gap_per_phase`.

## 8.6. Cron-EC2 lane

Serving/ owns this lane's AWS-touching artifacts; the ownership roster, SSM/timer mechanics, and the t4g.small dual-tenancy `MemoryMax=1500M` hazard: `data/charters/serving/cloud-base/cron-ec2-lane.md` (single owner). Reuses § 8.5's EC2 infra — additive only.

**Operator deploy path** (mirrors § 8.5, single command):

```bash
aws-vault exec qagents-deploy -- bash serving/scripts/deploy-ec2-cron.sh
```

**Two-clock TZ model** — both required layers (ET `OnCalendar=` on every `.timer` AND `Environment=TZ=America/New_York` on every cron `.service`) plus the box-TZ-stays-UTC rule are owned by `data/charters/serving/cloud-base/cron-ec2-lane.md`. Two consequences stated only here: without the *process* pin a 22:00 ET fire computes a next-day date, and `date -u` (RUN_IDs, `_routine.json`) ignores `$TZ`.

## 9. Pushing from the canonical-role holder (qpur by default) — four remotes per repo

Two qagents-class repos (`qagents`, `dot.claude` = `~/.claude/`) push to **four** remotes. Public-org GitHub content pushes via `publishing/scripts/github_meta.py sync` (owned by `publishing/CLAUDE.md` § 4–5; source of truth `publishing/quantapix/`); `git push-quantapix` remains for manual/non-publish pushes only — symlink-clobber hazard below.

```
github  → git@github-qpur:quantapix/<repo>.git           # via ed25519 SSH key
aws     → codecommit::us-east-1://<repo>                 # via aws-vault qagents-deploy
qblk    → qblk:~/repos/<repo>.git                        # via legacy quantapix RSA key
qred    → qred:~/repos/<repo>.git                        # same key; second LAN bare mirror
```

The qblk + qred bare mirrors double as the LAN git-exchange fabric for the network nodes (§ 10). `remote.pushDefault = github`, `push.default = current`. `git push-all` sweeps all four in one command (an unconfigured remote is reported `skip (not configured)` in the summary, not omitted; wraps the `aws` push in `aws-vault exec qagents-deploy --`); wrappers live at `serving/scripts/git-{push-all,push-quantapix,fetch-all}`, symlinked onto PATH at `~/.local/bin/`.

**The roster IS fingerprinted since 2026-08-06 — `parity.sh` `env.remotes`** (sorted remote-NAME set per qagents-class repo, compared outside the same-profile guard). Still `git remote` BOTH repos when provisioning a new host: **a new fingerprint field reads `unmeasured` until BOTH hosts have re-published carrying it**, so the gate is blind to this class on any host whose last publish predates the field. Design rationale (names-not-URLs; the outside-the-guard placement) + why it was needed (qyel sat 3-of-4 undetected behind an all-green `env.wrappers`): memory `project_serving_subproject`.

**Three rules for authoring any cross-host check** (minted 2026-08-06 by checks that were lying) — DEMOTED to the `scripts/parity.sh` header (M-V1, 2026-08-09): the authoring path root CLAUDE.md already sends cross-host-check authors to. Read them there before writing or extending any check; the worked instances (pipx venv root, ~/.local/bin never compared, herdr host-selects-version) travel with them.

**`git fetch --all` is BROKEN by construction — use `git fetch-all`** (ns:serving/72(a)): the `aws` leg needs the aws-vault wrap and git has no per-remote command hook, so push was wrapped from the start and fetch never was. It deliberately omits push-all's hub FF-guard — that guard refuses a divergent *write*, while updating remote-tracking refs is how a divergence is discovered. Sweeper `scripts/push-all.sh` loops it across every qagents-class checkout, folding `--tidy` after. **Fail-closed:** `git push-all` runs the FF-guard before pushing `main` (exit 30). Owner: `data/charters/qagents/push-pull/CHARTER.md` § 2 Mechanics + § ff-guard.

**Key facts that bite (git remotes / MFA / ssh / push bridges) → runbook
`serving/runbooks/git-remotes-and-mfa.md`** (2026-08-09, verbatim): CodeCommit
URL form under aws-vault, the MFA last-device lockout, per-host ssh lockdown,
`git filter-repo` remote strip, and the push-quantapix symlink hazard. Read it
before touching a remote, an MFA device, or a symlink-backed push.

## 10. Local network — qblk / qred / qyel nodes + `ssh aws-1`

This section is entry points + hazards only.

- **Remote sessions:** `bash serving/scripts/net-shell.sh {qblk|qred|qyel|aws-1}` attaches-or-creates the `qagents` tmux session (plain-shell fallback where tmux is absent).
- **LAN reachability is per-APP gated (macOS 15+ Local Network Privacy) — `Undefined error: 0` (errno never set) means a denied grant, not a dead node.** The grant belongs to the app that launched the shell (`cmux.app`), never to `ssh`; first probe is the same command from another app's shell, never a mirror or key investigation. Blast radius, the fix, and the three counter-signatures that RULE IT OUT (a real errno, a diurnal pattern, a launchd subject): memory `reference_macos_local_network_privacy_errno_zero`.
- **`ssh aws-1`** — SSH to `qagents-app-1` over an SSM tunnel (no public port 22; MFA stays the boundary). `Host aws-1` → `serving/scripts/ssm-ssh-proxy.sh` (resolves by Name tag, survives § 8.2 replacement); one-time key install: `serving/runbooks/ec2-ssh-over-ssm.md`; `ssm-shell.sh` remains the zero-setup fallback. Login user `ec2-user`; `sudo -u qagents` for `/srv/qagents`.
- **Git rule:** nodes work on `<node>/<topic>` branches pushed back to the qblk/qred bare mirrors; the canonical-role holder merges in a normal `/open` session and `git push-all` propagates — guarding the AUTHORITY as well as the mirrors and aborting the sweep when it rejects (2026-07-27); `/close` reports an undrained `main` but never pushes. **Non-role-holding** nodes never write `main`. *Canonical is a ROLE, not a hostname* (spec § 4.1; role-capable = {qpur, qyel}), and CR-3 makes the `<root>` checkout path an INVARIANT — every hardcoded canonical path in `scripts/` relies on it. **A lagging `push-all` stalls the whole leaf lane** — check `git rev-list --count qblk/main..main` before relaying `/pull`'s (leaf-shaped) exit-15 remedy a second time.
- **Node bring-up / "works over ssh, fails under launchd":** `runbooks/node-bring-up.md` (owner). Two invariants: an ssh shell and launchd have *different* missing pieces (Keychain / agent / homebrew `PATH`) — probe by absolute path; and sync a node by **pushing from the role holder**, never `git pull` on the node.
- **Node roster projection:** `serving/local-network/nodes.txt` — machine-readable mirror of the spec § 2 roster (consumers: `scripts/pull.sh` ref-scoping, managing AUDIT-C4).
- **LAN backups — runbook `serving/runbooks/lan-durability.md` § LAN backups** (M-V2, 2026-08-09, verbatim extract): backup-to-node/restore contracts + spec cites, the PROSPECTIVE_WAVE_SOURCES lockstep hazard, memsearch-subs LAN-only rule, and the source-host-PREFIX recovery coordinate (incl. the standing add-only deleter warning, `ns:qagents/123` class). Read it before any backup/restore drill.
- **Store durability — runbook `serving/runbooks/lan-durability.md` § Store durability** (M-V2): the three-tier chain, the /do-retire P0 gate coupling, and the conf.d truncation hazard. Read it on any durability alarm.
- **Credential rotation — four rules minted by the 2026-07-30/31 pg loss-and-recovery** (both incidents in full: memory `feedback_one_secret_two_at_rest_copies` § 2026-08-09 + `feedback_assert_hostname_before_host_scoped_secret_write` + `project_serving_subproject`). (a) Assert `hostname` FIRST before rewriting a host-scoped secret seat. (b) Verify by **live probe from each seat host, per PORT** — a hash compare is structurally blind, because the authority is the SERVER ROLE, not either at-rest file. (c) `provision-pg-lan.sh` is committed mode 644, so the recipe is `sudo bash <path>`, never `sudo <path>`. (d) **The sweep unit is the CLUSTER holding the role, not the host holding the file** — qblk runs two (`18/main` @5432, `18/verify` @5433), each with its own `qagents` role, and the missed half is the one no DAILY lane exercises; remedy `ALTER ROLE qagents PASSWORD …` in the affected cluster only (heredoc — `psql -c` does not interpolate `:'pw'`).
- Sibling cron `serving:ledger-daily` 05:20 daily — `qagents.ledger.import_logs` + `flush` (spool drain) against the LAN DSN (`~/.config/qagents/ledger.dsn`, direct qred link, no MFA/tunnel); mechanics: `data/specs/shared-ledger-store-2026-07-09/`.
- **Postgres:** topology, RDS-retirement state + DSN handling are owned by § 8.5 § Shared ledger store above (single owner in this file); provisioning `scripts/provision-pg-lan-push.sh {qred|qblk}`. **Since 2026-07-28 the store also carries `archive.blob`/`archive.sweep`** (`code/ledger/.../schema/006_archive.sql`), `/do-retire`'s durability tier for **untracked** content — and the split is the load-bearing part: `recoverable=none` lanes are the ONLY copy while the rest are `recoverable=git` projections, so a drill exercising the table as one population under-tests exactly the lanes that matter. Take the per-lane split from `data/specs/do-retire-2026-07-26/lanes.tsv` col 4, never from a remembered figure.
- **Mirror-guard:** `bash serving/scripts/harden-mirrors.sh [--verify]` — per-ref `update` hook on both nodes' `qagents.git` + `dot.claude.git` protecting `refs/heads/main` (non-FF + delete refused; `<node>/*` stays deletable for `/pull --tidy`). Installed + live-verified 2026-07-20 (ns-27).
