"""Deterministic feature hashing shared by training and inference."""
from __future__ import annotations

import re
from array import array
from collections import Counter

import numpy as np
from scipy.sparse import csr_matrix

N_CHAR = 1 << 15
N_WORD = 1 << 14
N_FEATURES = N_CHAR + N_WORD
TOKEN_RE = re.compile(r"\w+|[^\w\s]", re.UNICODE)
NUMBER_RE = re.compile(r"(?<![\w])\d+(?:[.,]\d+)*(?![\w])")


def normalize_numbers(text: str) -> str:
    return NUMBER_RE.sub(lambda match: " ZERO " if not any(digit in "123456789" for digit in match.group()) else " NUM ", text.lower())


def format_input(command: str, exit_code: int, stdout: str, stderr: str, limit: int = 12288) -> str:
    def clip(value: str) -> str:
        value = (value or "").replace("\r\n", "\n").replace("\r", "\n")
        if len(value) <= limit:
            return value
        return value[:2048] + "\n[VERDICT: middle omitted]\n" + value[-(limit - 2048):]

    code_token = "EXIT_ZERO" if int(exit_code) == 0 else "EXIT_NONZERO"
    return f"CMD {command or ''}\n{code_token} EXIT_CODE_{int(exit_code)}\nOUT {clip(stdout)}\nERR {clip(stderr)}"


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


def hashed_features(text: str) -> list[int]:
    features: set[int] = set()
    normalized = normalize_numbers(text) + " " + semantic_signals(text)
    tokens = TOKEN_RE.findall(normalized)
    for size in (1, 2, 3):
        for start in range(len(tokens) - size + 1):
            gram = " ".join(tokens[start:start + size])
            features.add(N_CHAR + (_fnv1a(f"w{size}:" + gram) % N_WORD))
    for token in tokens:
        padded = f" {token} "
        for size in (3, 4, 5):
            if len(padded) < size:
                continue
            for start in range(len(padded) - size + 1):
                features.add(_fnv1a("c:" + padded[start:start + size]) % N_CHAR)
    return sorted(features)


def sparse_matrix(texts: list[str]) -> csr_matrix:
    indices = array("i")
    indptr = array("i", [0])
    values = array("f")
    for text in texts:
        row = hashed_features(text)
        indices.extend(row)
        values.extend([1.0] * len(row))
        indptr.append(len(indices))
    return csr_matrix(
        (np.frombuffer(values, dtype=np.float32), np.frombuffer(indices, dtype=np.int32), np.frombuffer(indptr, dtype=np.int32)),
        shape=(len(texts), N_FEATURES),
    )
