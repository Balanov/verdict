const TOKEN_RE = /[\p{L}\p{N}_]+|[^\s\p{L}\p{N}_]/gu;
const NUMBER_RE = /(?<![\p{L}\p{N}_])\d+(?:[.,]\d+)*(?![\p{L}\p{N}_])/gu;
const DIRECT_COUNT_RE = /\b(tests?|failures?|errors?|passed|skipped|examples?)(?:\s+run)?\s*[:=]\s*(\d+)/giu;
const LEADING_COUNT_RE = /\b(\d+)\s+(tests?|failures?|errors?|passed|skipped|examples?)\b/giu;
const encoder = new TextEncoder();

function fnv1a(value) {
  let hash = 2166136261;
  for (const byte of encoder.encode(value)) hash = Math.imul(hash ^ byte, 16777619) >>> 0;
  return hash;
}

function semanticSignals(text) {
  const signals = [];
  for (const [pattern, valueGroup, nameGroup] of [[DIRECT_COUNT_RE, 2, 1], [LEADING_COUNT_RE, 1, 2]]) {
    pattern.lastIndex = 0;
    for (let match = pattern.exec(text); match; match = pattern.exec(text)) {
      signals.push(`SIG_${match[nameGroup].toUpperCase()}_${Number(match[valueGroup]) === 0 ? 'ZERO' : 'POS'}`);
    }
  }
  return signals.join(' ');
}

export class VerdictModel {
  static async load(url) {
    const response = await fetch(url);
    if (!response.ok) throw new Error(`Weights: HTTP ${response.status}`);
    const raw = await response.arrayBuffer();
    const view = new DataView(raw);
    const magic = new TextDecoder().decode(raw.slice(0, 4));
    if (magic !== 'VRD1') throw new Error('Invalid Verdict artifact');
    const headerSize = view.getUint32(4, true);
    const config = JSON.parse(new TextDecoder().decode(raw.slice(8, 8 + headerSize)));
    if (config.format !== 'verdict-q8-v1') throw new Error('Unsupported Verdict artifact');
    const coef = new Int8Array(raw, 8 + headerSize);
    if (coef.length !== config.labels.length * config.n_features) throw new Error('Corrupt Verdict artifact');
    return new VerdictModel(config, coef);
  }

  constructor(config, coef) { this.config = config; this.coef = coef; }

  features(text) {
    const normalized = text.toLowerCase().replace(NUMBER_RE, match => /[1-9]/.test(match) ? ' NUM ' : ' ZERO ') + ' ' + semanticSignals(text);
    const tokens = normalized.match(TOKEN_RE) || [];
    const features = new Set();
    for (let size = 1; size <= 3; size++) {
      for (let start = 0; start <= tokens.length - size; start++) {
        features.add(this.config.n_char + fnv1a(`w${size}:` + tokens.slice(start, start + size).join(' ')) % this.config.n_word);
      }
    }
    for (const token of tokens) {
      const padded = ` ${token} `;
      for (let size = 3; size <= 5; size++) {
        for (let start = 0; start <= padded.length - size; start++) {
          features.add(fnv1a('c:' + padded.slice(start, start + size)) % this.config.n_char);
        }
      }
    }
    return features;
  }

  format(command, exitCode, stdout, stderr) {
    const limit = this.config.input_limit_chars;
    const clip = input => {
      const value = (input || '').replace(/\r\n/g, '\n').replace(/\r/g, '\n');
      return value.length <= limit ? value : value.slice(0, 2048) + '\n[VERDICT: middle omitted]\n' + value.slice(-(limit - 2048));
    };
    const code = Number(exitCode);
    return `CMD ${command || ''}\n${code === 0 ? 'EXIT_ZERO' : 'EXIT_NONZERO'} EXIT_CODE_${code}\nOUT ${clip(stdout)}\nERR ${clip(stderr)}`;
  }

  predict(command, exitCode, stdout = '', stderr = '') {
    const features = this.features(this.format(command, exitCode, stdout, stderr));
    const scores = this.config.labels.map((_, classIndex) => {
      let total = this.config.bias[classIndex];
      const offset = classIndex * this.config.n_features;
      for (const feature of features) total += this.coef[offset + feature] * this.config.scales[classIndex];
      return total;
    });
    const maximum = Math.max(...scores);
    const exps = scores.map(score => Math.exp(score - maximum));
    const denominator = exps.reduce((a, b) => a + b, 0);
    const probabilities = exps.map(value => value / denominator);
    const best = scores.indexOf(maximum);
    return {
      label: this.config.labels[best],
      confidence: probabilities[best],
      probabilities: Object.fromEntries(this.config.labels.map((label, i) => [label, probabilities[i]])),
      advisory: true,
    };
  }
}
