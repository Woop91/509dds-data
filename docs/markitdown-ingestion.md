# MarkItDown Ingestion

Use `scripts/markitdown_bundle.py` to convert source documents into auditable Markdown bundles before parsing, indexing, or copying content into application repos.

## Install

Install MarkItDown in the Python environment used for data work:

```bash
pip install "markitdown[all]"
```

## Convert a document

```bash
npm run ingest:markitdown -- data/source/example.pdf --title "Example Source"
```

By default the wrapper writes:

```text
data/ingested/example/
  example.pdf
  example.md
  example.metadata.json
  example.checksum.txt
  example.warnings.txt
```

## Bundle contract

- Keep the original file in the bundle.
- Keep the generated Markdown next to the original file.
- Keep metadata, checksum, and warnings files so every extract can be traced back to the source document.
- Treat generated Markdown as `needs-review` until a human checks tables, footnotes, page headers, and OCR-sensitive sections.
- Use `--force` only when intentionally regenerating a bundle from the same source.

## Custom converter command

If MarkItDown is not on `PATH`, pass the converter command explicitly. For multi-argument commands, place this option last.

```bash
python scripts/markitdown_bundle.py data/source/example.pdf --converter-command python -m markitdown
```

## Downstream use

The Markdown bundle is the handoff point for:

- statistical extraction scripts in this repo,
- `509dds-audit-runs` evidence normalization,
- `agentward` library ingestion,
- future steward document workflows in `509dds`.
