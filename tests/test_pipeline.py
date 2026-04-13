"""Tests for kreuzberg_txtai.pipeline.KreuzbergPipeline."""

from __future__ import annotations

from typing import TYPE_CHECKING

import pytest

from kreuzberg_txtai import KreuzbergPipeline

if TYPE_CHECKING:
    from pathlib import Path


@pytest.fixture
def pipeline() -> KreuzbergPipeline:
    return KreuzbergPipeline()


def test_single_path_returns_length_one_list(pipeline: KreuzbergPipeline, sample_html_path: Path) -> None:
    docs = pipeline(str(sample_html_path))

    assert isinstance(docs, list)
    assert len(docs) == 1


def test_single_path_content_is_non_empty_string(pipeline: KreuzbergPipeline, sample_html_path: Path) -> None:
    docs = pipeline(str(sample_html_path))

    assert isinstance(docs[0]["content"], str)
    assert "Sample Document" in docs[0]["content"]
