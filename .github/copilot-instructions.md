Before creating or updating a PR:

1. Install dependencies using the repository's lockfile.
2. Run lint.
3. Run unit tests.
4. Run type checking when available.
5. Run the production build.
6. Do not commit secrets or .env files.
7. Do not modify GitHub Actions security settings unless explicitly required.
8. Preserve existing CI/CD security controls.
9. Report failed checks and their root cause in the PR.
10. Do not claim a task is complete while required checks are failing.
