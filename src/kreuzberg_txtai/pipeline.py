"""Kreuzberg-backed document extraction pipeline."""

from __future__ import annotations

from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    from kreuzberg import ExtractionConfig


class KreuzbergPipeline:
    """Kreuzberg-backed document extraction pipeline.

    A plain callable class that accepts one or more document paths and
    returns structured extraction results suitable for any downstream
    pipeline framework — txtai workflows, LangChain loaders, or direct
    use with embeddings indices.
    """

    def __init__(
        self,
        output_format: str = "markdown",
        ocr_backend: str | None = None,
        ocr_language: str | None = None,
        *,
        force_ocr: bool = False,
        config: ExtractionConfig | None = None,
    ) -> None:
        """Initialize the pipeline.

        Args:
            output_format: Kreuzberg output format. Defaults to "markdown".
            ocr_backend: OCR engine name. ``None`` uses Kreuzberg's default.
            ocr_language: ISO 639 language code for OCR. ``None`` uses default.
            force_ocr: Force OCR even on text-extractable documents.
            config: Full ``ExtractionConfig`` override. When provided, the
                scalar kwargs above are ignored.
        """
        raise NotImplementedError

    def __call__(self, documents: str | list[str]) -> list[dict[str, Any]]:
        """Extract text and metadata from one or more documents.

        Args:
            documents: A single file path, or a list of file paths.

        Returns:
            A list of dicts with ``content`` and ``metadata`` keys. The list
            has one element per input path, in input order. A single-string
            input still returns a one-element list.
        """
        raise NotImplementedError
