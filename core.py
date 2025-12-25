import hashlib
import re
from datetime import datetime
from typing import Dict, List, Optional


class SynthesisStudio:
    def __init__(self, name: str = "ArcDistiller Studio") -> None:
        if not isinstance(name, str):
            raise TypeError("name must be a string")
        self.name = name
        self.sigil_map = {"💠": 5, "✨": 3, "•": 1}
        self.echo_log: List[Dict[str, object]] = []

    # --- WING 1: PARSING ---
    def parse_chat_line(self, line: str) -> Optional[Dict[str, str]]:
        """Extract sender and text from standard chat formats."""
        if not isinstance(line, str):
            raise TypeError("line must be a string")

        cleaned = line.strip()
        if not cleaned:
            return None

        patterns = [
            # [Date, Time] Name: Message (seconds optional)
            r"^\[?(?P<timestamp>\d{1,2}/\d{1,2}/\d{4},\s*\d{1,2}:\d{2}(?::\d{2})?)\]?\s+(?P<sender>[^:]+):\s*(?P<text>.+)$",
            # Date, Time Name: Message (no brackets)
            r"^(?P<timestamp>\d{1,2}/\d{1,2}/\d{4},\s*\d{1,2}:\d{2}(?::\d{2})?)\s+(?P<sender>[^:]+):\s*(?P<text>.+)$",
            # Name: Message (no timestamp)
            r"^(?P<sender>[^:]+):\s*(?P<text>.+)$",
        ]

        for pattern in patterns:
            match = re.match(pattern, cleaned)
            if match:
                return {
                    "sender": match.group("sender").strip(),
                    "text": match.group("text").strip(),
                }

        return None

    # --- WING 2: EVALUATION ---
    def evaluate_resonance(self, text: str) -> int:
        """Calculate the alignment/priority score."""
        if not isinstance(text, str):
            raise TypeError("text must be a string")
        return sum(text.count(sigil) * weight for sigil, weight in self.sigil_map.items())

    # --- WING 3: SYNTHESIS ---
    def synthesize_echo(self, entry: Dict[str, str], cycle: int, persist: bool = False) -> Dict[str, str]:
        """Transform a parsed entry into a Prismatic Echo."""
        if not isinstance(entry, dict):
            raise TypeError("entry must be a dict with sender and text")
        if "sender" not in entry or "text" not in entry:
            raise ValueError("entry must contain 'sender' and 'text'")
        if not isinstance(entry["sender"], str) or not isinstance(entry["text"], str):
            raise TypeError("entry 'sender' and 'text' must be strings")
        if not isinstance(cycle, int):
            raise TypeError("cycle must be an int")

        text = entry["text"]
        score = self.evaluate_resonance(text)
        ts = datetime.utcnow().isoformat()
        trace = hashlib.sha256(f"{text}{ts}".encode()).hexdigest()[:8]

        # High-weight = PRISM (detail), Low-weight = SEED (summary)
        echo_type = "⟨PRISM⟩" if score >= 5 else "⟨SEED⟩"
        body = text if score >= 5 else text[:60] + "..."

        echo = {
            "trace": trace,
            "role": entry["sender"].lower(),
            "type": echo_type,
            "body": body,
            "weight": score,
            "cycle": cycle,
        }

        if persist:
            self.echo_log.append(echo)

        return echo

    def process_lines(self, lines: List[str], cycle: int, persist: bool = False) -> List[Dict[str, str]]:
        """Parse lines, synthesize echoes, and optionally persist them."""
        if not isinstance(lines, list):
            raise TypeError("lines must be a list of strings")
        if not isinstance(cycle, int):
            raise TypeError("cycle must be an int")

        echoes: List[Dict[str, str]] = []
        for line in lines:
            if not isinstance(line, str):
                raise TypeError("lines must contain only strings")
            entry = self.parse_chat_line(line)
            if entry is None:
                continue
            echoes.append(self.synthesize_echo(entry, cycle=cycle, persist=persist))

        return echoes

