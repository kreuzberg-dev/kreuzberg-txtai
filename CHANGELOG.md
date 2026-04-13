# Changelog

All notable changes to this project are documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

## [0.1.0] - 2026-04-14

### Added
- `KreuzbergPipeline` class — a plain callable that turns document paths into
  `list[dict]` with `content` and `metadata` fields (source, MIME type, title,
  page count).
- Support for single-path and batch (`list[str]`) inputs.
- Constructor kwargs: `output_format`, `ocr_backend`, `ocr_language`,
  `force_ocr`, plus a `config` escape hatch accepting a full `ExtractionConfig`.
- Optional `txtai` extra for consumers who want to wire the output into
  `Embeddings.index` or `Task(pipe)` workflows.
- PEP 561 `py.typed` marker.
