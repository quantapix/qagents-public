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

`@qagents/diagram-kit`, the chartered shared-code seam (§ 6) — emit-kind contract, design-bundle location + sync + P4 re-target, and the consumer `pre-X` rebuild rule: `serving/diagrams/kit/README.md` (single owner).

## 5. Diagram prompts are voice-controlled

`serving/diagrams/0X-*.prompt.md` are Claude Design prompts — branding/voice/primitive rules + the Design-round promotion pin: `serving/diagrams/kit/README.md` § "Diagram prompts (voice-controlled)".

## 6. Scope boundary — absolute, no staging

`serving/` does not import from any other subproject; the reverse is also forbidden. The rule is absolute: **no temporary cross-imports, no Phase-A staging step, no workspace-package-as-data-shim.** Cross-subproject contracts are JSON/parquet under `data/<topic>/<sub>.*` only.

The single allowed shared-code seam is `@qagents/diagram-kit`. Both producers (a subproject's `status_emit` script, etc.) and consumers (`designing/web`'s `/status` page) may depend on the kit. That is **not** a cross-subproject import — it's everyone-imports-from-shared-kit.

The CDK app is the only place that references AWS account IDs, ARN literals, or distribution IDs. Subprojects continue to read their bucket name + distribution ID from `serving/sites/<host>.env`, never inline (`INVENTORY.md` § 2 is the curated mirror).

## 7. Status emit (`data/status/serving.json`)

`scripts/status_emit.ts` writes `data/status/serving.json`: three graph-shaped architecture diagrams transcribed from `serving/diagrams/0[1-3]-*.prompt.md` (static-sites / app-api / identity), plus `TableEmit` + `DashboardEmit` panels and a live-state strip, interleaved via an explicit `panels[]` ordering. The exact panel set is pinned by `data/specs/serving-2026-05-26/tests/cases/80-status-emit-shape.sh` — extend the test with the emit.

Per-node `details` is an **HTML string** (rendered by the consumer via Astro's `set:html`, not `{expr}` which would escape entities). Keep detail prose factual — services + costs + scope phrasing matching `data/specs/serving-2026-05-26/SPEC.md`.

Diagram-vs-`TableEmit`-vs-`DashboardEmit` choice: memory `project_diagram_kit` § grid/Table/Dashboard judgment (a rule for every emitter); none of serving's panels is edgeless today.

The summary diagram surfaced on the index card is `static-sites`. Status-pill for serving: `OK` steady-state; `BUILDING` only while a `cdk deploy` is in flight.

## 8. AWS deploys (S3 + CloudFront sites)

Every Astro site under qagents (four today — see `./sites/*.env`; any future sibling) follows the same deploy contract. Per-site bucket + CloudFront distribution differ; the script shape, credential workflow, and verification cadence do not.

**Credential workflow — aws-vault + macOS Keychain (no plaintext keys on disk):**

- **Single unified IAM principal `qagents-deploy`** — one IAM user, two virtual MFA devices (primary + backup), one aws-vault profile, one Keychain entry. Locked at `data/specs/serving-2026-05-26/SPEC.md` § 2 decisions 7 + 8. Blast-radius isolation lives in policy-level MFA-Deny + 1h STS window, not principal multiplication.

  Each site's `<sub>/web/.env` pins `AWS_PROFILE=qagents-deploy` (per-site bucket + distribution IDs stay in `./sites/<host>.env` only — § 6); unified profile block at `./templates/aws-config.snippet`. Same principal pushes to CodeCommit for `qagents` + `dot.claude` (§ 9).

- `aws-vault add <profile>` — long-term IAM keys go to Keychain. `~/.aws/credentials` stays empty.
- `~/.aws/config` is metadata only (no credentials) — shape owned by `./templates/aws-config.snippet`, which says **do NOT add a `[default]` block**: with none, an unwrapped command errors `NoCredentials` instead of silently routing somewhere. Both workstations had drifted to one carrying `login_session = …:root`, so unwrapped botocore defaulted to a **root** session — invisible, because every deploy path is wrapped and only the unwrapped read lane (`git fetch aws`) hit it. Removed on both 2026-08-06 (ns:serving/72(b), operator-ruled; backups `~/.aws/config.pre-default-removal-2026-08-06`). Every deploy command selects `qagents-deploy` explicitly.
- IAM principal carries TWO scoped customer-managed policies (unitary principal; split 2026-08-01 at IAM's 6,144-char cap): `./policies/qagents-deploy.json` (main, frozen at cap) + `./policies/qagents-deploy-aux.json` (overflow). Sid list + rationale: `data/specs/serving-2026-05-26/SPEC.md` § 4.2. **Never** `AmazonS3FullAccess`. Inline-policy form retired — see `reference_iam_user_inline_policy_2kb_cap`.

  **Policy update workflow — self-serve from the laptop:** runbook at `./runbooks/policy-version-push.md` (§ B main / § C aux — `create-policy-version --set-as-default`, 5-version cap + `LimitExceeded` recovery, bootstrap). Never `put-user-policy` against this user — that recreates the retired inline-policy shape.

**Deploy script shape — `./scripts/deploy-site.sh <host>`** (full contract — env keys, cache policy, invalidation — at `data/specs/serving-2026-05-26/SPEC.md` § 5.3): sources the committed per-site `./sites/<host>.env`, wipes the bucket (skip: `DEPLOY_NO_WIPE=1`; reversible via bucket versioning), two-pass `aws s3 sync --delete`, then invalidates `/*`. Each site's `package.json` `deploy` runs `pnpm build && bash ../../serving/scripts/deploy-site.sh <host>`.

**Gotcha:** the script adds `--profile` only when **not** running under aws-vault (marker: `AWS_VAULT` env var) — under aws-vault, ambient credentials are present and `--profile` would trigger an empty `~/.aws/credentials` lookup → `Unable to locate credentials`.

Standard invocation: `aws-vault exec qagents-deploy -- pnpm -C <sub>/web deploy`.

**Large binary media — five paths depending on shape** (video-CDN / small-media / clips-backup / archive-backup / CDN-mirror): `data/specs/serving-2026-05-26/SPEC.md` § 5.4 owns the table + per-path detail.

**Hazard + structural fix — `PROTECTED_PATHS`** (small-media path). Worktrees don't carry gitignored binaries, so a `pnpm deploy` from a fresh worktree runs the wipe + `s3 sync --delete` without them, 404ing the live asset. Fix: a per-site `PROTECTED_PATHS` bash array in `./sites/<host>.env`, threaded as `--exclude` through the wipe AND both sync passes (set on `quantapix.com.env`; femfas.net needs none). Deletion-guard only — binary updates still go via `aws s3 cp` + targeted invalidation.

**Sibling hazard — archive `dir` bundles from canonical only** (root § Canonical-shared gitignored content: walkers must dereference or hard-refuse; a worktree push would tar the link entry alone). `bundle_dir()` hard-fails on a symlinked source and prints the canonical re-invocation; `file` bundles are immune. **Push `parquet` from canonical.** Detail: `data/specs/serving-2026-05-26/artifact-archive-s3-2026-05-29/SPEC.md` § 3.5; memory `project_parquet_gitignored_ground_truth`.

**`verify` vs `verify-content`.** `verify` hashes the compressed TAR — right for push idempotence, but it moves with the container *and* with mtimes, so the 80 of 84 `usc-waves` predating the 2026-07-22 ustar→pax flip report DRIFT **forever** while holding identical files. **Expected; not a durability signal; never re-push to silence it, and never compare DRIFT counts across hosts** (the sha is per-host). `verify-content` is the durability check — container/mtime-independent, a download per bundle ⇒ on-demand. Ruling + full mechanics: same spec § 2; memory `project_serving_subproject`. **A shared verb whose new flag consumers must adopt to keep a check meaningful owes a "consumers owing adoption" note here** — the wrapper axes are a known, enumerable set (`proving/dau.sh`, `accounting/dat.sh`, whatever `studying/` grows), and a thorough script-header doc still left one axis three days unable to ask the durability question.

**CLEAR-4 push-ledger completeness gate — `verify-push-ledger.sh`** (ruling: signoff-framework SPEC § 11 q.2; modes + surfaces in `serving/sites/quantapix.com.env`; pinned by `data/specs/serving-2026-05-26/tests/cases/21-push-ledger-gate.sh`). `deploy-site.sh` runs it **before the wipe** for any site setting `SIGNOFF_LEDGER_GATE=1` (only `quantapix.com.env` today), diffing live S3 objects against `data/publishing/push-ledger.jsonl` — canonical ∪ the `QAGENTS_PENDING_ROOT` overlay (R5). A live object with no ledger line is a breach; **STRICT** on `cdn` aborts pre-wipe (exit 3), `site-thumb` stays report-only pending R16 (spec § 5.4). `push-ledger.jsonl` is a GENERATED projection of `ledger.push_event` — never hand-append. Managing does NOT run this (observe-only on AWS). **Say WHAT you hash:** this ledger's `content_sha256` digests the **pushed binary object itself**; `evaluating/`'s identically-named clearance-record field is a roll-up over that record's `faces[]`. Two digests one level apart sharing a field name is a silent false-negative generator — it read a properly-cleared CDN push as a FALSE `UngatedPush` in `/dao` CLEAR-3f.

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

Different surface from § 8 static-site deploys. EC2 instance `qagents-app-1` hosts both `verifying/` (qnarre, :8787) and `evaluating/` (qresev, :8788) FastAPI servers behind Caddy on `api.{qnarre,qresev}.quantapix.com`; t4g.small sizing assumes mathlib-free kernels. Bootstrap pre-warms the kernels' Lean toolchain — `LEAN_TOOLCHAIN` in `scripts/bootstrap-ec2.sh` MUST stay in lockstep with `{proving,accounting,studying}/lean-toolchain`. Full topology: `serving/INVENTORY.md` § 2.5 + spec § 6; AMI-drift / deliberate-replacement cycle: spec § 8.2. Live-state items tracked in `data/next-steps/serving.md`.

**Deploy contract (spec § 2 dec. 2 — no repo credentials on EC2):**

```bash
aws-vault exec qagents-deploy -- bash serving/scripts/deploy-app.sh {qnarre|qresev|both}
```

- rsync server/ → tarball → `s3://qagents-artifacts/releases/<app>/<sha>.tar.gz` + `latest.tar.gz` pointer
- `aws ssm send-command` runs fetch + atomic-swap + `pip install -r requirements.txt` (only when the tarball ships one — qresev does for pyarrow, qnarre ships none; the EC2 step echoes a loud skip when absent) + `systemctl reload <app>.service`
- Rollback = one-line `aws s3 cp` of the prior tarball over `latest.tar.gz` + re-run deploy-app.sh

**Provisioning the qresev deps + data.** Bootstrap installs only fastapi+uvicorn; `deploy-app.sh qresev` stages `evaluating/requirements.txt` (pyarrow) for the SSM pip step, and the OHLCV tree ships out-of-band via `serving/scripts/ship-parquet.sh` (operator-fired; contract + `SHIP_DRY_RUN=1` in spec § 6). Instance replacement = `bootstrap → deploy-app.sh qresev → ship-parquet.sh`, not archaeology.

**Hazard — kernel rotation wipes post-bootstrap state.** `deploy-app.sh` rotates `/srv/qagents/<kernel>/` into `<kernel>.previous/`, so it must migrate `.lake/` back + `install -d` post-rotation. Failure signature if either step is missing: systemd preflight `status=226/NAMESPACE`. Detail: `feedback_kernel_rotation_cache_hazard`.

**Shell access** is SSM Session Manager only (no SSH on the box):

```bash
aws-vault exec qagents-deploy -- bash serving/scripts/ssm-shell.sh
```

Filters on tag `Name=qagents-app-1`. Requires `session-manager-plugin` installed locally (`brew install --cask session-manager-plugin`).

**Shared ledger store — LAN primary on qred** (owner: `data/specs/shared-ledger-store-2026-07-09/ledger-lan-primary-2026-07-19/SPEC.md` § 5–§ 7 — topology, TLS/role model, two-tier backups, cutover phases): qred `18-main` @ **5432** over direct LAN links, **no tunnel**. Tooling `serving/scripts/pg-lan/` + `migrate-ledger-to-lan.sh`; runbook `serving/runbooks/ledger-lan-cutover.md`. **L3 (RDS freeze → snapshot → destroy) unblocked 2026-08-01** — the scoped `rds:*` group is live in companion policy `qagents-deploy-aux`; run freeze→snapshot in ONE sitting (ns-30). **The SSM tunnel machinery SURVIVES L3** (retirement removes the RDS endpoint, not the lane). DB-gated suites use a disposable DB on qred, never prod. **DSN handling:** one at-rest copy, `~/.config/qagents/ledger.dsn` mode 600, injected per invocation, NEVER exported from a shell profile — `.zshenv` is sourced by every zsh, leaking the password to every process (`data/specs/memsearch-pg-flip-2026-07-21/SPEC.md` § 2 amendment).

**Smoke** (live HTTPS via Let's Encrypt cert):

```bash
curl -fsS https://api.qnarre.quantapix.com/api/health
curl -fsS https://api.qresev.quantapix.com/api/health
```

**Operator-policy gaps** — surviving items tracked in `INVENTORY.md` § 8 + `data/next-steps/serving.md` § A; bundled into the next policy-version push per `feedback_operator_policy_gap_per_phase`.

## 8.6. Cron-EC2 lane

Serving/ owns this lane's AWS-touching artifacts; the ownership roster, SSM/timer mechanics, and the t4g.small dual-tenancy `MemoryMax=1500M` hazard: `data/specs/cron-ec2-migration-2026-05-19/SPEC.md` Appendix B (single owner). Reuses § 8.5's EC2 infra — additive only.

**Operator deploy path** (mirrors § 8.5, single command):

```bash
aws-vault exec qagents-deploy -- bash serving/scripts/deploy-ec2-cron.sh
```

**Two-clock TZ model** (owner: `data/specs/cron-ec2-migration-2026-05-19/SPEC.md` § 3.4 — rationale + the unit roster). BOTH layers are required: timers FIRE at ET (`OnCalendar=… America/New_York` on every `.timer`) AND the routine *process* is pinned (`Environment=TZ=America/New_York` on all three cron `.service` units) — else a 22:00 ET fire computes a next-day date. Box TZ stays UTC; do NOT change it (FastAPI + Caddy + cw-agent share the box). `date -u` ignores `$TZ`.

## 9. Pushing from the canonical-role holder (qpur by default) — four remotes per repo

Two qagents-class repos (`qagents`, `dot.claude` = `~/.claude/`) push to **four** remotes. Public-org GitHub content pushes via `publishing/scripts/github_meta.py sync` (owned by `publishing/CLAUDE.md` § 4–5; [[reference_quantapix_org_repos]]; source of truth `publishing/quantapix/`); `git push-quantapix` remains for manual/non-publish pushes only — symlink-clobber hazard below.

```
github  → git@github-qpur:quantapix/<repo>.git           # via ed25519 SSH key
aws     → codecommit::us-east-1://<repo>                 # via aws-vault qagents-deploy
qblk    → qblk:~/repos/<repo>.git                        # via legacy quantapix RSA key
qred    → qred:~/repos/<repo>.git                        # same key; second LAN bare mirror
```

The qblk + qred bare mirrors double as the LAN git-exchange fabric for the network nodes (§ 10). `remote.pushDefault = github`, `push.default = current`. `git push-all` sweeps all four in one command (an unconfigured remote is reported `skip (not configured)` in the summary, not omitted; wraps the `aws` push in `aws-vault exec qagents-deploy --`); wrappers live at `serving/scripts/git-{push-all,push-quantapix,fetch-all}`, symlinked onto PATH at `~/.local/bin/`.

**The roster IS fingerprinted since 2026-08-06 — `parity.sh` `env.remotes`.** It emits the sorted remote-NAME set per qagents-class repo (names, not URLs: URLs carry the per-host `github-qpur` alias and would mint noise between two correct hosts), and is compared **outside** the same-profile guard on purpose — a remote roster has nothing to do with which venv extras a host requested, so leaving it inside would let a profile mismatch suppress a missing mirror. Until then nothing checked it: `env.wrappers` fingerprints whether the wrapper SCRIPTS resolve, never the remotes they push to, so qyel sat 3-of-4 on `qagents` and 2-of-4 on `dot.claude` undetected (found by a `git fetch aws` failing `'aws' does not appear to be a git repository` — not the MFA error expected). Still `git remote` BOTH repos when provisioning a new host: **a new fingerprint field reads `unmeasured` until BOTH hosts have re-published carrying it**, so the gate is blind to this class on any host whose last publish predates the field.

**`git fetch --all` is BROKEN by construction — use `git fetch-all`** (ns:serving/72(a)): the `aws` leg needs the aws-vault wrap and git has no per-remote command hook, so push was wrapped from the start and fetch never was. It deliberately omits push-all's hub FF-guard — that guard refuses a divergent *write*, while updating remote-tracking refs is how a divergence is discovered. Sweeper `scripts/push-all.sh` loops it across every qagents-class checkout, folding `--tidy` after. **Fail-closed:** `git push-all` runs the FF-guard before pushing `main` (exit 30). Owner: `data/specs/push-pull-redesign-2026-07-18/SPEC.md` § 5 + § 9.

**Key facts that bite if you forget them:**

- **CodeCommit URL form must NOT include the profile when running under aws-vault.** Use `codecommit::us-east-1://<repo>`, not `codecommit::us-east-1://qagents-deploy@<repo>`. The `@profile@` form makes git-remote-codecommit do a profile-credential lookup in `~/.aws/config` (which has no static keys — they're in Keychain), bypassing aws-vault's injected env vars.
- **Don't ever delete the only MFA device on `qagents-deploy` without registering its replacement first.** Merged policy carries a `DenyEverythingWithoutMFA` statement; with the only device gone, every `aws-vault exec` call fails until a new device is enrolled.
- **`~/.ssh/config` is locked-down per host.** No `Host *` IdentityFile, no `ForwardAgent yes`, `IdentitiesOnly yes` everywhere. The new ed25519 key (`~/.ssh/id_ed25519_github_qpur`) is GitHub-only via the `github-qpur` alias; the legacy `quantapix` RSA stays on qblk-class hosts only.
- **`git filter-repo` strips the `origin` remote** as a safety measure. After history rewrite, re-add remotes manually and force-push (rewritten history has different commit hashes).
- **The `git push-quantapix` bridge ships symlinks AS symlinks** (`rsync -a` copies the link, not the referent) — a push from a worktree would replace a `.worktree-links`-backed binary on GitHub with a link file. Push such slots from **canonical only**. (`/publish` is immune — `github_meta.py sync` uses `rsync -aL`.)

## 10. Local network — qblk / qred / qyel nodes + `ssh aws-1`

Owner: `data/specs/serving-2026-05-26/local-network-2026-07-12/SPEC.md` (node roster + IPs, SSH identity model, git topology, tmux contract, Postgres, backup lanes, access-ergonomics + root-account runbooks). This section is entry points + hazards only.

- **Remote sessions:** `bash serving/scripts/net-shell.sh {qblk|qred|qyel|aws-1}` attaches-or-creates the `qagents` tmux session (plain-shell fallback where tmux is absent).
- **LAN reachability is per-APP gated (macOS 15+ Local Network Privacy) — `Undefined error: 0` (errno never set) means a denied grant, not a dead node.** The grant belongs to the app that launched the shell (`cmux.app`), never to `ssh`; first probe is the same command from another app's shell, never a mirror or key investigation. Blast radius, the fix, and the three counter-signatures that RULE IT OUT (a real errno, a diurnal pattern, a launchd subject): memory `reference_macos_local_network_privacy_errno_zero`.
- **`ssh aws-1`** — SSH to `qagents-app-1` over an SSM tunnel (no public port 22; MFA stays the boundary). `Host aws-1` → `serving/scripts/ssm-ssh-proxy.sh` (resolves by Name tag, survives § 8.2 replacement); one-time key install: `serving/runbooks/ec2-ssh-over-ssm.md`; `ssm-shell.sh` remains the zero-setup fallback. Login user `ec2-user`; `sudo -u qagents` for `/srv/qagents`.
- **Git rule:** nodes work on `<node>/<topic>` branches pushed back to the qblk/qred bare mirrors; the canonical-role holder merges in a normal `/open` session and `git push-all` propagates — guarding the AUTHORITY as well as the mirrors and aborting the sweep when it rejects (2026-07-27); `/close` reports an undrained `main` but never pushes. **Non-role-holding** nodes never write `main`. *Canonical is a ROLE, not a hostname* (spec § 4.1; role-capable = {qpur, qyel}), and CR-3 makes the `<root>` checkout path an INVARIANT — every hardcoded canonical path in `scripts/` relies on it. **A lagging `push-all` stalls the whole leaf lane** — check `git rev-list --count qblk/main..main` before relaying `/pull`'s (leaf-shaped) exit-15 remedy a second time.
- **Node bring-up / "works over ssh, fails under launchd":** `runbooks/node-bring-up.md` (owner). Two invariants: an ssh shell and launchd have *different* missing pieces (Keychain / agent / homebrew `PATH`) — probe by absolute path; and sync a node by **pushing from the role holder**, never `git pull` on the node.
- **Node roster projection:** `serving/local-network/nodes.txt` — machine-readable mirror of the spec § 2 roster (consumers: `scripts/pull.sh` ref-scoping, managing AUDIT-C4).
- **LAN backups:** `bash serving/scripts/backup-to-node.sh {qblk|qred} [videos|waves|trading|memsearch|memsearch-subs]`; restore via `restore-from-node.sh` (tape moves through `scripts/sync-ground-truth.sh` only). Contract owner — per-source-host destination prefixes, `--delete-after` scoping, preflight + superset refusal, `BACKUP_DRY_RUN=1`: `data/specs/workstation-parity-2026-07-21/SPEC.md` § 5. Sources are hardcoded to canonical (worktree-symlink hazard class). Cron `serving:node-backup` 01:30 ET; the S3 leg is qred's nightly job. Two standing hazards: **present-but-EMPTY source hard-refuses UNLESS in `PROSPECTIVE_WAVE_SOURCES` — keep lockstep with `capability.sh have_waves`** (a disagreement pinned `exit=1` six days and masked a real outage; witness `t_14`); and **`memsearch-subs` is LAN-ONLY by construction** — widening `pg-nightly-backup.sh`'s S3 loop to iterate all classes is an unruled disclosure decision, not a bug (store-durability § 11.4).
- **Store durability** (`data/specs/store-durability-2026-07-26/SPEC.md`, promoted 2026-07-28): all three tiers live — qblk streaming standby, WAL+PITR, nightly dump. Three-layer health chain: `pg-health-probe.sh` renders facts on both nodes (04:30 ET, **grades nothing**), `pg-health-assert.sh` grades them **from the workstation** in the 01:30 `serving:node-backup` fire (absence is FAIL, never skip), cases 91–94 pin the monitors going red with no network. **That family's `tests/run.sh` IS `/do-retire`'s P0 gate**: REFUSES (exit 3) with no verify cluster, exit 1 on any NOT-RUN arm — a green licenses deletion downstream; `verify-target.sh` resolves local-or-ssh, so it runs unchanged from a PostgreSQL-less host. **Hazard, permanently true:** `provision-pg-lan.sh` truncates `conf.d/qagents.conf` and restarts — durability GUCs live only in `conf.d/qagents-durability.conf`. Retention lane, the drill's absent-sentinel proof, archive mode `postgres:qpix 2750`, A6b's coupling to `PG_BASEBACKUP_KEEP`, and the daily-glob cost tripwire: that spec + its `tests/README.md` + memory `project_serving_subproject`; never grade one periodic artifact against a differently-periodic one (`feedback_cross_cadence_grading_is_a_clock_check`).
- **Credential rotation — four rules minted by the 2026-07-30/31 pg loss-and-recovery.** (a) A session rewriting a **host-scoped** secret seat MUST assert `hostname` FIRST (memory `feedback_assert_hostname_before_host_scoped_secret_write`). (b) Verification is a **live probe FROM each seat host** — a cross-host hash compare passes while both copies are burned (`feedback_one_secret_two_at_rest_copies`). (c) `provision-pg-lan.sh` is committed mode 644, so the recipe is `sudo bash <path>`, never `sudo <path>`. (d) The sweep is not the two laptops — **qblk's `~/.pgpass` holds qagents rows too**, and stopping at qred leaves qblk's restore-verify lane failing auth. Incident detail: memory `project_serving_subproject`.
- Sibling cron `serving:ledger-daily` 05:20 daily — `qagents.ledger.import_logs` + `flush` (spool drain) against the LAN DSN (`~/.config/qagents/ledger.dsn`, direct qred link, no MFA/tunnel); mechanics: `data/specs/shared-ledger-store-2026-07-09/SPEC.md` § 13.
- **Postgres:** **qred `18-main` @ 5432 is the shared-ledger-store LAN primary** (spec § 6, first adoption consumed by `ledger-lan-primary-2026-07-19`); qblk `18-main` @ 5432 is backup/restore-verify. RDS frozen→retired at that subspec's L3. Provisioning: `scripts/provision-pg-lan-push.sh {qred|qblk}`; cutover runbook `runbooks/ledger-lan-cutover.md`. **Since 2026-07-28 the store also carries `archive.blob`/`archive.sweep`** (`code/ledger/.../schema/006_archive.sql`, applied to prod `qagents` + `qagents_test`), `/do-retire`'s durability tier for **untracked** content. That changes what a restore drill protects — but **not uniformly, and the split is the load-bearing part**: the `recoverable=none` lanes are the ONLY copy while the rest are `recoverable=git` projections, so a drill exercising the table as one population under-tests exactly the lanes that matter. Take the per-lane split from `data/specs/do-retire-2026-07-26/lanes.tsv` col 4, never from a remembered figure; growth is bounded by the per-lane TTLs.
- **Mirror-guard:** `bash serving/scripts/harden-mirrors.sh [--verify]` — per-ref `update` hook on both nodes' `qagents.git` + `dot.claude.git` protecting `refs/heads/main` (non-FF + delete refused; `<node>/*` stays deletable for `/pull --tidy`). Installed + live-verified 2026-07-20 (ns-27).
