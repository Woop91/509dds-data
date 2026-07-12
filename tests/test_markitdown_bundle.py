import importlib.util
import json
import sys
import unittest
from pathlib import Path
from tempfile import TemporaryDirectory


SCRIPT_PATH = Path(__file__).resolve().parents[1] / "scripts" / "markitdown_bundle.py"


def load_module():
    spec = importlib.util.spec_from_file_location("markitdown_bundle", SCRIPT_PATH)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


def write_fake_converter(path: Path) -> None:
    path.write_text(
        """
import argparse
import sys

parser = argparse.ArgumentParser()
parser.add_argument("source")
parser.add_argument("-o", "--output", required=True)
args = parser.parse_args()

source_text = open(args.source, "r", encoding="utf-8").read()
open(args.output, "w", encoding="utf-8").write("# Converted\\n\\n" + source_text)
print("fake converter warning", file=sys.stderr)
""".strip(),
        encoding="utf-8",
    )


class MarkItDownBundleTests(unittest.TestCase):
    def test_create_bundle_writes_markdown_metadata_checksum_and_warnings(self):
        module = load_module()
        with TemporaryDirectory() as tmp:
            tmp_path = Path(tmp)
            source = tmp_path / "source doc.txt"
            source.write_text("source body", encoding="utf-8")
            converter = tmp_path / "fake_converter.py"
            write_fake_converter(converter)

            result = module.create_bundle(
                source=source,
                out_dir=tmp_path / "bundle",
                title="Source Document",
                converter_command=[sys.executable, str(converter)],
                force=False,
            )

            self.assertEqual(result.markdown_path.read_text(encoding="utf-8"), "# Converted\n\nsource body")
            self.assertEqual((result.bundle_dir / "source doc.txt").read_text(encoding="utf-8"), "source body")
            self.assertIn("fake converter warning", result.warnings_path.read_text(encoding="utf-8"))
            self.assertIn("source doc.txt", result.checksum_path.read_text(encoding="utf-8"))

            metadata = json.loads(result.metadata_path.read_text(encoding="utf-8"))
            self.assertEqual(metadata["document"]["title"], "Source Document")
            self.assertEqual(metadata["document"]["slug"], "source-doc")
            self.assertEqual(metadata["document"]["review_status"], "needs-review")
            self.assertEqual(metadata["source"]["filename"], "source doc.txt")
            self.assertTrue(metadata["source"]["sha256"])
            self.assertEqual(metadata["conversion"]["tool"], "markitdown")
            self.assertEqual(metadata["conversion"]["exit_code"], 0)

    def test_existing_bundle_requires_force(self):
        module = load_module()
        with TemporaryDirectory() as tmp:
            tmp_path = Path(tmp)
            source = tmp_path / "source.txt"
            source.write_text("source body", encoding="utf-8")
            out_dir = tmp_path / "bundle"
            out_dir.mkdir()

            with self.assertRaisesRegex(FileExistsError, "already exists"):
                module.create_bundle(
                    source=source,
                    out_dir=out_dir,
                    title=None,
                    converter_command=[sys.executable, "-c", "print('unused')"],
                    force=False,
                )


if __name__ == "__main__":
    unittest.main()
