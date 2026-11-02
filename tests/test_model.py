import json
from pathlib import Path

import pytest

from verdict_tiny.model import Verdict

ROOT = Path(__file__).resolve().parents[1]


@pytest.fixture(scope="module")
def model():
    return Verdict(ROOT / "weights" / "verdict-q8.bin")


def test_artifact_contract(model):
    assert model.labels == ("success", "failure", "blocked", "unknown")
    assert model.n_features == 49152
    assert len(model.coef) == 4 * model.n_features


def test_prediction_contract(model):
    result = model.predict("pytest", 0, "12 passed in 0.4s")
    assert result["label"] in model.labels
    assert result["advisory"] is True
    assert sum(result["probabilities"].values()) == pytest.approx(1, abs=2e-5)


def test_long_input_is_bounded(model):
    result = model.predict("pytest", 0, "noise\n" * 20000 + "8 passed")
    assert result["label"] in model.labels


def test_corrupt_artifact_is_rejected(tmp_path):
    path = tmp_path / "bad.bin"
    path.write_bytes(b"not-a-model")
    with pytest.raises(ValueError):
        Verdict(path)


def test_fixture_predictions(model):
    fixtures = [
        ("mvn test", 0, "[INFO] BUILD SUCCESS\nTests run: 8, Failures: 0", "", "success"),
        ("pytest", 0, "no tests ran\ncollected 0 items", "", "unknown"),
        ("kubectl get pods", 1, "", "Error from server (Forbidden): permission denied", "blocked"),
        ("npm test", 1, "Tests: 2 failed, 4 passed", "", "failure"),
    ]
    for command, code, stdout, stderr, expected in fixtures:
        assert model.predict(command, code, stdout, stderr)["label"] == expected
