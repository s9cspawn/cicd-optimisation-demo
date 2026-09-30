import './style.css';
import { formatDuration, percentageChange, statusLabel } from './pipeline-metrics.js';

const baseline = {
  durationSeconds: 0,
  failureRate: 0,
  runs: 0,
};

const optimised = {
  durationSeconds: 0,
  failureRate: 0,
  runs: 0,
};

document.querySelector('#app').innerHTML = `
  <header class="site-header">
    <a class="brand" href="#top" aria-label="Pipeline Observatory home">
      <span class="brand-mark" aria-hidden="true">PO</span>
      <span>Pipeline Observatory</span>
    </a>
    <nav aria-label="Primary navigation">
      <a href="#experiment">Experiment</a>
      <a href="#pipeline">Pipeline</a>
      <a href="#results">Results</a>
    </nav>
  </header>

  <main id="main">
    <section class="hero" id="top">
      <div class="hero-copy">
        <p class="eyebrow">DevSecOps measurement lab</p>
        <h1>Make delivery speed visible.</h1>
        <p class="hero-text">
          A real GitHub Actions pipeline, measured before and after caching,
          parallel execution, and build-artifact reuse.
        </p>
        <a class="button" href="#experiment">View the experiment</a>
      </div>
      <div class="terminal-card" aria-label="Pipeline stages illustration">
        <div class="terminal-top"><span></span><span></span><span></span></div>
        <ol>
          <li><span>01</span> Build</li>
          <li><span>02</span> Test</li>
          <li><span>03</span> Scan</li>
          <li><span>04</span> Deploy</li>
        </ol>
      </div>
    </section>

    <section class="section" id="experiment">
      <div class="section-heading">
        <p class="eyebrow">Benchmark design</p>
        <h2>Ten controlled pipeline runs</h2>
        <p>Five runs establish the baseline. Five more measure the optimised workflow.</p>
      </div>
      <div class="card-grid">
        <article class="metric-card">
          <p>Baseline runs</p>
          <strong>${baseline.runs}</strong>
          <span>${statusLabel(baseline.runs)}</span>
        </article>
        <article class="metric-card accent">
          <p>Optimised runs</p>
          <strong>${optimised.runs}</strong>
          <span>${statusLabel(optimised.runs)}</span>
        </article>
        <article class="metric-card">
          <p>Measured change</p>
          <strong>${percentageChange(baseline.durationSeconds, optimised.durationSeconds)}</strong>
          <span>Average total duration</span>
        </article>
      </div>
    </section>

    <section class="section pipeline-section" id="pipeline">
      <div class="section-heading">
        <p class="eyebrow">Delivery path</p>
        <h2>From commit to production</h2>
      </div>
      <div class="pipeline" role="list" aria-label="CI/CD pipeline stages">
        <article role="listitem"><span>01</span><h3>Build</h3><p>Compile the production site.</p></article>
        <article role="listitem"><span>02</span><h3>Test</h3><p>Lint and run automated tests.</p></article>
        <article role="listitem"><span>03</span><h3>Scan</h3><p>Audit dependencies and source.</p></article>
        <article role="listitem"><span>04</span><h3>Deploy</h3><p>Publish to GitHub Pages.</p></article>
      </div>
    </section>

    <section class="section results-section" id="results">
      <div class="section-heading">
        <p class="eyebrow">Live result placeholder</p>
        <h2>Evidence replaces assumptions</h2>
        <p>The cards update once the benchmark exports have been collected.</p>
      </div>
      <div class="comparison" aria-label="Benchmark comparison">
        <div><span>Baseline average</span><strong>${formatDuration(baseline.durationSeconds)}</strong></div>
        <div><span>Optimised average</span><strong>${formatDuration(optimised.durationSeconds)}</strong></div>
        <div><span>Baseline failures</span><strong>${baseline.failureRate}%</strong></div>
        <div><span>Optimised failures</span><strong>${optimised.failureRate}%</strong></div>
      </div>
    </section>
  </main>

  <footer>
    <p>Built as a reproducible CI/CD optimisation experiment.</p>
    <a href="https://github.com/s9cspawn/cicd-optimisation-demo">Source and evidence</a>
  </footer>
`;

