# Contributing to Verdict

Issues and pull requests are welcome. Verdict is a small research preview, so keep changes scoped, measurable and reproducible.

## Tests

CI runs on every push and pull request against `main`:

```bash
python -m pip install -e '.[dev]'
pytest -q
```

The same workflow runs one CLI smoke check:

```bash
python -m verdict_tiny --command 'pytest' --exit-code 0 < /dev/null
```

## Build and run

Verdict is a pure standard-library package with no runtime dependencies. Install it from a checkout:

```bash
python -m pip install .
```

For development, install it in editable mode with the test extra:

```bash
python -m pip install -e '.[dev]'
```

Run the CLI:

```bash
printf 'collected 0 items\nno tests ran\n' | verdict --command 'pytest tests/' --exit-code 0
```

The research page under `site/` is a separate Vite application:

```bash
cd site
npm ci
npm run build
```

## Reproduce the model and the benchmark numbers

```bash
python -m pip install -e '.[train,dev]'
python training/train.py
pytest -q
```

`training/train.py` regenerates the synthetic corpus, trains from scratch, exports the int8 weights, evaluates the quantized artifact and writes the metrics in `bench/results.json`. When the model changes, keep the corpus, the exported weights, the results and the README consistent with each other.

## Propose a change

- Open an issue first when the behaviour or the measurement method is in question; open a pull request against `main` when it is not.
- Keep a pull request focused on one change and keep unrelated formatting out of it.
- Add or update tests for every behavioural change.
- Do not add vendor links or endorsements to the documentation.
- Do not commit secrets, API keys or credentials. Use environment variables and local fixtures instead; local inference makes no network calls.

## License

Code and model weights are licensed under Apache-2.0, see `LICENSE`. The synthetic dataset under `data/` is dedicated to the public domain under CC0-1.0, see `data/LICENSE`. Contributions are accepted under the same terms, and there is no separate contributor license agreement.

## Security

Verdict is an advisory classifier. It is not a sandbox, an authorization mechanism or a security boundary, so a single prediction must never be the only gate for a consequential action.

Report vulnerabilities privately through GitHub Security Advisories (Security -> Report a vulnerability) rather than in a public issue. If the advisory form is unavailable for this repository, use the private contact channel described in `SECURITY.md`. Never paste secrets or sensitive logs into a public issue.
