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


def test_batch_input_preserves_order_and_length(
    pipeline: KreuzbergPipeline,
    sample_html_path: Path,
    sample_pdf_path: Path,
) -> None:
    paths = [str(sample_html_path), str(sample_pdf_path)]

    docs = pipeline(paths)

    assert len(docs) == 2
    assert docs[0]["metadata"]["source"] == paths[0]
    assert docs[1]["metadata"]["source"] == paths[1]


def test_batch_input_returns_list_even_for_single_element(
    pipeline: KreuzbergPipeline,
    sample_html_path: Path,
) -> None:
    docs = pipeline([str(sample_html_path)])

    assert len(docs) == 1
    assert docs[0]["metadata"]["source"] == str(sample_html_path)


def test_empty_list_returns_empty_list(pipeline: KreuzbergPipeline) -> None:
    docs = pipeline([])

    assert docs == []


def test_metadata_source_matches_input_path(pipeline: KreuzbergPipeline, sample_html_path: Path) -> None:
    path = str(sample_html_path)

    docs = pipeline(path)

    assert docs[0]["metadata"]["source"] == path


def test_metadata_mime_type_is_populated_for_html(pipeline: KreuzbergPipeline, sample_html_path: Path) -> None:
    docs = pipeline(str(sample_html_path))

    mime = docs[0]["metadata"]["mime_type"]
    assert mime is not None
    assert "html" in mime.lower()


def test_metadata_has_stable_keys(pipeline: KreuzbergPipeline, sample_html_path: Path) -> None:
    docs = pipeline(str(sample_html_path))

    expected_keys = {"source", "mime_type", "title", "page_count"}
    assert set(docs[0]["metadata"].keys()) == expected_keys
