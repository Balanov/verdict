"""Command-line interface for Verdict."""
from __future__ import annotations

import argparse
import json
import sys

from .model import Verdict


def main() -> int:
    parser = argparse.ArgumentParser(description="Classify the semantic outcome of a CLI tool call.")
    parser.add_argument("--command", required=True, help="Executed command")
    parser.add_argument("--exit-code", required=True, type=int, help="Observed process exit code")
    parser.add_argument("--stdout", help="Stdout file; defaults to stdin when no output files are supplied")
    parser.add_argument("--stderr", help="Stderr file")
    parser.add_argument("--weights", help="Path to verdict-q8.bin")
    args = parser.parse_args()
    if args.stdout:
        stdout = open(args.stdout, encoding="utf-8").read()
    elif args.stderr:
        stdout = ""
    else:
        stdout = sys.stdin.read()
    stderr = open(args.stderr, encoding="utf-8").read() if args.stderr else ""
    result = Verdict(args.weights).predict(args.command, args.exit_code, stdout, stderr)
    print(json.dumps(result, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
