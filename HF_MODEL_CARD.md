---
license: apache-2.0
language: en
library_name: verdict-tiny
tags:
  - text-classification
  - ai-agents
  - tool-use
  - cli
  - quantized
  - tiny-model
---

# Verdict 0.1

**Exit code 0 is not proof.** Verdict is a 197 KB int8 classifier for the semantic outcome of CLI tool calls. Given a command, exit code, stdout, and stderr, it returns `success`, `failure`, `blocked`, or `unknown` with class probabilities.

This is a **research preview**, not an authoritative task-completion verifier.

## Intended use

Advisory outcome classification inside coding-agent harnesses, CI observability, and tool-output analysis. Keep exit codes, deterministic validators, and authoritative environment-state checks in place. Do not use Verdict alone to authorize destructive actions or declare critical work complete.

## Out-of-scope use

- General task-completion or code-correctness judgments
- Safety or security policy enforcement
- Non-CLI documents and general natural-language classification
- Unsupervised production deployment without domain evaluation

## Metrics

The test set contains 192 synthetic examples from 48 CLI template families that are entirely absent from training.

| Metric | Verdict int8 | Exit-code baseline |
|---|---:|---:|
| Accuracy | 93.2% | 47.9% |
| Macro-F1 | 93.2% | 31.9% |
| Artifact size | 197 KB | — |
| Median latency | 0.54 ms | — |

Latency was measured over 576 predictions on Windows 11 / AMD64 / Python 3.12. Full details and the confusion matrix are in `bench/results.json` in the code repository.

## Data and limitations

Training contains 1,440 programmatically generated records from 60 template families. The test corpus uses 48 separate template families. Both splits are public and CC0. No production logs or proprietary data were used.

The model is English-biased, may inherit template artifacts, and has not been validated on a representative production trace corpus. Confidence values are uncalibrated. Synthetic-held-out performance must not be interpreted as production reliability.

## Architecture

Hashed character 3–5-grams and word 1–3-grams feed a multinomial logistic regression classifier. The release contains 196,608 signed int8 weights, four biases, and per-class quantization scales. Input streams use explicit head/tail clipping at 12,288 characters each.

## Run locally

The inference package has no runtime dependencies. Get the code and this artifact from the linked GitHub repository:

```bash
git clone https://github.com/Balanov/verdict.git
cd verdict
python -m pip install .
```

```python
from verdict_tiny import Verdict

model = Verdict()
print(model.predict(
    command="mvn test",
    exit_code=0,
    stdout="[INFO] Tests run: 8, Failures: 0\n[INFO] BUILD SUCCESS",
))
```

## Files

- `verdict-q8.bin`: quantized model artifact
- `config.json`: architecture, labels, scales and biases
- `LICENSE`: Apache-2.0 for weights

## Links

- Code, data and benchmarks: https://github.com/Balanov/verdict
- Research page and local browser demo: https://balanov.pro/research/verdict/

## Citation

```bibtex
@misc{balanov2026verdict,
  title  = {Verdict: Tiny Semantic Outcome Verification for AI Agents},
  author = {Balanov, Anton},
  year   = {2026},
  url    = {https://balanov.pro/research/verdict/}
}
```
