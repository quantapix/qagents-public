# CLAUDE.md — serving/

Project-specific rules for the qagents AWS cloud-base. Assumes Claude Code's default guidance and the repo-root `qagents/CLAUDE.md`.

## 1. Single source of truth for AWS

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

The kit's display-mode contract — the closed set of `*Emit` schemas it ships vs. what stays consumer-owned (Chart, Graph, 3D-mix, Video, App-shell) — is fixed by `data/specs/display-modes-2026-05-07/SPEC.md`. Adding a new emit kind requires a kit minor version bump + spec amendment + e2e coverage; v0.4.0 closed the set.

The kit's source-of-truth design bundle lives at `data/renders/serving-design/` (read-only, regen-wholesale; moves to `rendering/designs/serving-diagrams/` at the serving P4 slot). Sync procedure: `serving/diagrams/kit/README.md` § "Sync with the design bundle".

**Consumers must rebuild the kit before their own typecheck/build/dev.** The kit emits to `dist/` (gitignored), and `pnpm install` does not auto-run workspace-package builds. Pointing the kit's `main`/`types` at `src/` directly was tested and rejected (DOM-type isolation; detail in `reference_kit_build_consumer_pre_x`). Adopted pattern is `pre-X` hooks in every consumer's `package.json` running `pnpm -F @qagents/diagram-kit build` before the consumer's own step. Wired today on `serving/package.json` (`pretypecheck`) and `designing/web/package.json` (`predev`, `prebuild`, `precheck`); future consumers need the same.

## 5. Diagram prompts are voice-controlled

`serving/diagrams/0X-*.prompt.md` are Claude Design prompts. They enforce Quantapix branding (BracketedQ glyph, approved brand names only), engineer-debugging-a-system voice on labels (no marketing fluff), and the shape-agnostic Node primitive (no AWS-service glyphs).

When iterating a Design return on a diagram bundle, lift any richer reading the round surfaced into round N+1's prompt rather than treating it as deviation. Pin: `feedback_design_round_richer_than_prompt_promote`.

## 6. Scope boundary — absolute, no staging

`serving/` does not import from any other subproject; the reverse is also forbidden. The rule is absolute: **no temporary cross-imports, no Phase-A staging step, no workspace-package-as-data-shim.** Cross-subproject contracts are JSON/parquet under `data/<topic>/<sub>.*` only.

The single allowed shared-code seam is `@qagents/diagram-kit`. Both producers (a subproject's `status_emit` script, etc.) and consumers (`designing/web`'s `/status` page) may depend on the kit. That is **not** a cross-subproject import — it's everyone-imports-from-shared-kit.

The CDK app is the only place that references AWS account IDs, ARN literals, or distribution IDs. Subprojects continue to read their bucket name + distribution ID from `serving/sites/<host>.env`, never inline.

## 7. Status emit (`data/status/serving.json`)

`scripts/status_emit.ts` writes `data/status/serving.json` with three graph-shaped architecture diagrams transcribed from `serving/diagrams/0[1-3]-*.prompt.md` (static-sites / app-api / identity), three `TableEmit` panels (static-sites-inventory, iam-principals, oidc-trust), and two `DashboardEmit` panels (service-inventory, security-baseline — each wrapping a KpiStrip + FilterChipGroup + underlying `*-table` TableEmit), plus a live-state strip; all interleaved via an explicit `panels[]` ordering.

Per-node `details` is an **HTML string** (rendered by the consumer via Astro's `set:html`, not `{expr}` which would escape entities). Keep detail prose factual — services + costs + scope phrasing matching `data/specs/serving-2026-05-26/SPEC.md`.

**Grid-diagram vs. `TableEmit` vs. `DashboardEmit` judgment.** Naturally tabular content (inventories, principal × policy matrices, trust maps) ships as a `TableEmit`, not an edgeless `gridLayout` diagram; tables wanting a header strip + state-aware filtering wrap into a `DashboardEmit` (KpiStrip + FilterChipGroup + the underlying `*-table` TableEmit). Keep the diagram only when cells need visual grouping, hover-pinning, or inspector details.

Any future matrix-shaped (zero-edge) serving diagram must use the kit's `gridLayout`, not `dagreLayout` — see `reference_dagre_grid_for_edgeless`. None is edgeless today (`service-inventory` + `security-baseline` ship as `TableEmit`/`DashboardEmit`).

The summary diagram surfaced on the index card is `static-sites`. Status-pill for serving: `OK` steady-state; `BUILDING` only while a `cdk deploy` is in flight.

## 8. AWS deploys (S3 + CloudFront sites)

Every Astro site under qagents (`documenting/web/` for femfas.net, `designing/web/` for quantapix.com, any future sibling) follows the same deploy contract. Per-site bucket name + CloudFront distribution differ; the script shape, credential workflow, and verification cadence do not.

**Credential workflow — aws-vault + macOS Keychain (no plaintext keys on disk):**

- `brew install awscli aws-vault` once per workstation.
- **Single unified IAM principal `qagents-deploy`** — one IAM user, two virtual MFA devices (`Imres-iPhone` primary + `Xmaos-iPhone` backup), one aws-vault profile, one Keychain entry. Locked at `data/specs/serving-2026-05-26/SPEC.md` § 2 decisions 7 + 8. Blast-radius isolation lives in policy-level MFA-Deny + 1h STS window, not principal multiplication.

  | Site | aws-vault profile | MFA device | Bucket | Distribution |
  |---|---|---|---|---|
  | femfas.net (`documenting/web/`) | `qagents-deploy` | `Imres-iPhone` | `femfas.net` | `E1HSASY4B6ODER` |
  | quantapix.com (`designing/web/`) | `qagents-deploy` | `Imres-iPhone` | `quantapix.com` | `E27NQG9Y1ZPLGH` |

  Each site's `<sub>/web/.env` pins `AWS_PROFILE=qagents-deploy`; unified profile block at `./templates/aws-config.snippet`. Same principal pushes to CodeCommit for `qagents` + `dot.claude` (§ 9).

- `aws-vault add <profile>` — long-term IAM keys go to Keychain. `~/.aws/credentials` stays empty.
- `~/.aws/config` is metadata only: per-site `[profile …]` with `region`, `output`, `mfa_serial`, `duration_seconds=3600`, `cli_pager=`, `cli_history=disabled`, an `s3 =` transfer-tuning block. **No `[default]` block** — forces explicit profile selection.
- IAM principal carries the scoped customer-managed policy at `./policies/qagents-deploy.json` (`arn:aws:iam::072264701492:policy/qagents-deploy`) — full Sid list, coverage, and rationale at `data/specs/serving-2026-05-26/SPEC.md` § 4.2. **Never** `AmazonS3FullAccess`. Inline-policy form retired — see `reference_iam_user_inline_policy_2kb_cap`.

  **Policy update workflow — self-serve from the laptop** (since v6 / 2026-05-16): runbook at `./runbooks/policy-version-push.md` (covers the `create-policy-version --set-as-default` recipe, 5-version cap + `LimitExceeded` recovery, fresh-account bootstrap). Never `put-user-policy` against this user — that recreates the retired inline-policy shape.

**Deploy script shape — `./scripts/deploy-site.sh <host>`** (full contract at `data/specs/serving-2026-05-26/SPEC.md` § 5.3):

The central deploy script is parameterized by per-site config files at `./sites/<host>.env` (committed; `S3_BUCKET`, `CLOUDFRONT_DIST_ID`, `AWS_PROFILE`, `SITE_DIR`, optional `PROTECTED_PATHS` bash array). Each site's `package.json` `deploy` script invokes `pnpm build && bash ../../serving/scripts/deploy-site.sh <host>`.

1. Source `./sites/<host>.env`.
2. Build the optional `--profile` flag — but only when **not** running under aws-vault. Marker: `AWS_VAULT` env var. Under aws-vault, ambient credentials are present and `--profile` would override them with empty `~/.aws/credentials` lookup → `Unable to locate credentials`.
3. **Wipe (default)** — `aws s3 rm s3://$BUCKET --recursive`. Skip with `DEPLOY_NO_WIPE=1`. Combined with bucket versioning, the wipe is reversible.
4. Two-pass `aws s3 sync --delete`: HTML short-cache (max-age=300, must-revalidate); everything else immutable (max-age=31536000).
5. CloudFront `/*` invalidation.

Standard invocation: `aws-vault exec qagents-deploy -- pnpm -C <sub>/web deploy`.

**Large binary media — five paths depending on shape:**

- **Published video deliverables** (MP4 from HeyGen/Remotion, `explaining/`-catalog-class) → `qagents-videos` via `./scripts/upload-video.sh <local> <topic>/<file>.<ext>` → `https://videos.quantapix.com/<topic>/<file>.<ext>`. Public CDN; decoupled from site deploy; immutable-keyed (no CF invalidation). **This bucket is world-readable the instant a key lands — every upload IS a public push, not a private build step (the 4.1 gate-jump).** Two contracts ride the chokepoint (signoff-framework § 8 / signoff-verification § 4.2): (1) **push-ledger emit** — every upload appends a `{key, content_sha256, surface:"cdn", commit}` line to the gitignored pending buffer (`${QAGENTS_PENDING_ROOT:-$REPO/pending}/data/publishing/push-ledger.jsonl`) + stdout audit, **never** canonical `data/publishing/` (cross-subproject, no `.data-write-lock`); the managing verifier is the canonical writer-of-record (append-MERGE, dedupe `commit`+`content_sha256`). `commit` = `git rev-parse HEAD` at the PUT instant; `content_sha256` is the sha of the PUT bytes. (2) **release gate** — a `T<n>/` catalog key REFUSES (exit 3) unless `CLEARANCE_COMMIT` (the FINANCIALLY-CLEARED record's `granting_commit`, publishing/CLAUDE.md § 10) is already an ancestor of HEAD — forcing `git merge main` first. The script can't judge prose attestations; this is the mechanical ancestry precondition, not a safety guarantee. One-off keys (no `T<n>/` prefix) are ungated but still ledgered for the inventory-diff completeness check. `UPLOAD_DRY_RUN=1` echoes the `aws`/append steps; pinned by `tests/cases/85-upload-video-ledger.sh`.
- **One-off small media** (logos, icons, <5 MB clips) ride on `pnpm deploy`: drop at `<sub>/web/public/<topic>/<file>.<ext>` (gitignore the file); existing `max-age=31536000, immutable` header applies. `PROTECTED_PATHS` hazard below applies to this path only.
- **Interim/scratch binaries (gitignored, temporary)** — HeyGen takes, Remotion ProRes, Resolve cut renders — mirror to `qagents-clips-backup` via `./scripts/backup-clips.sh <sub> <slug> [short|long]... [<class>...]`. Variant-aware: walks `<slug>/{long,short}/` dirs under per-variant S3 prefix `<sub>/<slug>/<variant>/<class>` (legacy flat `<slug>/<class>` still supported); the optional `short`/`long` arg filters. **Default classes = `takes auditions cuts captions`; `cues` are opt-in** (2026-06-30) — Remotion ProRes cues are deterministic + regenerable via `rendering/scripts/render.sh explaining-cards`, so they fail the bucket's expensive-to-regenerate criterion (pass `cues` explicitly to back them up). Private; Standard → IA(30d) → Glacier IR(90d) → expire(365d). Operator-fired only. Spec: `data/specs/serving-2026-05-26/clips-backup-s3-2026-05-24/SPEC.md`.
- **Durable version-pinned artifacts (gitignored, kept forever)** — regenerable-today-but-not-durably ground truth keyed by a version-pin → `qagents-archive-backup` via `./scripts/archive-artifact.sh <class> <version-pin> {push|verify|restore <dest>}`. Four registered classes (`uscode` / `parquet` / `usc-waves` / `trading-waves`) — registry in the script, class table + lifecycle in the spec. Private, **versioned**, content-addressed (sha256 metadata + per-pin MANIFEST.json), one immutable `<class>/<version-pin>/` prefix per pin. Durable inverse of the clips lane; operator-fired only. Spec: `data/specs/serving-2026-05-26/artifact-archive-s3-2026-05-29/SPEC.md`.
- **Local-backup mirror of CDN-hosted videos (opt-in per site):** sibling MAY retain gitignored mirror at `<sub>/web/public/videos/*.mp4`; protected from worktree-teardown via `<sub>/.close-protected-paths` (`feedback_close_protected_paths_pattern`); deploy-side `PROTECTED_PATHS` is separate. Embeds reference the absolute CDN URL.

**Hazard + structural fix — `PROTECTED_PATHS`.** Worktrees don't carry gitignored binaries, so a `pnpm deploy` from a fresh worktree runs the wipe + `s3 sync --delete` without them, 404ing the live asset. Fix: declare a per-site `PROTECTED_PATHS=("videos/*.mp4" ...)` bash array in `./sites/<host>.env`; `deploy-site.sh` threads `--exclude <glob>` through the wipe AND both sync passes. Currently set on `quantapix.com.env`; femfas.net needs none (its `public/*.pdf` filings are committed per `documenting/CLAUDE.md`). Binary updates still go via `aws s3 cp` + targeted invalidation — the protection only stops accidental deletion.

**Testing the deploy script — `DEPLOY_DRY_RUN=1`.** Echoes each `aws ...` command as `+ aws ...` instead of executing, and skips the `pnpm build` pre-step. Pinned by `data/specs/serving-2026-05-26/tests/cases/20-deploy-site-protected.sh` (pure bash, no AWS) — guards `PROTECTED_PATHS` propagation through every mutation + the `DEPLOY_NO_WIPE=1` suppression. Run the whole suite with `bash data/specs/serving-2026-05-26/tests/run.sh`. Companion live-URL e2e in `designing/web/tests/e2e/site.spec.ts` (`large media URLs` describe block) HEADs the protected URL post-deploy and asserts 200 + `video/*` content-type + >1MB.

**Bucket hardening — once per bucket:** `aws-vault exec qagents-deploy -- bash <sub>/web/scripts/setup-bucket-hardening.sh` enables versioning + 30-day noncurrent-version expiration + 7-day multipart-abort. Reference JSON at `./templates/s3-lifecycle-noncurrent-30d.json`.

**New-CloudFront-distribution checklist (one-time, per distribution).** S3 REST + OAC doesn't serve Astro out of the box — three knobs in order: (1) OAC bucket policy on the S3 bucket (else 403); (2) URI-rewrite Function from `./templates/cloudfront-rewrite-index.js`, **Save → Publish → attach to Viewer request** (Publish is easy to miss); (3) `403→/404.html` AND `404→/404.html` error responses (else missing routes return raw S3 AccessDenied XML). Every new shell must ship `src/pages/404.astro` so `dist/404.html` exists. Memories: `reference_cloudfront_function_redirect_pattern`, `reference_cloudfront_404_needs_dest_page`. After all three: `aws-vault exec qagents-deploy -- aws cloudfront create-invalidation --distribution-id <ID> --paths "/*"` → run live e2e.

**Internal links to anchored sections must include the trailing slash before the hash**: `/dockets/#tier-X`, never `/dockets#tier-X`. Astro static builds emit `/<route>/index.html`; S3 returns `302 → /<route>/` for the slashless form, costing a redirect round-trip and breaking Playwright glob matchers.

**Live-site smoke test after every deploy.** A clean `pnpm deploy` exit only proves S3 was written + invalidation accepted — not that the site is live. The Playwright suite at `<sub>/web/tests/e2e/` doubles as a deploy verifier; `playwright.config.ts` reads `PW_BASE_URL` and, when set, switches `baseURL` to the remote URL and omits the local `webServer` block entirely:

```
aws-vault exec qagents-deploy -- pnpm -C <sub>/web deploy
PW_BASE_URL=https://<site> pnpm -C <sub>/web test:e2e
```

Mandatory after first-time deploy to a new distribution and any origin/policy touch.

**CI lane — `.github/workflows/deploy-site.yml`.** Same `deploy-site.sh` runs from GitHub Actions under OIDC role `qagents-deploy-ci` (no long-lived secrets). Two triggers: `workflow_dispatch` with a `choice` input over the four sites (manual lane), and `push` to `main` filtered to `{documenting,designing,verifying,evaluating}/web/**` — a `resolve-matrix` job runs `git diff --name-only` on the push range and emits exactly the sites whose `<dir>/web/**` files changed. Per-matrix-entry concurrency keys on `deploy-${{ matrix.site }}` with `cancel-in-progress: false` (parallel across sites, queued within a site — half-applied wipe+sync is worse than waiting). The CI lane never reimplements deploy mechanics; it shells into `serving/scripts/deploy-site.sh`. Static wiring pinned by `data/specs/serving-2026-05-26/tests/cases/30-deploy-workflow.sh` (pure-bash grep checks, no Actions runner needed).

## 8.5. App server deploys (EC2 + Caddy + FastAPI)

Different surface from § 8 static-site deploys. EC2 instance `qagents-app-1` hosts both `verifying/` (qnarre, :8787) and `evaluating/` (qresev, :8788) FastAPI servers behind Caddy on `api.{qnarre,qresev}.quantapix.com`. Bootstrap installs elan + pre-installs `leanprover/lean4:v4.31.0` under `/srv/qagents/.elan` as the `qagents` user; t4g.small sizing assumes mathlib-free kernels. Full topology: `serving/INVENTORY.md` § 2.5; spec § 6. AMI-drift / deliberate-replacement cycle: `data/specs/serving-2026-05-26/SPEC.md` § 8.2. Live-state items (instance ids, health reconciliation) tracked in `data/next-steps/serving.md`.

**Deploy contract (spec § 2 dec. 2 — no repo credentials on EC2):**

```bash
aws-vault exec qagents-deploy -- bash serving/scripts/deploy-app.sh {qnarre|qresev|both}
```

- rsync server/ → tarball → `s3://qagents-artifacts/releases/<app>/<sha>.tar.gz` + `latest.tar.gz` pointer
- `aws ssm send-command` runs fetch + atomic-swap + `pip install -r requirements.txt` (only when the tarball ships one — neither app does today; the EC2 step echoes a loud skip) + `systemctl reload <app>.service`
- Rollback = one-line `aws s3 cp` of the prior tarball over `latest.tar.gz` + re-run deploy-app.sh

**Provisioning the qresev deps + data (both now have managed lanes).** Bootstrap installs only fastapi+uvicorn into `/srv/qagents/.venv`. The two extras the bars endpoint needs are each one command now: **(a) deps** — `evaluating/requirements.txt` pins `pyarrow>=17`; `deploy-app.sh qresev` stages it and the SSM step `pip install`s it (so a fresh `deploy-app.sh` after an § 8.2 replacement restores pyarrow). **(b) data** — the OHLCV parquet tree at `/srv/qagents/financial/parquet/ohlcv-equities/` (526 files, 17 MB) ships via `aws-vault exec qagents-deploy -- bash serving/scripts/ship-parquet.sh` (build tarball → `releases/qresev/data/` → SSM atomic-swap extract). Operator-fired; `SHIP_DRY_RUN=1` for the no-AWS path; pinned by `tests/cases/45-ship-parquet.sh`. So an instance replacement is `bootstrap → deploy-app.sh qresev → ship-parquet.sh`, not archaeology.

**Hazard — kernel rotation wipes post-bootstrap state.** Each `deploy-app.sh` rotates `/srv/qagents/<kernel>/` (e.g. `accounting/`, `proving/`) into `<kernel>.previous/` and unpacks the new tarball, which means `.lake/build/lib/` (the incremental kernel cache) is gone unless migrated. `deploy-app.sh` migrates `.lake/` from `<kernel>.previous/` and runs `install -d` post-rotation so the directory exists for the next build. **systemd preflight `status=226/NAMESPACE`** is the failure signature if either step is missing (the `ReadWritePaths=` mount fails). Pinned: `feedback_kernel_rotation_cache_hazard`.

**Shell access** is SSM Session Manager only (no SSH on the box):

```bash
aws-vault exec qagents-deploy -- bash serving/scripts/ssm-shell.sh
```

Filters on tag `Name=qagents-app-1`. Requires `session-manager-plugin` installed locally (`brew install --cask session-manager-plugin`).

**Smoke** (live HTTPS via Let's Encrypt cert):

```bash
curl -fsS https://api.qnarre.quantapix.com/api/health
curl -fsS https://api.qresev.quantapix.com/api/health
```

**Operator-policy gaps** — surviving items tracked in `data/next-steps/serving.md` A.1 + `INVENTORY.md` § 8; bundled into the next policy-version push per `feedback_operator_policy_gap_per_phase`.

## 8.6. Cron-EC2 lane

Serving/ owns the AWS-touching artifacts of `data/specs/cron-ec2-migration-2026-05-19/SPEC.md` — CDK deltas, EC2-side scripts + systemd units under `scripts/ec2-cron/`, ship script `scripts/deploy-ec2-cron.sh`, manifest verifier, structural test at `data/specs/serving-2026-05-26/tests/cases/40-ec2-cron.sh`. Operational deploy contract + first-fire smoke: `data/specs/serving-2026-05-26/SPEC.md` § 6.6 + § 8.3 (SDK-lane resume post-2026-06-15). Managing/ + trading/ + `code/agent_sdk/` own the out-of-serving-scope files (per-file owner tags in the spec's Appendix A.1/A.2). Reuses § 8.5's EC2 infra (`qagents-app-1` + `qagents-app-role` + `qagents-artifacts` + `alias/qagents-cmk`) — additive only.

**Operator deploy path** (mirrors § 8.5, single command):

```bash
aws-vault exec qagents-deploy -- bash serving/scripts/deploy-ec2-cron.sh
```

Same SSM mechanics as `deploy-app.sh`; no SSH. Per-routine timers enabled lane-by-lane by the owning session per spec § 8; the four shared timers (`qagents-mirror-pull`, both `qagents-tarball-build-*`, `qagents-routine@`) come up at Phase-7 first-deploy.

**Two-clock TZ model.** TZ is pinned in two load-bearing layers: (1) timers FIRE at ET via `OnCalendar=… America/New_York` on every `.timer`; (2) the routine *process* is separately pinned via `Environment=TZ=America/New_York` on all three cron `.service` units (`qagents-routine@`, both `qagents-tarball-build-*`) — without it a 22:00 ET `overnight-research` fire computes a next-day `research/<date>.md`. The box TZ stays UTC (AL2023 default; do not change it — FastAPI + Caddy + cw-agent from § 8.5 share the box). Provenance instants stay UTC (`date -u` ignores `$TZ`); `build-tarball.sh` mirrors the inline TZ for hand-run correctness. Spec § 3.4.

**Hazard — t4g.small dual-tenancy.** The cron lane shares CPU/RAM with the two FastAPI surfaces from § 8.5. `MemoryMax=1500M` per routine unit (cron-ec2-migration spec § 3.4) is the guardrail; FastAPI gets the other 500 MB minimum. If `journalctl` shows OOMs, the escalation is dedicated `qagents-cron-1` (cron-ec2-migration spec § 7.2 — ~$13/mo delta); not a re-architecture.

## 9. Pushing from this laptop (qpur) — three remotes per repo

Two qagents-class repos (`qagents`, `dot.claude` = `~/.claude/`) push to **three** remotes. Public-org GitHub push goes through `git push-quantapix` (see [[reference_quantapix_org_repos]]; source of truth `publishing/quantapix/`). **Superseded for the `/publish` path (2026-06-23, operator: gh does all GitHub work):** content now pushes via `publishing/scripts/github_meta.py sync` (`gh repo clone` → `rsync -aL` → commit → `git push` over gh's HTTPS helper); `git push-quantapix` remains for manual/non-publish pushes but carries the `-a` symlink-clobber hazard the gh arm's `rsync -aL` avoids.

```
github  → git@github-qpur:quantapix/<repo>.git           # via ed25519 SSH key
aws     → codecommit::us-east-1://<repo>                 # via aws-vault qagents-deploy
qblk    → qblk:~/repos/<repo>.git                        # via legacy quantapix RSA key
```

`remote.pushDefault = github`, `push.default = current`. `git push-all` sweeps all three in one command — skips unconfigured remotes silently, wraps the `aws` push in `aws-vault exec qagents-deploy --` automatically. Both git-subcommand wrappers live at `serving/scripts/git-push-{all,quantapix}` (public-org source of truth `publishing/quantapix/`), each symlinked onto PATH at `~/.local/bin/`. The repo-wide sweeper `scripts/push-all.sh` (root) loops `git push-all` across every qagents-class checkout.

**Key facts that bite if you forget them:**

- **CodeCommit URL form must NOT include the profile when running under aws-vault.** Use `codecommit::us-east-1://<repo>`, not `codecommit::us-east-1://qagents-deploy@<repo>`. The `@profile@` form makes git-remote-codecommit do a profile-credential lookup in `~/.aws/config` (which has no static keys — they're in Keychain), bypassing aws-vault's injected env vars.
- **Don't ever delete the only MFA device on `qagents-deploy` without registering its replacement first.** Merged policy carries a `DenyEverythingWithoutMFA` statement; with the only device gone, every `aws-vault exec` call fails until a new device is enrolled.
- **`~/.ssh/config` is locked-down per host.** No `Host *` IdentityFile, no `ForwardAgent yes`, `IdentitiesOnly yes` everywhere. The new ed25519 key (`~/.ssh/id_ed25519_github_qpur`) is GitHub-only via the `github-qpur` alias; the legacy `quantapix` RSA stays on qblk-class hosts only.
- **`git filter-repo` strips the `origin` remote** as a safety measure. After history rewrite, re-add remotes manually and force-push (rewritten history has different commit hashes).
- **The `git push-quantapix` bridge ships symlinks AS symlinks.** Its `rsync -a --exclude=.git` copies the link, not the referent — so a `/publish` run from a worktree, where `.worktree-links`-backed files (e.g. `publishing/resume/26-06-05.pdf`) are 56-byte links into canonical, would replace the real binary on GitHub with a link file (caught in the 2026-06-12 dry-run: `Bin 479128 → 56 bytes`; resume was excluded from that push). Push such slots from **canonical only**, or use `rsync -aL` (copy referents) for the affected paths. Cross-ref `data/next-steps/publishing.md` B.3.
