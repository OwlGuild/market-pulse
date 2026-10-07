"""Report stage: derive frequency tables. Counts are never hardcoded."""
from collections import Counter
from typing import Any, Mapping


def skill_frequency(records: list[dict[str, Any]]) -> Counter:
    counter: Counter = Counter()
    for record in records:
        skills = record.get("skills") or []
        # Case-insensitive, whitespace-safe, and counted once per record so a
        # duplicated bullet cannot inflate a skill's share of the corpus.
        unique = {s.strip().lower() for s in skills if isinstance(s, str) and s.strip()}
        counter.update(unique)
    return counter


def to_markdown(counter: Mapping[str, int], total: int) -> str:
    ordered = Counter(counter).most_common()
    lines = ["| Skill | Count | Share |", "|---|---|---|"]
    for skill, count in ordered:
        share = (count / total * 100) if total else 0
        lines.append(f"| {skill} | {count} | {share:.0f}% |")
    return "\n".join(lines)
