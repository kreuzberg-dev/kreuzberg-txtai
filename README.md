# kreuzberg-txtai

<div align="center" style="display: flex; flex-wrap: wrap; gap: 8px; justify-content: center; margin: 20px 0;">
  <a href="https://pypi.org/project/kreuzberg-txtai/">
    <img src="https://img.shields.io/pypi/v/kreuzberg-txtai?label=PyPI&color=007ec6" alt="PyPI">
  </a>
  <a href="https://pypi.org/project/kreuzberg-txtai/">
    <img src="https://img.shields.io/pypi/pyversions/kreuzberg-txtai?color=007ec6" alt="Python versions">
  </a>
  <a href="https://pypi.org/project/kreuzberg-txtai/">
    <img src="https://img.shields.io/pypi/dm/kreuzberg-txtai" alt="Downloads">
  </a>
  <a href="https://github.com/kreuzberg-dev/kreuzberg-txtai/actions/workflows/ci.yaml">
    <img src="https://github.com/kreuzberg-dev/kreuzberg-txtai/actions/workflows/ci.yaml/badge.svg" alt="CI">
  </a>
  <a href="https://github.com/kreuzberg-dev/kreuzberg-txtai/blob/main/LICENSE">
    <img src="https://img.shields.io/badge/License-MIT-blue.svg" alt="License">
  </a>
  <a href="https://github.com/kreuzberg-dev/kreuzberg">
    <img src="https://img.shields.io/github/stars/kreuzberg-dev/kreuzberg?style=flat&label=Kreuzberg&color=007ec6" alt="Kreuzberg">
  </a>
  <a href="https://docs.kreuzberg.dev">
    <img src="https://img.shields.io/badge/docs-kreuzberg.dev-blue" alt="Documentation">
  </a>
</div>

<div align="center" style="margin-top: 20px;">
  <a href="https://discord.gg/xt9WY3GnKR">
    <img height="22" src="https://img.shields.io/badge/Discord-Join%20our%20community-7289da?logo=discord&logoColor=white" alt="Discord">
  </a>
</div>

## Overview

**kreuzberg-txtai** is a [Kreuzberg](https://github.com/kreuzberg-dev/kreuzberg)-backed document extraction pipeline for [txtai](https://github.com/neuml/txtai) and any other Python framework built around the `__call__` convention. It replaces txtai's built-in `Textractor` (Apache Tika-based) with Kreuzberg's Rust-powered extraction stack, surfacing rich metadata — title, MIME type, page count — that Tika flattens away.

The core is a single class, `KreuzbergPipeline`, that turns document paths into a `list[dict]` with `content` and `metadata` fields, ready to plug into an embeddings index, a workflow task, or a plain `for` loop.

## Installation

```bash
pip install kreuzberg-txtai
```

For the txtai integration examples below:

```bash
pip install "kreuzberg-txtai[txtai]"
```

Requires Python 3.10+.

## Quick Start

```python
from kreuzberg_txtai import KreuzbergPipeline

pipeline = KreuzbergPipeline(output_format="markdown")
docs = pipeline(["doc1.pdf", "doc2.docx", "doc3.html"])

for doc in docs:
    print(doc["metadata"]["source"], "->", len(doc["content"]), "chars")
```

Each element in `docs` looks like:

```python
{
    "content": "# Sample Document\n\nExtracted text...",
    "metadata": {
        "source": "doc1.pdf",
        "mime_type": "application/pdf",
        "title": "Sample Document",
        "page_count": 5,
    },
}
```

## Features

- **88+ file formats** — PDF, DOCX, PPTX, XLSX, images, HTML, Markdown, plain text, and more via Kreuzberg
- **Stable dict contract** — every extraction returns `content` + `metadata` with the same four keys, regardless of source format
- **Rich metadata** — source path, MIME type, title, and page count surface directly; use the `config` escape hatch for deeper Kreuzberg fields
- **Batch support** — pass a single path or a `list[str]`; output is always `list[dict]` in input order
- **OCR-ready** — `ocr_backend`, `ocr_language`, and `force_ocr` constructor kwargs map straight through to Kreuzberg's OCR pipeline
- **Framework-agnostic** — txtai is an optional extra, not a hard dependency; the pipeline works in any framework that accepts a callable
- **Typed** — ships with a `py.typed` marker; full mypy strict compatibility

## Usage Examples

### RAG ingestion with `txtai.Embeddings`

The dominant real-world pattern — extract, index, search:

```python
from kreuzberg_txtai import KreuzbergPipeline
from txtai import Embeddings

pipeline = KreuzbergPipeline(output_format="markdown")
docs = pipeline(["doc1.pdf", "doc2.docx", "doc3.html"])

embeddings = Embeddings({
    "path": "sentence-transformers/all-MiniLM-L6-v2",
    "content": True,
})
embeddings.index([(i, doc["content"], None) for i, doc in enumerate(docs)])

results = embeddings.search("query", limit=5)
```

### Inside a `txtai.workflow.Task`

`Task` accepts any callable, so `KreuzbergPipeline` drops in without wrappers. Because the pipeline returns `list[dict]`, downstream tasks that expect strings need a one-line adapter:

```python
from txtai.workflow import Task, Workflow
from kreuzberg_txtai import KreuzbergPipeline

extract = KreuzbergPipeline()

wf = Workflow([
    Task(extract),
    Task(lambda docs: [d["content"] for d in docs]),  # flatten dicts -> strings
])

list(wf(["doc1.pdf", "doc2.pdf"]))
```

### Framework-free loop

```python
from kreuzberg_txtai import KreuzbergPipeline

pipeline = KreuzbergPipeline(output_format="plain")
for doc in pipeline(["scan1.pdf", "scan2.pdf"]):
    print(doc["metadata"]["source"], "->", len(doc["content"]), "chars")
```

No txtai needed — the class works on just the core `kreuzberg` dependency.

### Full Kreuzberg config override

For knobs that aren't exposed as top-level kwargs, pass an `ExtractionConfig` directly. When `config` is provided, the scalar kwargs (`output_format`, `ocr_backend`, `ocr_language`, `force_ocr`) are ignored:

```python
from kreuzberg import ExtractionConfig, OcrConfig
from kreuzberg_txtai import KreuzbergPipeline

custom = ExtractionConfig(
    output_format="markdown",
    ocr=OcrConfig(backend="tesseract", language="eng+deu"),
    force_ocr=True,
)

pipeline = KreuzbergPipeline(config=custom)
docs = pipeline("scanned_report.pdf")
```

## Constructor

| Parameter | Type | Default | Notes |
|---|---|---|---|
| `output_format` | `str` | `"markdown"` | Kreuzberg output format (`"plain"`, `"markdown"`, `"html"`, `"djot"`, `"structured"`) |
| `ocr_backend` | `str \| None` | `None` | OCR engine; `None` uses Kreuzberg's default backend |
| `ocr_language` | `str \| None` | `None` | ISO 639 code; `None` uses the backend default |
| `force_ocr` | `bool` | `False` | Force OCR even on text-extractable PDFs |
| `config` | `ExtractionConfig \| None` | `None` | Full override; bypasses the scalar kwargs when provided |

## Return Shape

`__call__` always returns `list[dict]` — a single-path input still returns a length-1 list. Each dict has exactly two top-level keys:

- `content` — the extracted text in the requested `output_format`
- `metadata` — a dict with exactly four keys: `source`, `mime_type`, `title`, `page_count`

Missing metadata fields are `None` (rather than omitted) to keep the dict shape stable across document types.

## Related Projects

- **[kreuzberg](https://github.com/kreuzberg-dev/kreuzberg)** — the extraction engine powering this package
- **[langchain-kreuzberg](https://github.com/kreuzberg-dev/langchain-kreuzberg)** — Kreuzberg document loader for LangChain
- **[llama-index-kreuzberg](https://github.com/kreuzberg-dev/llama-index-kreuzberg)** — LlamaIndex reader and node parser
- **[kreuzberg-crewai](https://github.com/kreuzberg-dev/kreuzberg-crewai)** — CrewAI agent tool
- **[kreuzberg-surrealdb](https://github.com/kreuzberg-dev/kreuzberg-surrealdb)** — SurrealDB ingestion connector

## License

MIT — see [LICENSE](./LICENSE).
