# serving — AWS cloud-base

Project-specific rules for the qagents AWS cloud-base. Cross-project rules:
root `CLAUDE.md`. (Account IDs, ARNs, distribution / instance / device
identifiers, and IAM principal names are deliberately omitted from this
public mirror — they live only in the private working tree.)

## 1. Single source of truth for AWS

Three layers, each with a distinct job:

- **The target contract** (a dated spec) — every cloud resource (S3,
  CloudFront, ACM, Route 53, IAM, EC2, KMS, SSM, CloudWatch), current and
  forward-looking, described as we want it to be: locked decisions,
  identity model, deploy contracts, scale-up paths, runbooks, open work.
- **`INVENTORY.md`** — the curated narrative of current AWS reality, with a
  drift-items section cross-referenced to the spec. When the spec and
  reality diverge in a way that's not a tracked drift item, the spec is
  wrong — fix it in the same change.
- **`inventory/<date>/`** — the verifiable backing: an exhaustive
  structural dump of every AWS service, captured as root in CloudShell
  (the deploy principal's MFA-Deny blocks some enumeration). The git diff
  between two dated snapshots is the canonical change report.

Other subprojects' CLAUDE.md files MAY name a single resource but never
document AWS configuration — that is `serving/`'s job exclusively.

## 2–3. Locked decisions + universal tags

The locked decisions (an OIDC role for CI, build-tarball deploys, a chosen
reverse proxy, CDK in TypeScript, a single shared EC2 instance, a unitary
deploy IAM principal, ≥ 2 virtual MFA devices) are load-bearing — change
them only via a deliberate spec amendment, never a one-off script tweak.
Every taggable resource carries universal tags (`Project`, `Owner`, `Env`,
`Component`, `ManagedBy`) applied centrally from `cdk/lib/shared/tags.ts`;
any resource missing one fails `cdk synth` lint. Lint enforces tag
*presence*, not value, so use the central helper — an inline tag would pass
silently while violating canonical values.

## 4. Diagram kit (`serving/diagrams/kit/`)

The Quantapix-branded diagram primitives + layouts live here as the
`@qagents/diagram-kit` workspace package — the **legitimate shared-code
seam** for cross-subproject diagram primitives + the kit-owned status-hub
schema. It just lives inside the `serving/` tree because that's where the
work was first scaffolded; anyone may import it. The kit's display-mode
contract — the closed set of `*Emit` schemas (Diagram, Table, StatCard,
KpiStrip, FilterChipGroup, Dashboard) and what stays consumer-owned (Chart,
Graph, 3D-mix, Video, App-shell) — is fixed by a dated spec; adding an emit
kind requires a kit minor bump + spec amendment + e2e coverage. Consumers
must rebuild the kit before their own typecheck/build/dev via `pre-X` hooks.

## 5. Diagram prompts are voice-controlled

The design prompts enforce Quantapix branding, an engineer-debugging-a-system
voice on labels (no marketing fluff), and a shape-agnostic Node primitive
(no AWS-service glyphs). The same prompt shape drives the Lean4
proof-graph rendering kit consumed by `verifying/web/`.

## 6. Scope boundary — absolute, no staging

`serving/` does not import from any other subproject; the reverse is also
forbidden. The rule is absolute: no temporary cross-imports, no staging
step, no workspace-package-as-data-shim. Cross-subproject contracts are
JSON/parquet under the shared-data hub only. The single allowed shared-code
seam is `@qagents/diagram-kit` (everyone-imports-from-shared-kit, same
pattern as the vendored memsearch + shared Playwright helpers). The CDK app
is the only place that references AWS account IDs, ARN literals, or
distribution IDs; subprojects read their bucket name + distribution id from
a per-host env file, never inline.

## 7. Status emit (`data/status/serving.json`)

`scripts/status_emit.ts` writes three graph-shaped architecture diagrams
(static-sites / app-api / identity), three `TableEmit` panels, and two
`DashboardEmit` panels (service-inventory, security-baseline), plus a
live-state strip, interleaved via an explicit panel ordering. Per-node
`details` is an HTML string (rendered via the consumer's set-html, not an
escaping expression). Naturally tabular content ships as a `TableEmit`, not
an edgeless grid diagram; tables that benefit from a header strip +
state-aware filtering wrap into a `DashboardEmit`; the diagram is kept only
when cells need visual grouping or inspector details. Edgeless node sets
must render with the kit's grid layout, not the dagre layout (dagre
collapses a zero-edge node set to one rank).

## 8. AWS deploys (S3 + CloudFront sites)

Every Astro site follows the same deploy contract; per-site bucket +
distribution differ, the script shape and credential workflow do not.

- **Credentials — a secrets-vault tool + the OS keychain (no plaintext keys
  on disk).** A single unified deploy IAM principal, two virtual MFA
  devices (primary + backup), one vault profile, one keychain entry.
  Blast-radius isolation lives in policy-level MFA-Deny + a 1-hour STS
  window, not principal multiplication.
- The principal carries a scoped customer-managed policy — never a
  broad managed policy like S3-full-access. Policy updates are self-serve
  from the workstation via a create-policy-version recipe (mind the
  5-version cap); never the inline-policy form.
- **Deploy script** — parameterized by per-host env files (bucket,
  distribution id, profile, site dir, an optional protected-paths array).
  It sources the env, builds the optional profile flag only when not under
  the vault, wipes the bucket by default (reversible via versioning), runs
  a two-pass `s3 sync --delete` (HTML short-cache; everything else
  immutable), then invalidates the distribution.

**Large binary media — five paths by shape:** published video deliverables
→ a public videos CDN bucket via an upload script; one-off small media ride
the site deploy under an immutable header; interim scratch binaries mirror
to a private lifecycle-tiered backup bucket; durable version-pinned
artifacts (the full U.S. Code corpus, the market-data parquet hub) → a
content-addressed archive bucket via an archive script; an opt-in local
mirror of CDN videos survives worktree teardown via a protected-paths list.

**Hazard — protected paths.** A binary must exist in the *building*
worktree's `dist/`, but worktrees don't carry gitignored files; a deploy
from a fresh worktree without the binary would wipe the live copy. Fix: a
per-host protected-paths array threaded through the wipe and both sync
passes. **New-distribution checklist:** the OAC bucket policy, the
URI-rewrite function (Save → Publish → attach to Viewer-request — Publish
is easy to miss), and `403→/404.html` + `404→/404.html` error responses,
then invalidate + run live e2e. **Internal anchored links** must include
the trailing slash before the hash (`/route/#anchor`), or static hosting
costs a redirect round-trip. **Live smoke test after every deploy** — a
clean exit only proves S3 was written; the Playwright suite doubles as a
deploy verifier when pointed at the remote URL. A CI lane runs the same
deploy script under an OIDC role, triggered manually or on changed
`*/web/**` paths, with per-site concurrency queued (a half-applied
wipe+sync is worse than waiting).

## 8.5–8.6. App-server + cron EC2 lanes

A shared EC2 instance hosts both app servers (Qnarre + Qresev FastAPI)
behind a reverse proxy, plus a cron lane. The deploy contract carries no
repo credentials onto EC2: rsync → tarball → artifacts bucket, then SSM
runs fetch + atomic-swap + reload. **Hazard — kernel rotation wipes
post-bootstrap state:** each deploy rotates the kernel dir and unpacks the
new tarball, so the incremental Lean build cache is gone unless migrated; a
systemd namespace preflight failure is the signature if the migration or a
read-write-path mount is missing. Shell access is session-manager only (no
SSH). The cron lane shares the instance with the FastAPI surfaces under a
per-routine memory cap; timers fire at ET wall-clock and the routine
process is separately pinned to ET while the box stays UTC (without the
process pin, a late-evening routine that crosses the UTC day boundary would
compute the wrong date).

## 9. Pushing from the workstation — three remotes per repo

The two qagents-class repos push to **three** remotes (a GitHub mirror, a
CodeCommit mirror via the vault, and a legacy bare-repo host). A
`push-all` wrapper sweeps all three, skipping unconfigured remotes and
wrapping the CodeCommit push in the vault automatically. Public-org GitHub
pushes go through a separate `push-quantapix` bridge (owned by
`publishing/`). Facts that bite if forgotten: the CodeCommit URL must NOT
embed the profile when running under the vault; never delete the only MFA
device on the deploy principal without enrolling its replacement first (a
DenyEverythingWithoutMFA statement would lock out every call); the SSH
config is locked down per host (`IdentitiesOnly`, no wildcard identity).
