import argparse
import json
import sys
from pathlib import Path

from content_distill.core import SynthesisStudio


def main() -> int:
    parser = argparse.ArgumentParser(
        description="content-distill: structured text distillation"
    )
    parser.add_argument("input", type=Path)
    parser.add_argument("--cycle", type=int, required=True)
    parser.add_argument("--persist", action="store_true")
    args = parser.parse_args()

    if not args.input.is_file():
        print("error: input file not found", file=sys.stderr)
        return 1

    engine = SynthesisStudio()

    for line in args.input.read_text(encoding="utf-8").splitlines():
        entry = engine.parse_chat_line(line)
        if entry is None:
            continue

        echo = engine.synthesize_echo(
            entry=entry,
            cycle=args.cycle,
            persist=args.persist,
        )

        json.dump(echo, sys.stdout, ensure_ascii=False)
        sys.stdout.write("\n")

    return 0


if __name__ == "__main__":
    sys.exit(main())
