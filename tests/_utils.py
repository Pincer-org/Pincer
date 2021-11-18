# Copyright Pincer 2021-Present
# Full MIT License can be found in `LICENSE` at the project root.

from contextlib import contextmanager


@contextmanager
def assert_not_raises():
    """Dummy context manager to highlight a row of a test
    that should not raises any exception"""
    yield
