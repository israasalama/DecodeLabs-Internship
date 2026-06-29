"""Unit tests for TfidfVectorizer."""

import pytest

from src.core.vectorizer import TfidfVectorizer


class TestTfidfVectorizer:
    def setup_method(self) -> None:
        self.vectorizer = TfidfVectorizer()

    # --- fit() -----------------------------------------------------------

    def test_fit_builds_sorted_vocabulary_from_documents(self) -> None:
        documents = [["python", "sql"], ["java", "sql"]]
        self.vectorizer.fit(documents)
        assert self.vectorizer.vocabulary == ["java", "python", "sql"]

    def test_fit_raises_on_empty_document_set(self) -> None:
        with pytest.raises(ValueError):
            self.vectorizer.fit([])

    def test_term_in_every_document_gets_near_zero_idf(self) -> None:
        """
        Page 11: terms appearing in EVERY document are generic and
        should be penalized almost to zero (smoothed, not literally
        zero, per our smoothing implementation).
        """
        documents = [["python", "sql"], ["python", "java"], ["python", "html"]]
        self.vectorizer.fit(documents)
        vector = self.vectorizer.transform(["python"])
        idx = self.vectorizer.vocabulary.index("python")
        assert vector[idx] < 1e-6

    def test_rare_term_gets_higher_idf_than_common_term(self) -> None:
        documents = [
            ["python", "sql"],
            ["python", "java"],
            ["python", "rare_skill"],
        ]
        self.vectorizer.fit(documents)
        vec_common = self.vectorizer.transform(["python"])
        vec_rare = self.vectorizer.transform(["rare_skill"])

        idx_common = self.vectorizer.vocabulary.index("python")
        idx_rare = self.vectorizer.vocabulary.index("rare_skill")

        assert vec_rare[idx_rare] > vec_common[idx_common]

    # --- transform() -------------------------------------------------------

    def test_transform_raises_if_called_before_fit(self) -> None:
        with pytest.raises(RuntimeError):
            self.vectorizer.transform(["python"])

    def test_transform_returns_vector_aligned_to_vocabulary_length(self) -> None:
        documents = [["python", "sql", "java"]]
        self.vectorizer.fit(documents)
        vector = self.vectorizer.transform(["python"])
        assert len(vector) == len(self.vectorizer.vocabulary)

    def test_transform_ignores_out_of_vocabulary_terms(self) -> None:
        """
        Cold Start / vocabulary mismatch scenario (Page 9, 20): unknown
        terms simply don't contribute -- they don't crash the system.
        """
        documents = [["python", "sql"]]
        self.vectorizer.fit(documents)
        vector = self.vectorizer.transform(["some_unknown_skill"])
        assert all(value == 0.0 for value in vector)

    def test_transform_empty_skill_list_returns_zero_vector(self) -> None:
        documents = [["python", "sql"]]
        self.vectorizer.fit(documents)
        vector = self.vectorizer.transform([])
        assert all(value == 0.0 for value in vector)
