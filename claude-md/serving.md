# CLAUDE.md — serving/

Project-specific rules for the qagents AWS cloud-base. Assumes the repo-root `qagents/CLAUDE.md`.

## 1. Single source of truth for AWS

Scope charter: `data/charters/serving/cloud-base/CHARTER.md` (minted 2026-07-20, operator-directed) — the serving governance home: scope map, ownership boundaries, and the spec-family relocation roster (zero relocated at mint; the layers below stay normative until the anchor family closes).

Three layers, each with a distinct job:

- [`data/specs/serving-2026-05-26/SPEC.md`](../data/specs/serving-2026-05-26/SPEC.md) — the **target contract**. Every cloud resource (S3, CloudFront, ACM, Route 53, IAM, EC2, KMS, SSM, CloudWatch) — current and forward-looking — described as we want it to be. Locked decisions, identity model, deploy contracts, scale-up paths, operational runbooks, open work. Companion tests at `data/specs/serving-2026-05-26/tests/`.
- [`INVENTORY.md`](./INVENTORY.md) — the **curated narrative** of current AWS reality. § 8 records known drift items cross-referenced to the spec's § 9 OE-* identifiers. When the spec and reality diverge in a way that's NOT a tracked drift item, the spec is wrong — fix it in the same PR.
- [`inventory/<YYYY-MM-DD>/`](./inventory/) — the **verifiable backing** for INVENTORY.md. Exhaustive structural dump captured by `serving/scripts/aws-snapshot.sh` as **root in CloudShell** (deploy-principal MFA-Deny blocks ACM/R53/IAM/KMS/GuardDuty/SNS/Budgets enumeration). `MANIFEST.md` summarizes census + drift + gaps. Re-run at every phase boundary; the **git diff between two dated snapshots is the canonical change report**.

Two refresh paths:
- Curated (deploy-principal, fast): `pnpm -C serving inventory:fetch` (under `aws-vault exec qagents-deploy --`); prints what `qagents-deploy` can read + a "GAPS" footer enumerating console-only items.
- Ground truth (root, exhaustive): upload `serving/scripts/aws-snapshot.sh` to CloudShell root, `bash aws-snapshot.sh`, download tarball, extract under `serving/inventory/<date>/`, regenerate MANIFEST.md.

Other subprojects' CLAUDE.md files MAY name a single resource (e.g. `documenting/CLAUDE.md` § 5 cites the femfas.net bucket name) but never document AWS configuration — that is `serving/`'s job exclusively.

## 2. Locked decisions live in the spec § 2

The decisions (OIDC role for CI, build-tarball deploys, Caddy not nginx, no Cloudflare, CDK in TypeScript, single shared EC2, unitary `qagents-deploy` IAM principal, ≥2 virtual MFA devices) and the naming-conventions table are load-bearing. Change them only via a deliberate amendment to `data/specs/serving-2026-05-26/SPEC.md`; never via a one-off script tweak.

## 3. Universal tags (every taggable AWS resource)

```
Project   = qagents
Owner     = quantapix
Env       = prod
Component = site | app | shared | identity | monitoring
ManagedBy = cdk | manual
```

Applied centrally from `cdk/lib/shared/tags.ts`. Any resource missing one fails `cdk synth` lint. `ManagedBy=manual` is reserved for legacy resources awaiting CDK adoption.

Every new stack MUST call `applyUniversalTags(this, {component: '<c>'})` from `cdk/lib/shared/tags.ts` — lint enforces tag *presence*, not value, so an inline `Tags.of(...).add('Owner', 'qpix')` would pass silently while violating canonical values. Reference: `cdk/lib/clips-backup-stack.ts`.

## 4. Diagram kit (`serving/diagrams/kit/`)

The Quantapix-branded diagram primitives + layouts live here, packaged as the `@qagents/diagram-kit` workspace pnpm package. It is the legitimate shared-code seam for cross-subproject diagram primitives + the kit-owned status-hub schema — sibling-of-subprojects, not `serving/`-internal. Anyone (designing/web, explaining/, future consumers) may import it; see § 6.

The kit's display-mode contract — the closed set of `*Emit` schemas it ships vs. what stays consumer-owned (Chart, Graph, 3D-mix, Video, App-shell) — is fixed by `data/specs/display-modes-2026-05-07/SPEC.md`. Adding a new emit kind requires a kit minor version bump + spec amendment + e2e coverage.

The kit's source-of-truth design bundle lives at `data/renders/serving-design/` (read-only, regen-wholesale; moves to `rendering/designs/serving-diagrams/` at the serving P4 slot). Sync procedure: `serving/diagrams/kit/README.md` § "Sync with the design bundle".

**Consumers must rebuild the kit before their own typecheck/build/dev** — the kit emits to gitignored `dist/` and `pnpm install` does not auto-build workspace packages. Adopted pattern: `pre-X` hooks in every consumer's `package.json` running `pnpm -F @qagents/diagram-kit build` (rationale + rejected src/-pointing alternative: `reference_kit_build_consumer_pre_x`).

## 5. Diagram prompts are voice-controlled

`serving/diagrams/0X-*.prompt.md` are Claude Design prompts. They enforce Quantapix branding (BracketedQ glyph, approved brand names only), engineer-debugging-a-system voice on labels (no marketing fluff), and the shape-agnostic Node primitive (no AWS-service glyphs).

When iterating a Design return on a diagram bundle, lift any richer reading the round surfaced into round N+1's prompt rather than treating it as deviation. Pin: `feedback_design_round_richer_than_prompt_promote`.

## 6. Scope boundary — absolute, no staging

`serving/` does not import from any other subproject; the reverse is also forbidden. The rule is absolute: **no temporary cross-imports, no Phase-A staging step, no workspace-package-as-data-shim.** Cross-subproject contracts are JSON/parquet under `data/<topic>/<sub>.*` only.

The single allowed shared-code seam is `@qagents/diagram-kit`. Both producers (a subproject's `status_emit` script, etc.) and consumers (`designing/web`'s `/status` page) may depend on the kit. That is **not** a cross-subproject import — it's everyone-imports-from-shared-kit.

The CDK app is the only place that references AWS account IDs, ARN literals, or distribution IDs. Subprojects continue to read their bucket name + distribution ID from `serving/sites/<host>.env`, never inline (`INVENTORY.md` § 2 is the curated mirror).

## 7. Status emit (`data/status/serving.json`)

`scripts/status_emit.ts` writes `data/status/serving.json`: three graph-shaped architecture diagrams transcribed from `serving/diagrams/0[1-3]-*.prompt.md` (static-sites / app-api / identity), plus `TableEmit` + `DashboardEmit` panels and a live-state strip, interleaved via an explicit `panels[]` ordering. The exact panel set is pinned by `data/specs/serving-2026-05-26/tests/cases/80-status-emit-shape.sh` — extend the test with the emit.

Per-node `details` is an **HTML string** (rendered by the consumer via Astro's `set:html`, not `{expr}` which would escape entities). Keep detail prose factual — services + costs + scope phrasing matching `data/specs/serving-2026-05-26/SPEC.md`.

**Grid-diagram vs. `TableEmit` vs. `DashboardEmit` judgment.** Naturally tabular content (inventories, principal × policy matrices, trust maps) ships as a `TableEmit`, not an edgeless `gridLayout` diagram; tables wanting a header strip + state-aware filtering wrap into a `DashboardEmit` (KpiStrip + FilterChipGroup + the underlying `*-table` TableEmit). Keep the diagram only when cells need visual grouping, hover-pinning, or inspector details. Any future matrix-shaped (zero-edge) diagram must use the kit's `gridLayout`, not `dagreLayout` (`reference_dagre_grid_for_edgeless`); none is edgeless today.

The summary diagram surfaced on the index card is `static-sites`. Status-pill for serving: `OK` steady-state; `BUILDING` only while a `cdk deploy` is in flight.

## 8. AWS deploys (S3 + CloudFront sites)

Every Astro site under qagents (four today — see `./sites/*.env`; any future sibling) follows the same deploy contract. Per-site bucket + CloudFront distribution differ; the script shape, credential workflow, and verification cadence do not.

**Credential workflow — aws-vault + macOS Keychain (no plaintext keys on disk):**

- **Single unified IAM principal `qagents-deploy`** — one IAM user, two virtual MFA devices (primary + backup), one aws-vault profile, one Keychain entry. Locked at `data/specs/serving-2026-05-26/SPEC.md` § 2 decisions 7 + 8. Blast-radius isolation lives in policy-level MFA-Deny + 1h STS window, not principal multiplication.

  Each site's `<sub>/web/.env` pins `AWS_PROFILE=qagents-deploy` (per-site bucket + distribution IDs stay in `./sites/<host>.env` only — § 6); unified profile block at `./templates/aws-config.snippet`. Same principal pushes to CodeCommit for `qagents` + `dot.claude` (§ 9).

- `aws-vault add <profile>` — long-term IAM keys go to Keychain. `~/.aws/credentials` stays empty.
- `~/.aws/config` is metadata only (no credentials) — per-site `[profile …]` keys mirror `./templates/aws-config.snippet`. The `[default]` block carries **no credentials and no profile defaults for deploy work** — only `region` plus the `login_session` pointer that `aws login` (root console-session CLI for CloudShell-class root ops) maintains; deploy commands still require explicit `qagents-deploy` profile selection.
- IAM principal carries the scoped customer-managed policy at `./policies/qagents-deploy.json` (`arn:aws:iam::072264701492:policy/qagents-deploy`) — full Sid list, coverage, and rationale at `data/specs/serving-2026-05-26/SPEC.md` § 4.2. **Never** `AmazonS3FullAccess`. Inline-policy form retired — see `reference_iam_user_inline_policy_2kb_cap`.

  **Policy update workflow — self-serve from the laptop:** runbook at `./runbooks/policy-version-push.md` (covers the `create-policy-version --set-as-default` recipe, 5-version cap + `LimitExceeded` recovery, fresh-account bootstrap). Never `put-user-policy` against this user — that recreates the retired inline-policy shape.

**Deploy script shape — `./scripts/deploy-site.sh <host>`** (full contract at `data/specs/serving-2026-05-26/SPEC.md` § 5.3): sources the committed per-site `./sites/<host>.env` (`S3_BUCKET`, `CLOUDFRONT_DIST_ID`, `AWS_PROFILE`, `SITE_DIR`, optional `PROTECTED_PATHS` bash array), wipes the bucket (skip: `DEPLOY_NO_WIPE=1`; reversible via bucket versioning), runs the two-pass `aws s3 sync --delete` (HTML short-cache, everything else immutable), then invalidates `/*`. Each site's `package.json` `deploy` script invokes `pnpm build && bash ../../serving/scripts/deploy-site.sh <host>`.

**Gotcha:** the script adds `--profile` only when **not** running under aws-vault (marker: `AWS_VAULT` env var) — under aws-vault, ambient credentials are present and `--profile` would trigger an empty `~/.aws/credentials` lookup → `Unable to locate credentials`.

Standard invocation: `aws-vault exec qagents-deploy -- pnpm -C <sub>/web deploy`.

**Large binary media — five paths depending on shape** (video-CDN / small-media / clips-backup / archive-backup / CDN-mirror). Full path table + per-path operational detail (video-CDN push-ledger + release-gate chokepoint contracts + `UPLOAD_DRY_RUN`/test pin; `backup-clips.sh` variant-awareness + `cues` opt-in; the four `archive-artifact.sh` classes; `.close-protected-paths` mirror) → `data/specs/serving-2026-05-26/SPEC.md` § 5.4. The `PROTECTED_PATHS` hazard below applies to the small-media path.

**Hazard + structural fix — `PROTECTED_PATHS`.** Worktrees don't carry gitignored binaries, so a `pnpm deploy` from a fresh worktree runs the wipe + `s3 sync --delete` without them, 404ing the live asset. Fix: declare a per-site `PROTECTED_PATHS=("videos/*.mp4" ...)` bash array in `./sites/<host>.env`; `deploy-site.sh` threads `--exclude <glob>` through the wipe AND both sync passes (set on `quantapix.com.env`; femfas.net needs none — its `public/*.pdf` filings are committed). Binary updates still go via `aws s3 cp` + targeted invalidation — the protection only stops accidental deletion.

**Sibling hazard — archive `dir` bundles from canonical only.** Worktrees carry gitignored ground truth as *symlinks* (`.worktree-links`) and `find` won't descend them, so `archive-artifact.sh <class> … push` from a worktree tars the link entry alone (empty archive) and `verify` false-matches it against an equally empty rebuild. `bundle_dir()` now hard-fails on a symlinked source and prints the canonical re-invocation; `file` bundles are immune (`cp` follows links). Push `parquet` from canonical. Memory `project_parquet_gitignored_ground_truth`; spec `data/specs/serving-2026-05-26/artifact-archive-s3-2026-05-29/SPEC.md` § 3.5.

**CLEAR-4 push-ledger completeness gate — `verify-push-ledger.sh`.** The operator ruling (signoff-framework SPEC § 11 q.2, 2026-07-20) homes the independent S3 inventory diff in the serving pre-deploy path, authenticated through this script's aws-vault profile lane (managing is observe-only on AWS, so it does NOT run it). `deploy-site.sh` runs the gate before the wipe for any site whose `<host>.env` sets `SIGNOFF_LEDGER_GATE=1` (only `quantapix.com.env` today — it owns the video CDN + `video-thumbs/` surfaces). The gate lists live objects in `s3://qagents-videos/*` (`cdn`) + `s3://quantapix.com/video-thumbs/*` (`site-thumb`) and diffs vs `data/publishing/push-ledger.jsonl` (canonical ∪ the `QAGENTS_PENDING_ROOT` overlay, so an un-promoted same-day line still counts — R5); a live object with no ledger line is a breach. **STRICT since 2026-07-22** (`SIGNOFF_GATE_STRICT=1` in `quantapix.com.env`): a live `cdn` object with no ledger line aborts the deploy pre-wipe (exit 3). The legacy backfill that gated the flip is done (ledger 2→9 lines). `site-thumb` stays report-only until its `surface:"site-thumb"` writer lands (R16) — add it to `LEDGER_GATE_STRICT_SURFACES` then, but ledger its 8 live thumbs FIRST or every deploy blocks. `push-ledger.jsonl` is a GENERATED projection of `ledger.push_event` (`qagents.ledger render-push-ledger`) — never hand-append. Pinned by `data/specs/serving-2026-05-26/tests/cases/21-push-ledger-gate.sh` (pure-bash fixture mode, no AWS).

**Testing the deploy script — `DEPLOY_DRY_RUN=1`.** Echoes each `aws ...` command as `+ aws ...` instead of executing, and skips the `pnpm build` pre-step. Pinned by `data/specs/serving-2026-05-26/tests/cases/20-deploy-site-protected.sh` (pure bash, no AWS) — guards `PROTECTED_PATHS` propagation through every mutation + the `DEPLOY_NO_WIPE=1` suppression. Run the whole suite with `bash data/specs/serving-2026-05-26/tests/run.sh`. Companion live-URL e2e in `designing/web/tests/e2e/site.spec.ts` (`large media URLs` describe block) HEADs the protected URL post-deploy and asserts 200 + `video/*` content-type + >1MB.

**Bucket hardening — once per bucket:** `aws-vault exec qagents-deploy -- bash <sub>/web/scripts/setup-bucket-hardening.sh` enables versioning + 30-day noncurrent-version expiration + 7-day multipart-abort. Reference JSON at `./templates/s3-lifecycle-noncurrent-30d.json`.

**New-CloudFront-distribution checklist** → `./runbooks/new-cloudfront-distribution.md`. Pins `reference_cloudfront_function_redirect_pattern`, `reference_cloudfront_404_needs_dest_page`.

**Internal links to anchored sections must include the trailing slash before the hash**: `/dockets/#tier-X`, never `/dockets#tier-X`. Astro static builds emit `/<route>/index.html`; S3 returns `302 → /<route>/` for the slashless form, costing a redirect round-trip and breaking Playwright glob matchers.

**Live-site smoke test after every deploy.** A clean `pnpm deploy` exit only proves S3 was written + invalidation accepted — not that the site is live. The Playwright suite at `<sub>/web/tests/e2e/` doubles as a deploy verifier; `playwright.config.ts` reads `PW_BASE_URL` and, when set, switches `baseURL` to the remote URL and omits the local `webServer` block entirely:

```
aws-vault exec qagents-deploy -- pnpm -C <sub>/web deploy
PW_BASE_URL=https://<site> pnpm -C <sub>/web test:e2e
```

Mandatory after first-time deploy to a new distribution and any origin/policy touch.

**CI lane — `.github/workflows/deploy-site.yml`.** Same `deploy-site.sh` runs from GitHub Actions under OIDC role `qagents-deploy-ci` (no long-lived secrets). Two triggers: `workflow_dispatch` with a `choice` input over the four sites (manual lane), and `push` to `main` filtered to `{documenting,designing,verifying,evaluating}/web/**` — a `resolve-matrix` job runs `git diff --name-only` on the push range and emits exactly the sites whose `<dir>/web/**` files changed. Per-matrix-entry concurrency keys on `deploy-${{ matrix.site }}` with `cancel-in-progress: false` (parallel across sites, queued within a site — half-applied wipe+sync is worse than waiting). The CI lane never reimplements deploy mechanics; it shells into `serving/scripts/deploy-site.sh`. Static wiring pinned by `data/specs/serving-2026-05-26/tests/cases/30-deploy-workflow.sh` (pure-bash grep checks, no Actions runner needed).

## 8.5. App server deploys (EC2 + Caddy + FastAPI)

Different surface from § 8 static-site deploys. EC2 instance `qagents-app-1` hosts both `verifying/` (qnarre, :8787) and `evaluating/` (qresev, :8788) FastAPI servers behind Caddy on `api.{qnarre,qresev}.quantapix.com`. Bootstrap installs elan + pre-installs the kernels' pinned Lean toolchain (`LEAN_TOOLCHAIN` in `scripts/bootstrap-ec2.sh`, lockstep with `{proving,accounting}/lean-toolchain`) under `/srv/qagents/.elan` as the `qagents` user; t4g.small sizing assumes mathlib-free kernels. Full topology: `serving/INVENTORY.md` § 2.5; spec § 6. AMI-drift / deliberate-replacement cycle: `data/specs/serving-2026-05-26/SPEC.md` § 8.2. Live-state items (instance ids, health reconciliation) tracked in `data/next-steps/serving.md`.

**Deploy contract (spec § 2 dec. 2 — no repo credentials on EC2):**

```bash
aws-vault exec qagents-deploy -- bash serving/scripts/deploy-app.sh {qnarre|qresev|both}
```

- rsync server/ → tarball → `s3://qagents-artifacts/releases/<app>/<sha>.tar.gz` + `latest.tar.gz` pointer
- `aws ssm send-command` runs fetch + atomic-swap + `pip install -r requirements.txt` (only when the tarball ships one — qresev does for pyarrow, qnarre ships none; the EC2 step echoes a loud skip when absent) + `systemctl reload <app>.service`
- Rollback = one-line `aws s3 cp` of the prior tarball over `latest.tar.gz` + re-run deploy-app.sh

**Provisioning the qresev deps + data.** Bootstrap installs only fastapi+uvicorn into `/srv/qagents/.venv`; `deploy-app.sh qresev` stages `evaluating/requirements.txt` (pyarrow) for the SSM pip step, and the OHLCV parquet tree at `/srv/qagents/financial/parquet/ohlcv-equities/` ships via `aws-vault exec qagents-deploy -- bash serving/scripts/ship-parquet.sh` (operator-fired; `SHIP_DRY_RUN=1` no-AWS path; pinned by `tests/cases/45-ship-parquet.sh`; detail in spec § 6). Instance replacement = `bootstrap → deploy-app.sh qresev → ship-parquet.sh`, not archaeology.

**Hazard — kernel rotation wipes post-bootstrap state.** `deploy-app.sh` rotates `/srv/qagents/<kernel>/` into `<kernel>.previous/` and unpacks the new tarball, dropping `.lake/build/lib/` (incremental cache) unless migrated — so it migrates `.lake/` from `<kernel>.previous/` + runs `install -d` post-rotation. Failure signature if either step is missing: systemd preflight `status=226/NAMESPACE` (the `ReadWritePaths=` mount fails). Pinned: `feedback_kernel_rotation_cache_hazard`.

**Shell access** is SSM Session Manager only (no SSH on the box):

```bash
aws-vault exec qagents-deploy -- bash serving/scripts/ssm-shell.sh
```

Filters on tag `Name=qagents-app-1`. Requires `session-manager-plugin` installed locally (`brew install --cask session-manager-plugin`).

**Shared ledger store — LAN primary on qred** (`ledger-lan-primary-2026-07-19` subspec of `data/specs/shared-ledger-store-2026-07-09/`): the store runs on qred `18-main` @ **5432** over direct LAN links (verify-ca TLS + scram `qagents` role; DSN in `~/.config/qagents/ledger.dsn`, chmod 600) — no tunnel on the LAN path. Cutover tooling `serving/scripts/pg-lan/` + `migrate-ledger-to-lan.sh`; runbook `serving/runbooks/ledger-lan-cutover.md`; backups two-tier (qred nightly dump → qblk 14d/8w + weekly restore-verify; ONE daily S3 ship via the put-only `qagents-pg-backup` seat to `s3://qagents-artifacts/backups/`). The legacy RDS path stays until L3 (freeze → snapshot → destroy after a 30-day read; `serving/scripts/ledger-tunnel.sh` port-forwards to it). **L3 is blocked on an IAM delta, not on MFA** — `qagents-deploy` holds no direct `rds:*` (probed 2026-07-22; CDK reaches RDS via the bootstrap role it assumes). **The SSM tunnel machinery survives L3** — retirement removes the RDS endpoint, not the tunnel lane. DROP-schema test rule unchanged (DB-gated suites use a disposable DB on qred, never prod). The `--tunnel-status` ritual applies only while RDS is the DSN target; post-L1 the LAN DSN makes store writes tunnel-independent. **DSN handling:** one at-rest copy, `~/.config/qagents/ledger.dsn` mode 600 — injected per invocation (`~/.local/bin/memsearch` wrapper), NEVER exported from a shell profile (`.zshenv` is sourced by every zsh, which leaks the password to every process).

**Smoke** (live HTTPS via Let's Encrypt cert):

```bash
curl -fsS https://api.qnarre.quantapix.com/api/health
curl -fsS https://api.qresev.quantapix.com/api/health
```

**Operator-policy gaps** — surviving items tracked in `INVENTORY.md` § 8 + `data/next-steps/serving.md` § A; bundled into the next policy-version push per `feedback_operator_policy_gap_per_phase`.

## 8.6. Cron-EC2 lane

Serving/ owns the AWS-touching artifacts of `data/specs/cron-ec2-migration-2026-05-19/SPEC.md` — CDK deltas, EC2-side scripts + systemd units under `scripts/ec2-cron/`, ship script `scripts/deploy-ec2-cron.sh`, manifest verifier, structural test at `data/specs/serving-2026-05-26/tests/cases/40-ec2-cron.sh`. Operational deploy contract + first-fire smoke: `data/specs/serving-2026-05-26/SPEC.md` § 6.6 + § 8.3. Managing/ + trading/ + `code/agent_sdk/` own the out-of-serving-scope files (per-file owner tags in the spec's Appendix A.1/A.2). Reuses § 8.5's EC2 infra (`qagents-app-1` + `qagents-app-role` + `qagents-artifacts` + `alias/qagents-cmk`) — additive only.

**Operator deploy path** (mirrors § 8.5, single command):

```bash
aws-vault exec qagents-deploy -- bash serving/scripts/deploy-ec2-cron.sh
```

Same SSM mechanics as `deploy-app.sh`; no SSH. Per-routine timers enabled lane-by-lane by the owning session per spec § 8; the four shared timers (`qagents-mirror-pull`, both `qagents-tarball-build-*`, `qagents-routine@`) come up at Phase-7 first-deploy.

**Two-clock TZ model.** TZ is pinned in two load-bearing layers, BOTH required: (1) timers FIRE at ET via `OnCalendar=… America/New_York` on every `.timer`; (2) the routine *process* is pinned via `Environment=TZ=America/New_York` on all three cron `.service` units (`qagents-routine@`, both `qagents-tarball-build-*`) — else a 22:00 ET fire computes a next-day date. The box TZ stays UTC (AL2023 default; do NOT change it — FastAPI + Caddy + cw-agent share the box); provenance instants stay UTC (`date -u` ignores `$TZ`); `build-tarball.sh` mirrors the inline TZ for hand-run correctness. Full rationale: spec § 3.4.

**Hazard — t4g.small dual-tenancy.** The cron lane shares CPU/RAM with the two FastAPI surfaces from § 8.5. Guardrail: `MemoryMax=1500M` per routine unit (cron-ec2-migration spec § 3.4), FastAPI keeps 500 MB min. OOMs in `journalctl` → escalate to dedicated `qagents-cron-1` (spec § 7.2, ~$13/mo delta), not a re-architecture.

## 9. Pushing from the canonical-role holder (qpur by default) — four remotes per repo

Two qagents-class repos (`qagents`, `dot.claude` = `~/.claude/`) push to **four** remotes. Public-org GitHub content pushes via `publishing/scripts/github_meta.py sync` (owned by `publishing/CLAUDE.md` § 4–5; [[reference_quantapix_org_repos]]; source of truth `publishing/quantapix/`); `git push-quantapix` remains for manual/non-publish pushes only — symlink-clobber hazard below.

```
github  → git@github-qpur:quantapix/<repo>.git           # via ed25519 SSH key
aws     → codecommit::us-east-1://<repo>                 # via aws-vault qagents-deploy
qblk    → qblk:~/repos/<repo>.git                        # via legacy quantapix RSA key
qred    → qred:~/repos/<repo>.git                        # same key; second LAN bare mirror
```

The qblk + qred bare mirrors double as the LAN git-exchange fabric for the network nodes (§ 10). `remote.pushDefault = github`, `push.default = current`. `git push-all` sweeps all four in one command — skips unconfigured remotes silently, wraps the `aws` push in `aws-vault exec qagents-deploy --` automatically. Both git-subcommand wrappers live at `serving/scripts/git-push-{all,quantapix}`, each symlinked onto PATH at `~/.local/bin/`. The repo-wide sweeper `scripts/push-all.sh` (root) loops `git push-all` across every qagents-class checkout. Since 2026-07-18 (`push-pull-redesign-2026-07-18` § 9): `git push-all` runs a **hub FF-guard** before pushing `main` — refuses (exit 30) a `main` not fast-forwardable from a qblk/qred mirror (fail-closed) — and `scripts/push-all.sh` folds `--tidy` (reaps merged `<node>/<topic>` mirror refs) after the sweep.

**Key facts that bite if you forget them:**

- **CodeCommit URL form must NOT include the profile when running under aws-vault.** Use `codecommit::us-east-1://<repo>`, not `codecommit::us-east-1://qagents-deploy@<repo>`. The `@profile@` form makes git-remote-codecommit do a profile-credential lookup in `~/.aws/config` (which has no static keys — they're in Keychain), bypassing aws-vault's injected env vars.
- **Don't ever delete the only MFA device on `qagents-deploy` without registering its replacement first.** Merged policy carries a `DenyEverythingWithoutMFA` statement; with the only device gone, every `aws-vault exec` call fails until a new device is enrolled.
- **`~/.ssh/config` is locked-down per host.** No `Host *` IdentityFile, no `ForwardAgent yes`, `IdentitiesOnly yes` everywhere. The new ed25519 key (`~/.ssh/id_ed25519_github_qpur`) is GitHub-only via the `github-qpur` alias; the legacy `quantapix` RSA stays on qblk-class hosts only.
- **`git filter-repo` strips the `origin` remote** as a safety measure. After history rewrite, re-add remotes manually and force-push (rewritten history has different commit hashes).
- **The `git push-quantapix` bridge ships symlinks AS symlinks** (`rsync -a` copies the link, not the referent) — a push from a worktree would replace a `.worktree-links`-backed binary on GitHub with a link file. Push such slots from **canonical only**. (`/publish` is immune — `github_meta.py sync` uses `rsync -aL`.)

## 10. Local network — qblk / qred / qyel nodes + `ssh aws-1`

Owner: `data/specs/serving-2026-05-26/local-network-2026-07-12/SPEC.md` (node roster + IPs, SSH identity model, git topology, tmux contract, Postgres, backup lanes, access-ergonomics + root-account runbooks). This section is entry points + hazards only.

- **Remote sessions:** `bash serving/scripts/net-shell.sh {qblk|qred|qyel|aws-1}` attaches-or-creates the `qagents` tmux session (plain-shell fallback where tmux is absent).
- **`ssh aws-1`** — SSH to `qagents-app-1` over an SSM tunnel (no public port 22; MFA stays the boundary). `Host aws-1` → `serving/scripts/ssm-ssh-proxy.sh` (resolves by Name tag, survives § 8.2 replacement); one-time key install: `serving/runbooks/ec2-ssh-over-ssm.md`; `ssm-shell.sh` remains the zero-setup fallback. Login user `ec2-user`; `sudo -u qagents` for `/srv/qagents`.
- **Git rule:** nodes work on `<node>/<topic>` branches pushed back to the qblk/qred bare mirrors; the canonical-role holder merges in a normal `/open` session and `git push-all` propagates. **Non-role-holding** nodes never write `main`. *Canonical is a ROLE, not a hostname* (spec § 4.1, ratified 2026-07-22): qpur holds it by default, qyel is the other role-capable host (it genuinely writes + pushes `main` while holding the cron `SEAT`), qblk/qred/aws-1 never can. CR-3: a role-capable host's checkout MUST be at `<root>` — that identity is what every hardcoded canonical path in `scripts/` relies on.
- **Node bring-up / "works over ssh, fails under launchd":** `runbooks/node-bring-up.md` — an ssh shell has no Keychain, no agent, and homebrew on `PATH`; launchd has none of the three. Probe by absolute path, test agents via `launchctl kickstart`, and sync a node by **pushing from the role holder** (`git push qyel:<root> main`; `receive.denyCurrentBranch=updateInstead` is set there) — never `git pull` on the node.
- **Node roster projection:** `serving/local-network/nodes.txt` — machine-readable mirror of the spec § 2 roster (consumers: `scripts/pull.sh` ref-scoping, managing AUDIT-C4). Edit in lockstep with the spec when adding/removing a node.
- **LAN backups:** `bash serving/scripts/backup-to-node.sh {qblk|qred} [videos|waves|trading|memsearch]` — contract owner: `data/specs/workstation-parity-2026-07-21/SPEC.md` § 5. Destinations are per-SOURCE-HOST prefixed (`<node>:~/backups/qagents/<host>/<class>/` — two workstations never share a delete scope); `--delete-after` survives only on `trading` (host-owned scope); per-destination preflight refuses empty sources + destination-superset divergence; `-i` itemizes deletions. Sources hardcoded to canonical (worktree-symlink hazard class); `BACKUP_DRY_RUN=1` for the no-write lane; `BACKUP_SSH` overrides the transport. Restore: `restore-from-node.sh {qblk|qred} {waves|videos|memsearch} [--apply]` (LAN union across host prefixes; tape moves via `scripts/sync-ground-truth.sh` only). Cron: `serving:node-backup` (01:30 ET, live + first fires clean) + this host's parity-fingerprint publish; the S3 leg is qred's nightly job (host-prefixed keys, missing class = hard fail). S3 stays the durability story.
- **Postgres:** **qred `18-main` @ 5432 is the shared-ledger-store LAN primary** (spec § 6, first adoption consumed by `ledger-lan-primary-2026-07-19`); qblk `18-main` @ 5432 is backup/restore-verify. RDS frozen→retired at that subspec's L3. Provisioning: `scripts/provision-pg-lan-push.sh {qred|qblk}`; cutover runbook `runbooks/ledger-lan-cutover.md`.
- **Mirror-guard:** `bash serving/scripts/harden-mirrors.sh [--verify]` — per-ref `update` hook on both nodes' `qagents.git` + `dot.claude.git` protecting `refs/heads/main` (non-FF + delete refused; `<node>/*` stays deletable for `/pull --tidy`). Installed + live-verified 2026-07-20 (ns-27).
