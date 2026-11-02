import './style.css';
import { VerdictModel } from './verdict.js';

const messages = {
  en: {
    kicker: 'Tiny model · Apache-2.0',
    tagline: '<b>Exit code 0 ≠ success.</b> 197 KB · local · open source.',
    copy: 'Copy', copied: 'Copied', loading: 'Loading model…', ready: 'model ready · local', load_error: 'model failed to load',
    verdict: 'VERDICT · LOCAL', bench_title: 'Measured, reproducible ↗', bench_note: '192 synthetic held-out · 48 unseen families',
    baseline: 'Exit code', labels: 'outcomes', dependencies: 'dependencies', cite: 'Cite this work — BibTeX', weights: 'Weights',
    title: 'Verdict — local CLI outcome model',
  },
  ru: {
    kicker: 'Маленькая модель · Apache-2.0',
    tagline: '<b>Exit code 0 ≠ успех.</b> 197 КБ · локально · open source.',
    copy: 'Copy', copied: 'Copied', loading: 'Загрузка модели…', ready: 'модель готова · локально', load_error: 'ошибка загрузки модели',
    verdict: 'ВЕРДИКТ · ЛОКАЛЬНО', bench_title: 'Измерено, воспроизводимо ↗', bench_note: '192 synthetic held-out · 48 новых семейств',
    baseline: 'Exit code', labels: 'исхода', dependencies: 'зависимостей', cite: 'Цитирование — BibTeX', weights: 'Веса',
    title: 'Verdict — локальная модель результатов CLI',
  },
  zh: {
    kicker: '微型模型 · Apache-2.0',
    tagline: '<b>退出码 0 ≠ 成功。</b>197 KB · 本地 · 开源。',
    copy: 'Copy', copied: 'Copied', loading: '正在加载模型…', ready: '模型就绪 · 本地', load_error: '模型加载失败',
    verdict: '判定 · 本地', bench_title: '可测量，可复现 ↗', bench_note: '192 个合成留出样本 · 48 个未见类别',
    baseline: '退出码', labels: '种结果', dependencies: '个依赖', cite: '引用此工作 — BibTeX', weights: '权重',
    title: 'Verdict — 本地 CLI 结果模型',
  },
  es: {
    kicker: 'Modelo diminuto · Apache-2.0',
    tagline: '<b>Exit code 0 ≠ éxito.</b> 197 KB · local · open source.',
    copy: 'Copy', copied: 'Copied', loading: 'Cargando modelo…', ready: 'modelo listo · local', load_error: 'error al cargar el modelo',
    verdict: 'VEREDICTO · LOCAL', bench_title: 'Medido, reproducible ↗', bench_note: '192 sintéticos held-out · 48 familias nuevas',
    baseline: 'Exit code', labels: 'resultados', dependencies: 'dependencias', cite: 'Citar este trabajo — BibTeX', weights: 'Pesos',
    title: 'Verdict — modelo local de resultados CLI',
  },
};

const storage = {
  get(key) { try { return localStorage.getItem(key); } catch { return null; } },
  set(key, value) { try { localStorage.setItem(key, value); } catch {} },
};
const $ = selector => document.querySelector(selector);
const $$ = selector => [...document.querySelectorAll(selector)];
let language = 'en';
let model = null;

function applyTheme(theme) {
  const next = theme === 'dark' ? 'dark' : 'light';
  document.documentElement.dataset.theme = next;
  $('meta[name="theme-color"]').content = next === 'dark' ? '#0e0f11' : '#fafaf8';
  $('#theme-toggle').setAttribute('aria-pressed', String(next === 'dark'));
  storage.set('verdict-theme', next);
}
applyTheme(storage.get('verdict-theme') === 'dark' ? 'dark' : 'light');
$('#theme-toggle').addEventListener('click', () => {
  applyTheme(document.documentElement.dataset.theme === 'dark' ? 'light' : 'dark');
});

function setLanguage(next) {
  language = messages[next] ? next : 'en';
  document.documentElement.lang = language;
  document.title = messages[language].title;
  $$('[data-i18n]').forEach(node => {
    const value = messages[language][node.dataset.i18n];
    if (value) node.textContent = value;
  });
  $$('[data-i18n-html]').forEach(node => {
    const value = messages[language][node.dataset.i18nHtml];
    if (value) node.innerHTML = value;
  });
  $('#language').value = language;
  if (model) $('#model-status').textContent = messages[language].ready;
  storage.set('verdict-language', language);
  const url = new URL(location.href);
  url.searchParams.set('lang', language);
  history.replaceState(null, '', url);
}
const requested = new URLSearchParams(location.search).get('lang');
const savedLanguage = storage.get('verdict-language');
const detected = (navigator.languages || [navigator.language || 'en'])
  .map(value => value.toLowerCase().split('-')[0]).find(value => messages[value]);
setLanguage(requested || savedLanguage || detected || 'en');
$('#language').addEventListener('change', event => setLanguage(event.target.value));

function legacyCopy(text) {
  const area = document.createElement('textarea');
  area.value = text;
  area.style.cssText = 'position:fixed;opacity:0;pointer-events:none';
  document.body.appendChild(area);
  area.select();
  try { document.execCommand('copy'); } catch {}
  area.remove();
}
async function copyText(text, button) {
  try {
    if (navigator.clipboard?.writeText) await navigator.clipboard.writeText(text);
    else legacyCopy(text);
  } catch { legacyCopy(text); }
  button.textContent = messages[language].copied;
  button.classList.add('copied');
  setTimeout(() => {
    button.textContent = messages[language].copy;
    button.classList.remove('copied');
  }, 1400);
}
$$('[data-copy-target]').forEach(button => button.addEventListener('click', () => {
  const target = document.getElementById(button.dataset.copyTarget);
  if (target) copyText(target.textContent, button);
}));

async function loadGithubStats() {
  const controller = new AbortController();
  const timeout = setTimeout(() => controller.abort(), 6000);
  try {
    const response = await fetch('https://api.github.com/repos/Balanov/verdict', { signal: controller.signal });
    if (!response.ok) return;
    const data = await response.json();
    if (Number.isFinite(data.stargazers_count)) $('#gh-stars').textContent = data.stargazers_count.toLocaleString('en-US');
    if (Number.isFinite(data.forks_count)) $('#gh-forks').textContent = data.forks_count.toLocaleString('en-US');
  } catch {
    // Static counters remain usable when the API is unavailable or rate-limited.
  } finally { clearTimeout(timeout); }
}
loadGithubStats();

const presets = [
  { command: 'mvn test', code: 0, stdout: '[INFO] Tests run: 8, Failures: 0, Errors: 0\n[INFO] BUILD SUCCESS', stderr: '' },
  { command: 'npm test', code: 1, stdout: 'FAIL src/payments.test.js\nTests: 2 failed, 4 passed, 6 total', stderr: '' },
  { command: 'kubectl get pods', code: 1, stdout: '', stderr: 'Error from server (Forbidden): permission denied' },
  { command: 'pytest tests/', code: 0, stdout: 'collected 0 items\nno tests ran in 0.01s', stderr: '' },
];
const reducedMotion = window.matchMedia?.('(prefers-reduced-motion: reduce)').matches;
const wait = ms => new Promise(resolve => setTimeout(resolve, ms));
let runId = 0;
let autoplay = !reducedMotion;

function showResult(result, elapsed) {
  const label = $('#result-label');
  label.textContent = result.label;
  label.dataset.label = result.label;
  $('#result-confidence').textContent = `${(result.confidence * 100).toFixed(1)}%`;
  $('#result-latency').textContent = `${elapsed.toFixed(2)} ms · browser`;
  $('#probabilities').innerHTML = Object.entries(result.probabilities).map(([name, value]) => `
    <div class="prob-row"><span>${name}</span><div class="prob-track"><i style="width:${Math.max(.5, value * 100)}%"></i></div><b>${(value * 100).toFixed(1)}</b></div>`).join('');
  $('#json-result').textContent = JSON.stringify({ label: result.label, confidence: Number(result.confidence.toFixed(6)), advisory: true });
}

async function playScenario(index, animate = true) {
  if (!model) return;
  const id = ++runId;
  const preset = presets[index];
  $$('[data-preset]').forEach(button => button.setAttribute('aria-pressed', String(Number(button.dataset.preset) === index)));
  const label = $('#result-label');
  label.textContent = '···';
  delete label.dataset.label;
  $('#result-confidence').textContent = '—';
  $('#result-latency').textContent = 'browser';
  $('#probabilities').innerHTML = '';
  $('#json-result').textContent = '{ … }';
  $('#term-exit').textContent = `exit ${preset.code}`;
  const output = [preset.stdout, preset.stderr].filter(Boolean).join('\n');

  if (animate) {
    $('#term-command').textContent = '';
    $('#term-output').textContent = '';
    for (let char = 1; char <= preset.command.length; char++) {
      if (id !== runId) return;
      $('#term-command').textContent = preset.command.slice(0, char);
      await wait(18 + Math.random() * 18);
    }
    const lines = output.split('\n');
    for (let line = 1; line <= lines.length; line++) {
      await wait(220);
      if (id !== runId) return;
      $('#term-output').textContent = lines.slice(0, line).join('\n');
    }
    await wait(180);
  } else {
    $('#term-command').textContent = preset.command;
    $('#term-output').textContent = output;
  }
  if (id !== runId) return;
  const started = performance.now();
  const result = model.predict(preset.command, preset.code, preset.stdout, preset.stderr);
  const elapsed = performance.now() - started;
  showResult(result, elapsed);
}

$$('[data-preset]').forEach(button => button.addEventListener('click', () => {
  autoplay = false;
  playScenario(Number(button.dataset.preset), !reducedMotion);
}));

async function autoplayDemos() {
  if (reducedMotion) {
    await playScenario(0, false);
    return;
  }
  let index = 0;
  while (autoplay) {
    await playScenario(index, true);
    if (!autoplay) break;
    await wait(4200);
    if (!autoplay) break;
    index = (index + 1) % presets.length;
  }
}

const fills = $$('.bar-fill');
function fillBars() { fills.forEach(fill => { fill.style.width = `${fill.dataset.w}%`; }); }
if (reducedMotion || !('IntersectionObserver' in window)) fillBars();
else {
  const observer = new IntersectionObserver(entries => {
    if (entries[0].isIntersecting) { fillBars(); observer.disconnect(); }
  }, { threshold: .2 });
  observer.observe($('#bench'));
}

try {
  model = await VerdictModel.load(new URL('./verdict-q8.bin', document.baseURI));
  $('#model-status').textContent = messages[language].ready;
  $$('[data-preset]').forEach(button => { button.disabled = false; });
  autoplayDemos();
} catch (error) {
  $('#model-status').textContent = messages[language].load_error;
  $('#result-label').textContent = 'error';
  console.error(error);
}
