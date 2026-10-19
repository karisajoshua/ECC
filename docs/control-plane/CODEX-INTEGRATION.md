# Codex integration and reusable ECC adoption

## Scope and source of truth

This repository uses root `AGENTS.md` to route Codex to
`.codex/AGENTS.md`, `docs/CODEX-NAVIGATION-GUIDE.md`, and the applicable
`rules/` files. Instructions guide the agent; they do not enforce GitHub checks,
grant tool permissions, or install a plugin.

ECC has two complementary skill surfaces:

- `skills/` is canonical and is exposed by the native Codex plugin.
- `.agents/skills/` is the curated repository-local discovery surface. Use only
  relevant skills; read their bodies and referenced resources when needed.
  A checkout can use this surface without a global plugin installation.

The marketplace at `.agents/plugins/marketplace.json` points to the repository
root. Do not install the thin `plugins/ecc/` compatibility directory: its
parent-relative asset paths do not survive an isolated plugin cache.
See [native installation](../../.codex-plugin/README.md). Use this fork's reviewed
checkout when testing branch-specific control-plane guidance; installing upstream
`affaan-m/ECC` does not install this fork's foundation changes.

## Read-only smoke test first

Before installing hooks, syncing user configuration, or making repository changes:

1. Record the checkout commit and initial worktree state with
   `git rev-parse HEAD` and `git status --porcelain=v1`.
2. Run the dependency-free checks:
   `node tests/ci/codex-skill-surface.test.js` and
   `node tests/docs/codex-navigation-map.test.js`.
3. Check `codex --version` and `codex plugin list --json`. Registration alone
   does not prove skill discovery or that referenced files exist.
4. In a runtime with model access, run the following from the checkout:

   ```bash
   codex exec --sandbox read-only --ephemeral \
     'Read AGENTS.md and its Codex routing. Read the ecc-conventions
   and verification-loop skills. Summarize applicable engineering rules with
   file citations and distinguish the proposed foundation, shipped advisory
   view, and design-only TCAS hook. Do not edit files, install anything, invoke
   hooks, access secrets, call external write tools, or create commits or PRs.'
   ```

5. Compare the final worktree status to the initial status. Accept only if the
   response cites actual rules and skills, reports capability limitations,
   distinguishes advisory state from enforcement, and makes no repository edits.
   The shell sandbox does not constrain every MCP or connector; disable external
   write tools and executable hooks in the smoke-test runtime as well.

If a native plugin is already installed, also run
`node scripts/codex/check-plugin-cache.js` against its actual cache. Do not use a
source checkout as proof of an installed cache. Do not trust hooks as part of this
test. Plugin installation, hook trust, and user configuration sync are separate
write operations.

Report static tests, CLI configuration loading, plugin registration/cache checks,
and model-level instruction/skill use separately. Missing authentication, network
access, or an installed plugin is **BLOCKED** or **NOT CONFIGURED**, never PASS.
A model-level test must be repeated after setup in a capable runtime.

## Validation recorded on 2026-10-19

The baseline was a targeted source snapshot read through the GitHub connector
from `feature/engineering-control-plane-foundation` at
`1dc66121f20bcd846ad455f436fdd39a9c31508b`; the workspace had no checkout and
its proxy refused the normal clone.

- PASS before changes: skill-surface tests (4/4), navigation tests (3/3).
  The same seven checks passed after the instruction changes.
- PASS: the complete Git tree contained all five native manifest references
  (skills, MCP, hooks, icon, logo). This is source-path validation, not a cache test.
- PASS: project TOML parsed; all three role paths resolved and requested
  `sandbox_mode = "read-only"`. This does not certify effective runtime policy.
- CLI observed: `codex-cli 0.159.2`; `codex mcp list` returned no configured
  servers. `--strict-config` is not supported for that subcommand.
- NOT CONFIGURED: `codex plugin list --json` returned empty installed/available
  lists and a remote-catalog connection warning. No plugin/cache was installed.
- BLOCKED: `codex exec --sandbox read-only --ephemeral --skip-git-repo-check`
  against the baseline snapshot exited before model execution:
  `failed to initialize in-process app-server client: Read-only file system`.
  Model-level instruction following and automatic skill use remain unverified.
- NOT RUN: full repository tests, dependency audits, and Markdown lint. The
  snapshot contains the targeted instruction/skill/test surfaces, not an
  installed full repository and dependencies. No dependency files were changed.

These results do not establish cross-repository enrollment or control-plane
deployment. Repeat the model smoke in a capable Codex runtime before relying on
runtime integration.

## Control-plane boundaries

Read [FOUNDATION.md](FOUNDATION.md) for enrollment and security policy.

- Foundation: proposed / not deployed; each additional repository must opt in.
- [VIEW-CONTRACT.md](VIEW-CONTRACT.md): shipped, read-only advisory view. Its
  loopback GET endpoints describe observations; they do not enforce CI or leases.
- [TCAS-HOOK.md](TCAS-HOOK.md): design only. Codex steering is instruction-backed;
  do not claim a working blocking edit hook or durable lock.
- The [Sunshark pilot](pilots/sunshark-engineering.md) remains planned, not installed.

No repository may be reported protected, passing, deployed, or enrolled merely
because ECC instructions or a dashboard entry exist.

## Proposed reuse across other repositories

Keep ECC as the central versioned source. Do not copy the framework into each
application. This section is a proposal, not cross-repository enrollment.

1. **One installation per coding environment.** Use the native Codex plugin for
   reusable skills. For reproducibility, check out an approved full ECC commit
   outside the application repository and register that local marketplace using
   the documented native commands. Record the source commit and inspect the
   installed cache. Marketplace registration and a version string alone do not
   enforce a commit pin; upgrades need explicit review and repeat validation.
   Hooks stay untrusted until separately reviewed.
2. **A thin contract per opted-in repository.** Add a short root `AGENTS.md`
   section and a small policy record containing ECC repository, full commit,
   owner, risk tier, language rules, selected skills, real lint/test/build
   commands, and approved exceptions. Keep project-specific instructions local.
   The environment bootstrap supplies a verified ECC checkout at a documented
   absolute path (for example `/opt/ecc/<full-commit>`); instructions must tell
   Codex to read `rules/common/` and the selected language rules there.
   Plugin skills do not automatically apply the central `rules/` directory.
   A URL or SHA in AGENTS is a reference, not downloaded or enforced policy.
3. **Validate the contract before engineering writes.** Verify the local ECC
   checkout matches the recorded commit and required rule files and skills
   resolve. Use a shared, reviewed verifier in the environment bootstrap to
   reject a mismatch before a write-capable session starts. Until that verifier
   exists, perform and record the checks manually; do not call the pin enforced.
   If ECC is unavailable, report the missing policy and stop policy-dependent
   writes instead of silently claiming compliance.
4. **Central checks, small callers.** Reuse ECC's existing reusable workflow
   patterns after checking their compatibility. The current
   `.github/workflows/reusable-test.yml` hardcodes `node tests/run-all.js`;
   `reusable-validate.yml` runs ECC-specific validators. They are not universal
   application gates. A general language-aware gate is future work. Once that
   gate exists and is reviewed, each repository adds a small
   caller pinned to a full reviewed workflow commit, with explicit inputs for
   its language, package manager, risk tier, and actual check commands. Start
   with `contents: read`, explicit secret passing only where needed, and no
   execution of untrusted PR code with privileged tokens. Absent checks remain
   NOT CONFIGURED. Workflow files are proposed through repository-specific PRs.
5. **Separate proposal from enforcement.** Codex proposes fixes in PRs. GitHub
   Actions reports actual results. Human-reviewed required-check and protection
   settings provide enforcement only after the pilot proves success. No
   automatic merge, deployment, permission changes, or repository enrollment.
6. **Upgrade and rollback through PRs.** Central ECC changes produce reviewed
   pin-update PRs for opted-in repositories. Re-run the read-only smoke test and
   actual project checks. Roll back the policy pin and caller through a PR;
   remove the thin contract/caller to unenroll. Disable the environment's ECC
   plugin separately if desired; do not delete user configuration or history.

Begin with ECC itself, then an explicitly opted-in low-risk repository.
The Sunshark specification identifies missing checks and dependency preparation;
do not treat it as a ready-to-run universal template.
