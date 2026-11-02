#!/usr/bin/env python3
"""Train, quantize and evaluate Verdict on held-out CLI families."""
from __future__ import annotations

import json
import platform
import random
import statistics
import sys
import time
from collections import Counter
from pathlib import Path

import numpy as np
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix, f1_score

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(ROOT / "src"))

from training.data import LABELS, build  # noqa: E402
from training.features import format_input, sparse_matrix  # noqa: E402
from verdict_tiny.model import Verdict  # noqa: E402


def dump_jsonl(path: Path, records: list[dict]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("".join(json.dumps(r, ensure_ascii=False) + "\n" for r in records), encoding="utf-8")


def quantize(coef: np.ndarray) -> tuple[np.ndarray, list[float]]:
    scales = (np.max(np.abs(coef), axis=1) / 127.0).astype(np.float64)
    scales[scales == 0] = 1.0
    quantized = np.clip(np.rint(coef / scales[:, None]), -127, 127).astype(np.int8)
    return quantized, scales.tolist()


def main() -> None:
    random.seed(42)
    np.random.seed(42)
    train, test = build("train"), build("test")
    dump_jsonl(ROOT / "data" / "train.jsonl", train)
    dump_jsonl(ROOT / "data" / "test.jsonl", test)
    x_train = sparse_matrix([format_input(r["command"], r["exit_code"], r["stdout"], r["stderr"]) for r in train])
    y_train = np.array([LABELS.index(r["label"]) for r in train])
    classifier = LogisticRegression(
        C=2.0, max_iter=500, class_weight="balanced",
        solver="lbfgs", random_state=42,
    ).fit(x_train, y_train)
    assert list(classifier.classes_) == list(range(len(LABELS)))

    quantized, scales = quantize(classifier.coef_.astype(np.float64))
    header = {
        "format": "verdict-q8-v1", "version": "0.1.0", "labels": list(LABELS),
        "n_features": int(classifier.coef_.shape[1]), "n_char": 1 << 15,
        "n_word": 1 << 14, "scales": scales, "bias": classifier.intercept_.tolist(),
        "quantization": "signed-int8-per-class", "feature_hash": "fnv1a32-char3-5-word1-3-number-normalized-semantic-counts-v1",
        "input_limit_chars": 12288, "training_records": len(train),
        "evaluation": "held-out-template-families",
    }
    payload = json.dumps(header, separators=(",", ":"), ensure_ascii=False).encode("utf-8")
    artifact = b"VRD1" + len(payload).to_bytes(4, "little") + payload + quantized.tobytes()
    weights = ROOT / "weights"
    weights.mkdir(exist_ok=True)
    (weights / "verdict-q8.bin").write_bytes(artifact)
    (weights / "config.json").write_text(json.dumps(header, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    package_weights = ROOT / "src" / "verdict_tiny" / "weights"
    package_weights.mkdir(exist_ok=True)
    (package_weights / "verdict-q8.bin").write_bytes(artifact)

    model = Verdict(weights / "verdict-q8.bin")
    predictions, latencies = [], []
    for _ in range(3):
        for record in test:
            started = time.perf_counter_ns()
            result = model.predict(record["command"], record["exit_code"], record["stdout"], record["stderr"])
            latencies.append((time.perf_counter_ns() - started) / 1e6)
            if _ == 0:
                predictions.append(result["label"])
    truth = [r["label"] for r in test]
    baseline = ["success" if r["exit_code"] == 0 else "failure" for r in test]
    metrics = {
        "version": "0.1.0",
        "train_records": len(train), "test_records": len(test),
        "train_families": len({r["family"] for r in train}), "test_families": len({r["family"] for r in test}),
        "class_distribution_test": dict(Counter(truth)),
        "accuracy": accuracy_score(truth, predictions),
        "macro_f1": f1_score(truth, predictions, labels=list(LABELS), average="macro", zero_division=0),
        "exit_code_baseline_accuracy": accuracy_score(truth, baseline),
        "exit_code_baseline_macro_f1": f1_score(truth, baseline, labels=list(LABELS), average="macro", zero_division=0),
        "per_class": classification_report(truth, predictions, labels=list(LABELS), output_dict=True, zero_division=0),
        "confusion_matrix": confusion_matrix(truth, predictions, labels=list(LABELS)).tolist(),
        "artifact_bytes": len(artifact),
        "latency_ms_median": statistics.median(latencies),
        "latency_ms_p95": float(np.percentile(latencies, 95)),
        "latency_samples": len(latencies),
        "environment": {"python": platform.python_version(), "platform": platform.platform(), "machine": platform.machine()},
        "limitations": ["Synthetic templates only", "English-biased CLI output", "Advisory signal, not authoritative state verification"],
    }
    (ROOT / "bench").mkdir(exist_ok=True)
    (ROOT / "bench" / "results.json").write_text(json.dumps(metrics, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(json.dumps(metrics, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
