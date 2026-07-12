#!/usr/bin/env python3
from __future__ import annotations

import argparse
import hashlib
import json
import re
import shutil
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import NamedTuple, Sequence


class BundleResult(NamedTuple):
    bundle_dir: Path
    markdown_path: Path
    metadata_path: Path
    checksum_path: Path
    warnings_path: Path


def slugify(value: str) -> str:
    slug = re.sub(r"[^a-z0-9]+", "-", value.lower()).strip("-")
    return slug or "document"


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def create_bundle(
    source: Path,
    out_dir: Path | None = None,
    title: str | None = None,
    converter_command: Sequence[str] | None = None,
    force: bool = False,
) -> BundleResult:
    source = Path(source).resolve()
    if not source.is_file():
        raise FileNotFoundError(f"Source file not found: {source}")

    slug = slugify(source.stem)
    bundle_dir = Path(out_dir or Path("data") / "ingested" / slug).resolve()
    if bundle_dir.exists() and not force:
        raise FileExistsError(f"Bundle already exists: {bundle_dir}. Re-run with --force to overwrite.")
    bundle_dir.mkdir(parents=True, exist_ok=True)

    archived_source = bundle_dir / source.name
    if archived_source.resolve() != source:
        shutil.copy2(source, archived_source)

    markdown_path = bundle_dir / f"{slug}.md"
    metadata_path = bundle_dir / f"{slug}.metadata.json"
    checksum_path = bundle_dir / f"{slug}.checksum.txt"
    warnings_path = bundle_dir / f"{slug}.warnings.txt"

    command = list(converter_command or ["markitdown"])
    completed = subprocess.run(
        [*command, str(source), "-o", str(markdown_path)],
        check=False,
        capture_output=True,
        text=True,
    )

    warnings_text = "".join(
        part
        for part in (completed.stdout, completed.stderr)
        if part
    )
    warnings_path.write_text(warnings_text or "No converter warnings captured.\n", encoding="utf-8")

    if completed.returncode != 0:
        raise RuntimeError(
            f"MarkItDown conversion failed with exit code {completed.returncode}. "
            f"See {warnings_path}."
        )
    if not markdown_path.is_file():
        raise RuntimeError(f"Converter did not write expected markdown file: {markdown_path}")

    checksum = sha256_file(source)
    checksum_path.write_text(f"{checksum}  {source.name}\n", encoding="utf-8")

    metadata = {
        "document": {
            "title": title or source.stem,
            "slug": slug,
            "review_status": "needs-review",
        },
        "source": {
            "filename": source.name,
            "original_path": str(source),
            "archived_path": str(archived_source),
            "sha256": checksum,
            "bytes": source.stat().st_size,
        },
        "conversion": {
            "tool": "markitdown",
            "command": command,
            "converted_at": datetime.now(timezone.utc).isoformat(),
            "markdown_path": str(markdown_path),
            "warnings_path": str(warnings_path),
            "exit_code": completed.returncode,
        },
    }
    metadata_path.write_text(json.dumps(metadata, indent=2, sort_keys=True) + "\n", encoding="utf-8")

    return BundleResult(
        bundle_dir=bundle_dir,
        markdown_path=markdown_path,
        metadata_path=metadata_path,
        checksum_path=checksum_path,
        warnings_path=warnings_path,
    )


def parse_args(argv: Sequence[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Convert a source document with MarkItDown and write an auditable ingestion bundle."
    )
    parser.add_argument("source", type=Path, help="PDF, DOCX, XLSX, HTML, TXT, or other MarkItDown-supported file")
    parser.add_argument("--out-dir", type=Path, default=None, help="Bundle directory; defaults to data/ingested/<slug>")
    parser.add_argument("--title", default=None, help="Human-readable document title for metadata")
    parser.add_argument("--force", action="store_true", help="Allow writing into an existing bundle directory")
    parser.add_argument(
        "--converter-command",
        nargs="+",
        default=["markitdown"],
        help="Converter command to run. For multi-arg commands, put this option last.",
    )
    return parser.parse_args(argv)


def main(argv: Sequence[str] | None = None) -> int:
    args = parse_args(argv or sys.argv[1:])
    try:
        result = create_bundle(
            source=args.source,
            out_dir=args.out_dir,
            title=args.title,
            converter_command=args.converter_command,
            force=args.force,
        )
    except Exception as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 1

    print(result.bundle_dir)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
