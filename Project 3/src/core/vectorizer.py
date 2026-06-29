"""
TF-IDF Vectorizer.

Implements the exact formulas specified (Page 12):

    TF(t, d)  = (count of term t in document d) / (total terms in d)
    IDF(t)    = log(total documents / documents containing term t)
    weight(t) = TF(t, d) * IDF(t)

This is a from-scratch implementation (no scikit-learn) because the
spec frames this project as mastering the "fundamental art" of
similarity logic before reaching for higher-level libraries.
"""

import math
from collections import Counter


class TfidfVectorizer:
    """
    Builds a shared vocabulary from a corpus of documents (each document
    being a list of skill tags) and transforms skill lists into TF-IDF
    weighted vectors within that shared vocabulary space.
    """

    def __init__(self) -> None:
        self._vocabulary: list[str] = []
        self._idf_scores: dict[str, float] = {}
        self._is_fitted: bool = False

    @property
    def vocabulary(self) -> list[str]:
        return list(self._vocabulary)

    def fit(self, documents: list[list[str]]) -> None:
        """
        Build the vocabulary and compute IDF scores from a corpus.

        Args:
            documents: A list of "documents," where each document is a
                list of skill tags (e.g. one job role's skill list).

        Raises:
            ValueError: If documents is empty.
        """
        if not documents:
            raise ValueError("Cannot fit vectorizer on an empty document set.")

        total_documents = len(documents)
        unique_terms: set[str] = set()
        document_frequency: Counter[str] = Counter()

        for doc in documents:
            unique_terms_in_doc = set(doc)
            unique_terms.update(unique_terms_in_doc)
            for term in unique_terms_in_doc:
                document_frequency[term] += 1

        self._vocabulary = sorted(unique_terms)
        self._idf_scores = {
            term: math.log(total_documents / document_frequency[term])
            if document_frequency[term] > 0
            else 0.0
            for term in self._vocabulary
        }
        # Smooth the edge case where every document contains every term
        # (log(1) = 0, which would zero-out otherwise-valid signal).
        # We add a small constant to avoid fully zeroing out IDF.
        for term, score in self._idf_scores.items():
            if score == 0.0:
                self._idf_scores[term] = 1e-9

        self._is_fitted = True

    def transform(self, skills: list[str]) -> list[float]:
        """
        Transform a list of skill tags into a TF-IDF weighted vector
        aligned to the fitted vocabulary.

        Skills not present in the fitted vocabulary are ignored (they
        cannot contribute to similarity math by definition -- this is
        part of how the Cold Start problem manifests, Page 20).

        Args:
            skills: A list of (already normalized) skill tags.

        Returns:
            A vector of floats, one per vocabulary term, in vocabulary order.

        Raises:
            RuntimeError: If called before fit().
        """
        if not self._is_fitted:
            raise RuntimeError("Vectorizer must be fit() before calling transform().")

        total_terms = len(skills) if skills else 1  # avoid division by zero
        term_counts = Counter(skills)

        vector: list[float] = []
        for term in self._vocabulary:
            tf = term_counts.get(term, 0) / total_terms
            idf = self._idf_scores.get(term, 0.0)
            vector.append(tf * idf)

        return vector
