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

