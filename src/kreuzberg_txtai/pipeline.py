"""Kreuzberg-backed document extraction pipeline."""

from __future__ import annotations

from typing import Any

from kreuzberg import ExtractionConfig, OcrConfig, extract_file_sync


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
            output_format: Kreuzberg output format. Defaults to ``"markdown"``.
            ocr_backend: OCR engine name. ``None`` uses Kreuzberg's default.
            ocr_language: ISO 639 language code for OCR. ``None`` uses default.
            force_ocr: Force OCR even on text-extractable documents.
            config: Full ``ExtractionConfig`` override. When provided, the
                scalar kwargs above are ignored.
        """
        if config is not None:
            self._config = config
        else:
            ocr_config = (
                OcrConfig(backend=ocr_backend, language=ocr_language)
                if ocr_backend is not None or ocr_language is not None
                else None
            )
            self._config = ExtractionConfig(
                output_format=output_format,
                ocr=ocr_config,
                force_ocr=force_ocr,
            )

    def __call__(self, documents: str | list[str]) -> list[dict[str, Any]]:
        """Extract text and metadata from one or more documents.

        Args:
            documents: A single file path, or a list of file paths.

        Returns:
            A list of dicts with ``content`` and ``metadata`` keys. The list
            has one element per input path, in input order. A single-string
            input still returns a one-element list.
        """
        paths = [documents] if isinstance(documents, str) else list(documents)
        return [self._extract_one(path) for path in paths]

    def _extract_one(self, path: str) -> dict[str, Any]:
        result = extract_file_sync(path, config=self._config)
        metadata = result.metadata or {}
        return {
            "content": result.content,
            "metadata": {
                "source": path,
                "mime_type": result.mime_type,
                "title": metadata.get("title"),
                "page_count": metadata.get("page_count"),
            },
        }
