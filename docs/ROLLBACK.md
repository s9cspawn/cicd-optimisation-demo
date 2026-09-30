# GitHub Pages rollback runbook

Every successful optimised pipeline run retains the tested `dist/` directory for 30 days as `site-<commit-sha>`. The rollback workflow redeploys that immutable artifact and does not reinstall dependencies or rebuild source.

## Procedure

1. Open the successful historical **CI/CD Pipeline** run that deployed the required version.
2. Copy its numeric run ID from the run URL.
3. Open **Actions → Roll back GitHub Pages → Run workflow**.
4. Enter the historical run ID and start the workflow.
5. Confirm the rollback run succeeds and smoke-test the published Pages URL.

CLI equivalent:

```bash
gh workflow run rollback.yml \
  --repo s9cspawn/cicd-optimisation-demo \
  --ref main \
  -f source_run_id=<successful-run-id>
```

Rollback is available while the selected versioned artifact is retained. If it has expired, revert to the required commit and run the full CI/CD workflow.

