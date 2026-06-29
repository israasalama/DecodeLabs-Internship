"""
Custom exceptions for the Tech Stack Recommender.

Using specific exception types (instead of generic ValueError/Exception
everywhere) lets calling code react differently to different failure
modes -- e.g. the CLI can catch InsufficientSkillsError and simply
re-prompt the user, while EmptyDatasetError is fatal and should exit.
"""


class RecommenderError(Exception):
    """Base class for all recommender-specific errors."""


class InsufficientSkillsError(RecommenderError):
    """Raised when the user provides fewer than the minimum required skills."""


class EmptyDatasetError(RecommenderError):
    """Raised when the job-roles dataset is missing, empty, or malformed."""


class ColdStartError(RecommenderError):
    """
    Raised internally when a user's skill vector has zero overlap with
    every job role in the dataset (the "Cold Start" problem, Page 20).

    This is caught by the pipeline and converted into a graceful
    trending-roles fallback -- it should never reach the end user as
    a raw error.
    """
