"""
Skill normalization.

The spec (Page 9) explicitly warns: discrepancies in naming
conventions (e.g. "Web Design" vs. "Frontend Development") will cause
the similarity math to fail, because the two terms occupy different
vocabulary dimensions even though they mean the same thing to a human.

This module is the single place where that risk is mitigated, via:
  1. Case-folding and whitespace trimming.
  2. A synonym map that collapses common aliases to one canonical term.

It MUST run before vectorization -- normalizing after the vocabulary
is built would be too late, since the mismatch would already exist.
"""

# Maps common aliases/variants -> canonical skill name.
# Extend this map as new mismatches are discovered in production.
_SYNONYM_MAP: dict[str, str] = {
    "js": "javascript",
    "ts": "javascript",  # treated as same family for this engine's scope
    "ml": "machine learning",
    "k8s": "kubernetes",
    "cloud": "cloud computing",
    "ci": "ci/cd",
    "cd": "ci/cd",
    "ci cd": "ci/cd",
    "rdbms": "database design",
    "oop": "object oriented design",
    "devops": "automation",
    "py": "python",
    "tf": "terraform",
    "aws cloud": "aws",
}


class SkillNormalizer:
    """Normalizes raw skill strings into a canonical vocabulary form."""

    def __init__(self, synonym_map: dict[str, str] | None = None) -> None:
        self._synonym_map = synonym_map if synonym_map is not None else _SYNONYM_MAP

    def normalize(self, skill: str) -> str:
        """
        Normalize a single skill string.

        Steps: trim whitespace -> lowercase -> alias lookup.
        """
        cleaned = skill.strip().lower()
        return self._synonym_map.get(cleaned, cleaned)

    def normalize_all(self, skills: list[str]) -> list[str]:
        """
        Normalize a list of skills and remove duplicates while
        preserving the first-seen order (deterministic output).
        """
        seen: set[str] = set()
        result: list[str] = []
        for skill in skills:
            normalized = self.normalize(skill)
            if normalized and normalized not in seen:
                seen.add(normalized)
                result.append(normalized)
        return result
