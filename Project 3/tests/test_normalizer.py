"""Unit tests for SkillNormalizer."""

from src.core.normalizer import SkillNormalizer


class TestSkillNormalizer:
    def setup_method(self) -> None:
        self.normalizer = SkillNormalizer()

    # --- normalize() ---------------------------------------------------

    def test_lowercases_input(self) -> None:
        assert self.normalizer.normalize("PYTHON") == "python"

    def test_trims_whitespace(self) -> None:
        assert self.normalizer.normalize("  sql  ") == "sql"

    def test_known_alias_is_mapped_to_canonical_form(self) -> None:
        assert self.normalizer.normalize("JS") == "javascript"
        assert self.normalizer.normalize("k8s") == "kubernetes"
        assert self.normalizer.normalize("ML") == "machine learning"

    def test_unknown_skill_passes_through_unchanged(self) -> None:
        assert self.normalizer.normalize("rust") == "rust"

    def test_empty_string_normalizes_to_empty_string(self) -> None:
        assert self.normalizer.normalize("") == ""

    # --- normalize_all() -------------------------------------------------

    def test_normalize_all_deduplicates_after_normalization(self) -> None:
        # "JS" and "js" both map to "javascript" -- should collapse to one.
        result = self.normalizer.normalize_all(["JS", "js", "JavaScript"])
        assert result.count("javascript") == 1

    def test_normalize_all_preserves_first_seen_order(self) -> None:
        result = self.normalizer.normalize_all(["sql", "python", "java"])
        assert result == ["sql", "python", "java"]

    def test_normalize_all_handles_empty_list(self) -> None:
        assert self.normalizer.normalize_all([]) == []

    def test_web_design_vs_frontend_development_mismatch_is_a_known_gap(self) -> None:
        """
        Documents the exact failure mode called out in the spec (Page 9):
        without an explicit alias entry, semantically-identical terms
        remain distinct vocabulary dimensions. This test demonstrates
        *why* the synonym map must be actively maintained.
        """
        result = self.normalizer.normalize_all(["Web Design", "Frontend Development"])
        assert len(result) == 2  # Not yet aliased -- a documented limitation.
