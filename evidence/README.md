# Benchmark evidence

The evidence files are derived from GitHub's workflow, job, and step timestamps. Each row links back to the immutable Actions run used in the sample.

## Baseline definition

- Commit: [`95f5222`](https://github.com/s9cspawn/cicd-optimisation-demo/commit/95f52226fa664d289b9209a589a36f302d1d564f)
- Five sequential `workflow_dispatch` runs on the same commit and GitHub-hosted runner label
- No dependency caching
- Build, test, dependency audit, and CodeQL scan execute sequentially
- Deployment performs a second checkout, dependency installation, and production build

Stage values sum the named GitHub Actions steps. Because GitHub timestamps have one-second resolution, subsecond steps can appear as zero seconds. Total duration uses the workflow-level `startedAt` and `updatedAt` timestamps and therefore includes orchestration between jobs.

The baseline mean was **108 seconds**, nearest-rank p95 was **117 seconds**, and all five runs succeeded (**0% failure rate**).

## Optimised definition

- Merge commit: [`d8fb8e4`](https://github.com/s9cspawn/cicd-optimisation-demo/commit/d8fb8e48060eee3e7cf38c6abadd162b5cecb219)
- Pull request: [#1](https://github.com/s9cspawn/cicd-optimisation-demo/pull/1)
- Five sequential warm-cache `workflow_dispatch` runs on the same commit and runner label
- Lint/tests, CodeQL/dependency scans, and the production build run in parallel
- The production build is retained for 30 days and reused by deployment and rollback

The automatic post-merge run was treated as a separate warm-up observation and excluded from the five-run comparison. The optimised mean was **93.6 seconds**, nearest-rank p95 was **99 seconds**, and all five runs succeeded (**0% failure rate**).

The verified artifact-only rollback completed in **17 seconds**, an **84.3%** reduction compared with the baseline full-pipeline recovery-time proxy of 108 seconds.

