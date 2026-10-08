"""Report stage: derive frequency tables. Counts are never hardcoded."""
from collections import Counter
from typing import Any, Mapping


def skill_frequency(records: list[dict[str, Any]]) -> Counter:
    counter: Counter = Counter()
    for index, record in enumerate(records):
        skills = record.get("skills")
        if skills is None:
            skills = []
        if not isinstance(skills, list):
            raise ValueError(
                f"record {index}: 'skills' must be a list of strings, "
                f"got {type(skills).__name__}"
            )
        if not all(isinstance(skill, str) for skill in skills):
            raise ValueError(f"record {index}: 'skills' must contain only strings")
        # Case-insensitive, whitespace-safe, and counted once per record so a
        # duplicated bullet cannot inflate a skill's share of the corpus.
        seen: set[str] = set()
        ordered: list[str] = []
        for skill in skills:
            key = skill.strip().lower()
            if not key or key in seen:
                continue
            seen.add(key)
            ordered.append(key)
        counter.update(ordered)
    return counter


def to_markdown(counter: Mapping[str, int], total: int) -> str:
    ordered = Counter(counter).most_common()
    lines = ["| Skill | Count | Share |", "|---|---|---|"]
    for skill, count in ordered:
        share = (count / total * 100) if total else 0
        lines.append(f"| {skill} | {count} | {share:.0f}% |")
    return "\n".join(lines)
