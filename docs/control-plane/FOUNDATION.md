# ECC Central Engineering Control Plane — Foundation

Status: proposed / not deployed. This document defines safe rollout rules; it does not install agents or grant permissions.

## Purpose
Coordinate engineering quality across repositories owned by karisajoshua while preserving each repository's independent build, deployment, and ownership.

## Operating model
- ECC provides reusable agent skills, review rules, and policy templates.
- GitHub Actions executes checks inside each opted-in repository.
- Codex or another supported coding agent may propose changes via pull requests, using least-privilege credentials.
- A future dashboard may aggregate GitHub check results; it must not imply checks are running unless GitHub reports them.

## Enrollment
1. Inventory repositories, including pagination beyond the first 100 results.
2. Identify owner, language, package manager, default branch, deployment provider, and existing CI.
3. Classify each repository: experimental, standard, production, or sensitive.
4. Explicitly opt in each repository. Do not push workflows or change settings during discovery.
5. Deploy a minimal CI workflow on a feature branch and review its first run.
6. Add optional automated PR suggestions after CI is stable.

## Risk tiers
| Tier | Examples | Merge policy |
| --- | --- | --- |
| Experimental | prototypes and sandboxes | auto-merge may be enabled after checks |
| Standard | websites and noncritical apps | auto-merge only for approved low-risk changes |
| Production | customer-facing applications | required checks and review |
| Sensitive | payment, auth, identity, personal data, financial systems | human approval; no unattended deployment |

## Minimum checks
- Language-specific lint and type checking where applicable.
- Unit tests and build validation.
- Dependency and secret scanning.
- Pull-request diff review, with explicit attention to auth, payments, database migrations, and permission changes.
- Report unsupported or absent checks as NOT CONFIGURED, never PASS.

## Security boundaries
- Use GitHub App installation tokens with minimal repository access and short expiration.
- Do not store tokens, customer data, or production secrets in ECC repository files.
- Restrict untrusted pull-request code execution and third-party Actions permissions.
- Do not grant agents unrestricted access to production credentials.
- Require human review for high-risk changes, permission escalation, branch protection changes, and production deploys.
- Keep audit logs and reversible changes.

## Proposed initial pilot
1. ECC itself: validate current workflows, permissions, and maintainability.
2. A low-risk opted-in repository: introduce a reusable quality gate.
3. A representative React app: verify build/test compatibility.
4. A Python/Rust project: validate language-specific templates.
5. Expand only after documented success.

## Dashboard status schema (proposal)
For each repository: name, tier, enrollment status, default branch, CI configured, last check conclusion, open PR count, security alerts where permitted, deployment provider, last deployment status, and last verified timestamp.

## Acceptance criteria
- Every enrolled repository has a documented owner and tier.
- CI reports genuine results and fails closed on required-check failures.
- No agent merges sensitive changes without approval.
- Existing deployment and production workflows remain intact.
- Rollback and removal instructions are documented before enabling automated writes.

## Current verification
- GitHub repository ECC found under karisajoshua, default branch main.
- ECC README/package describe version 2.2.3 and multiple agent environments.
- ECC contains .github/workflows/ci.yml.
- Initial repository inventory returned 100 repositories; it is not a complete count.
- No cross-repository deployment or agent activation has been performed.
