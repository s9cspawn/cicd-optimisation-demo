# CI/CD Benchmark & Optimisation Report

**Pipeline:** GitHub Actions to GitHub Pages  
**Application:** Pipeline Observatory (Vite website)  
**Repository:** https://github.com/s9cspawn/cicd-optimisation-demo  
**Measurement date:** 30 September 2026

## Objective and method

The experiment measured one real build-test-scan-deploy pipeline before and after optimisation. Both samples used five sequential manual runs on the same GitHub-hosted `ubuntu-latest` label and the same application/lockfile. Total duration is the GitHub workflow `startedAt` to `updatedAt` interval; stage values use job/step timestamps. p95 uses the nearest-rank method. GitHub timestamps have one-second resolution.

The baseline commit [`95f5222`](https://github.com/s9cspawn/cicd-optimisation-demo/commit/95f52226fa664d289b9209a589a36f302d1d564f) ran build, lint/tests, dependency audit and CodeQL sequentially. Deployment then repeated checkout, `npm ci`, and the production build. The optimisation was reviewed in [PR #1](https://github.com/s9cspawn/cicd-optimisation-demo/pull/1) and merged as [`d8fb8e4`](https://github.com/s9cspawn/cicd-optimisation-demo/commit/d8fb8e48060eee3e7cf38c6abadd162b5cecb219).

## Changes implemented

1. **Dependency caching:** `setup-node` restores npm's cache using `package-lock.json`.
2. **Parallel jobs:** lint/tests, dependency/CodeQL scans, and the production build execute concurrently; deployment waits for all three gates.
3. **Build once and reuse:** the tested `dist/` output is uploaded once, deployed without rebuilding, and retained for 30 days as a versioned rollback artifact.

## Measured results

| Metric | Baseline | Optimised | Change |
|---|---:|---:|---:|
| Average total duration | 108.0 s | 93.6 s | **-14.4 s (-13.3%)** |
| p95 total duration | 117 s | 99 s | **-18 s (-15.4%)** |
| Build steps | 1.4 s / 2 builds | 1.2 s / 1 build | **1 build removed** |
| Test steps | 1.2 s | 1.2 s | 0% |
| Scan steps | 68.6 s | 65.4 s | **-4.7%** |
| Deployment job | 19.0 s | 9.4 s | **-50.5%** |
| Failure rate | 0/5 (0%) | 0/5 (0%) | No regression |

Total duration improved because independent gates overlap and deployment no longer repeats installation/build work. CodeQL remained the critical path, so the overall reduction is smaller than the 50.5% deployment-stage improvement. The automatic post-merge run (111 s) warmed the cache and is disclosed but excluded from the matched five-run sample. Aggregated install time did not fall because three parallel jobs each run `npm ci`; at this small project size, runner setup variance dominates, while caching principally avoids repeated registry downloads.

## Failure and rollback outcome

All ten measured runs succeeded, so failure rate remained 0%; an improvement could not be demonstrated without manufacturing failures. A feature-branch deployment was correctly rejected by the protected `github-pages` environment and excluded from the samples.

Baseline rollback required reverting/rerunning a historical commit through the full pipeline (108 s average proxy) and could rebuild against changed external dependencies. The new [`rollback.yml`](https://github.com/s9cspawn/cicd-optimisation-demo/blob/main/.github/workflows/rollback.yml) redeploys the retained immutable artifact. [Rollback run 36704893909](https://github.com/s9cspawn/cicd-optimisation-demo/actions/runs/36704893909) succeeded in **17 s**, an **84.3% recovery-time reduction**, followed by a successful live-site smoke test.

## Evidence

- Baseline exports: [`baseline-runs.csv`](../evidence/baseline-runs.csv) and [`baseline-runs.json`](../evidence/baseline-runs.json)
- Optimised exports: [`optimised-runs.csv`](../evidence/optimised-runs.csv) and [`optimised-runs.json`](../evidence/optimised-runs.json)
- Rollback export: [`rollback-run.json`](../evidence/rollback-run.json)
- Live deployment: https://s9cspawn.github.io/cicd-optimisation-demo/

**Conclusion:** the optimised workflow achieved a repeatable 13.3% mean and 15.4% p95 delivery-time reduction without reducing quality/security gates or reliability. Artifact-based rollback produced the largest operational gain.

