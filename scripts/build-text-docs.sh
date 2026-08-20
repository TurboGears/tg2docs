#!/usr/bin/env bash
set -euo pipefail

repo_root=$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)
build_root=$(mktemp -d)
archive="$repo_root/tg2docs.txt.zip"
trap 'rm -rf "$build_root"' EXIT

python3 -m sphinx --keep-going \
    -b text \
    -d "$build_root/doctrees" \
    "$repo_root/docs" \
    "$build_root/text"

python3 - "$build_root/text" "$archive" <<'PY'
from pathlib import Path
from sys import argv
from zipfile import ZIP_DEFLATED, ZipFile

text_root = Path(argv[1])
archive_path = Path(argv[2])
text_files = sorted(text_root.rglob("*.txt"))

with ZipFile(archive_path, "w", compression=ZIP_DEFLATED) as archive:
    for text_file in text_files:
        archive.write(text_file, text_file.relative_to(text_root))

print(f"Created {archive_path} with {len(text_files)} text files")
PY
