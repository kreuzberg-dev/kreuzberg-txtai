"""Kreuzberg-backed document extraction pipeline."""

from typing import Any

from kreuzberg import ExtractionConfig, extract_file_sync


class KreuzbergPipeline:
    """Kreuzberg-backed document extraction pipeline.

    A plain callable class that accepts one or more document paths and
    returns structured extraction results suitable for any downstream
    pipeline framework — txtai workflows, LangChain loaders, or direct
    use with embeddings indices.
    """

    def __init__(self, config: ExtractionConfig | None = None) -> None:
        """Initialize the pipeline.

        Args:
            config: A Kreuzberg ``ExtractionConfig``. Pass one to control
                output format, OCR backend and language, ``force_ocr``, and
                every other Kreuzberg knob — they are all fields on
                ``ExtractionConfig`` (OCR settings live on the nested
                ``OcrConfig``). When omitted, Kreuzberg's defaults apply.

                Example::

                    from kreuzberg import ExtractionConfig, OcrConfig

                    config = ExtractionConfig(
                        output_format="markdown",
                        ocr=OcrConfig(backend="tesseract", language="eng"),
                        force_ocr=True,
                    )
                    pipeline = KreuzbergPipeline(config=config)

        """
        self._config = config

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
