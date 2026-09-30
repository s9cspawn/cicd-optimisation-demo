# CI/CD Optimisation Demo

A small production-style website used to benchmark a real GitHub Actions pipeline before and after measurable optimisation.

## Experiment

The experiment uses the same website and GitHub-hosted runner class for two five-run samples.

1. **Baseline:** sequential build, test, dependency audit and CodeQL scan; deployment performs a second clean install and build.
2. **Optimised:** dependency caching, parallel quality/security/build jobs, and build-artifact reuse for deployment.
3. **Measure:** export workflow, job, and step timestamps; compare mean, p95, stage duration, and failure rate.

No artificial delay is added to either workflow.

## Local checks

```bash
npm ci
npm run lint
npm run test:coverage
npm run audit
npm run build
```

## Deployment

The default branch deploys `dist/` to GitHub Pages through `.github/workflows/pages.yml`.

