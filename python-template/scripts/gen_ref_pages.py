"""Generate API reference pages from docstrings."""

from pathlib import Path

import mkdocs_gen_files

src_root = Path("src")
for path in sorted(src_root.rglob("*.py")):
    if path.name == "__init__.py":
        continue
    module = ".".join(path.with_suffix("").parts[1:])
    doc_path = Path("api", *path.with_suffix(".md").parts[1:])
    with mkdocs_gen_files.open(doc_path, "w") as f:
        f.write(f"::: {module}\n")
