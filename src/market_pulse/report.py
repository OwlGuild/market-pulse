"""Report stage: derive frequency tables. Counts are never hardcoded."""
from collections import Counter
from typing import Any, Mapping


def skill_frequency(records: list[dict[str, Any]]) -> Counter:
    counter: Counter = Counter()
    for r in records:
        for skill in r.get("skills", []):
            counter[skill.lower()] += 1
    return counter


def to_markdown(counter: Mapping[str, int], total: int) -> str:
    ordered = Counter(counter).most_common()
    lines = ["| Skill | Count | Share |", "|---|---|---|"]
    for skill, count in ordered:
        share = (count / total * 100) if total else 0
        lines.append(f"| {skill} | {count} | {share:.0f}% |")
    return "\n".join(lines)
