"""Zero-dependency inference for the quantized Verdict model."""
from __future__ import annotations

import json
import math
import re
from array import array
from pathlib import Path

TOKEN_RE = re.compile(r"\w+|[^\w\s]", re.UNICODE)
NUMBER_RE = re.compile(r"(?<![\w])\d+(?:[.,]\d+)*(?![\w])")
DEFAULT_WEIGHTS = Path(__file__).resolve().parent / "weights" / "verdict-q8.bin"


def _fnv1a(value: str) -> int:
    result = 2166136261
    for byte in value.encode("utf-8"):
        result ^= byte
        result = (result * 16777619) & 0xFFFFFFFF
    return result


DIRECT_COUNT_RE = re.compile(r"\b(tests?|failures?|errors?|passed|skipped|examples?)(?:\s+run)?\s*[:=]\s*(\d+)", re.IGNORECASE)
LEADING_COUNT_RE = re.compile(r"\b(\d+)\s+(tests?|failures?|errors?|passed|skipped|examples?)\b", re.IGNORECASE)


def semantic_signals(text: str) -> str:
    signals = []
    for pattern, value_group, name_group in ((DIRECT_COUNT_RE, 2, 1), (LEADING_COUNT_RE, 1, 2)):
        for match in pattern.finditer(text):
            value = "ZERO" if int(match.group(value_group)) == 0 else "POS"
            signals.append(f"SIG_{match.group(name_group).upper()}_{value}")
    return " ".join(signals)


class Verdict:
    def __init__(self, weights: str | Path | None = None):
        self.weights_path = Path(weights) if weights else DEFAULT_WEIGHTS
        raw = self.weights_path.read_bytes()
        if len(raw) < 8 or raw[:4] != b"VRD1":
            raise ValueError("Not a Verdict VRD1 artifact")
        header_size = int.from_bytes(raw[4:8], "little")
        self.config = json.loads(raw[8:8 + header_size])
        if self.config.get("format") != "verdict-q8-v1":
            raise ValueError("Unsupported Verdict artifact")
        self.labels = tuple(self.config["labels"])
        self.n_features = int(self.config["n_features"])
        self.n_char = int(self.config["n_char"])
        self.n_word = int(self.config["n_word"])
        self.scales = self.config["scales"]
        self.bias = self.config["bias"]
        expected = len(self.labels) * self.n_features
        body = raw[8 + header_size:]
        if len(body) != expected:
            raise ValueError(f"Corrupt Verdict artifact: expected {expected} weight bytes, got {len(body)}")
        self.coef = array("b")
        self.coef.frombytes(body)

    def _features(self, text: str) -> list[int]:
        features: set[int] = set()
        normalized = NUMBER_RE.sub(lambda match: " ZERO " if not any(digit in "123456789" for digit in match.group()) else " NUM ", text.lower())
        normalized += " " + semantic_signals(text)
        tokens = TOKEN_RE.findall(normalized)
        for size in (1, 2, 3):
            for start in range(len(tokens) - size + 1):
                gram = " ".join(tokens[start:start + size])
                features.add(self.n_char + (_fnv1a(f"w{size}:" + gram) % self.n_word))
        for token in tokens:
            padded = f" {token} "
            for size in (3, 4, 5):
                for start in range(max(0, len(padded) - size + 1)):
                    features.add(_fnv1a("c:" + padded[start:start + size]) % self.n_char)
        return sorted(features)

    def _format(self, command: str, exit_code: int, stdout: str, stderr: str) -> str:
        limit = int(self.config["input_limit_chars"])

        def clip(value: str) -> str:
            value = (value or "").replace("\r\n", "\n").replace("\r", "\n")
            if len(value) <= limit:
                return value
            return value[:2048] + "\n[VERDICT: middle omitted]\n" + value[-(limit - 2048):]

        code_token = "EXIT_ZERO" if int(exit_code) == 0 else "EXIT_NONZERO"
        return f"CMD {command or ''}\n{code_token} EXIT_CODE_{int(exit_code)}\nOUT {clip(stdout)}\nERR {clip(stderr)}"

    def predict(self, command: str, exit_code: int, stdout: str = "", stderr: str = "") -> dict:
        features = self._features(self._format(command, exit_code, stdout, stderr))
        scores = []
        for class_index in range(len(self.labels)):
            offset = class_index * self.n_features
            total = self.bias[class_index]
            scale = self.scales[class_index]
            for feature in features:
                total += self.coef[offset + feature] * scale
            scores.append(total)
        maximum = max(scores)
        exps = [math.exp(score - maximum) for score in scores]
        denominator = sum(exps)
        probabilities = [value / denominator for value in exps]
        best = max(range(len(scores)), key=scores.__getitem__)
        return {
            "label": self.labels[best],
            "confidence": round(probabilities[best], 6),
            "probabilities": {label: round(probabilities[i], 6) for i, label in enumerate(self.labels)},
            "advisory": True,
        }
