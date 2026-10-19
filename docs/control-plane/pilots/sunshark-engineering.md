# Sunshark Engineering — CI pilot specification

Status: **planned; not installed**. Target repository: `karisajoshua/sunshark-engineering` (private). No modifications have been made to the target repository.

## Observed state
- Default branch: `main`.
- Vite/React application; `package.json` declares `dev`, `build`, and `preview`.
- No `lint` or `test` script declared in the inspected package file.
- Dependencies use `latest`, which can change unexpectedly.
- No `package-lock.json`, `pnpm-lock.yaml`, or `.github/workflows/ci.yml` found at the checked paths.
- GitHub repository reports `allow_auto_merge=false`.

## First pilot pull request
1. Identify the project's package manager and produce a reviewed lockfile.
2. Pin dependencies to compatible, reproducible versions after validating the current build.
3. Add a minimal GitHub Actions workflow triggered by pull requests and pushes to main:
   - checkout with minimum read permissions;
   - set up the pinned Node LTS version;
   - install with the lockfile-aware frozen install command;
   - run `npm run build` (or the actual package-manager equivalent).
4. Add lint and tests in subsequent PRs only when scripts and tests exist.
5. Protect `main` with required checks after the first successful CI run.
6. Keep deployment and automatic merging out of scope for the first pilot.

## Validation
- Build workflow succeeds on a real GitHub-hosted runner.
- A deliberate build failure produces a failed check.
- No credentials or production secrets are required.
- Workflow does not modify deployment state.
- Any changes to dependencies and lockfiles are reviewed.

## Rollback
Revert the pilot workflow and dependency/lockfile changes through a pull request. Do not bypass branch protection or force push.

## Implementation blocker
An attempted feature-branch creation in the target repository was blocked by a safety control. Do not represent the pilot as deployed or bypass that control.
