import { defineConfig } from 'vite';

export default defineConfig({
  base: '/cicd-optimisation-demo/',
  test: {
    coverage: {
      provider: 'v8',
      reporter: ['text', 'json-summary'],
      include: ['src/pipeline-metrics.js'],
      thresholds: {
        lines: 90,
        functions: 90,
        statements: 90,
        branches: 85,
      },
    },
  },
});
