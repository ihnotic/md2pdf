#!/usr/bin/env python3

from __future__ import annotations

import html
import pathlib
import re
import sys


HEADING_PATTERN = re.compile(r"<h([1-6])\b([^>]*)>(.*?)</h\1>", re.IGNORECASE | re.DOTALL)
TABLE_PATTERN = re.compile(r"<table\b([^>]*)>(.*?)</table>", re.IGNORECASE | re.DOTALL)
TH_PATTERN = re.compile(r"<th\b[^>]*>(.*?)</th>", re.IGNORECASE | re.DOTALL)
TAG_PATTERN = re.compile(r"<[^>]+>")
SPACE_PATTERN = re.compile(r"\s+")

TABLE_CLASSES = {
    ("field", "value"): "table-kv",
    ("term", "definition"): "table-definitions",
    ("area", "requested configuration"): "table-kv",
    ("req id", "priority", "requirement statement"): "table-requirements",
    ("requirement group", "expected evidence"): "table-kv",
    ("id", "type", "description", "owner"): "table-open-items",
    ("version", "date", "author", "summary of change"): "table-revision-history",
}

HEADING_CLASSES = {
    "revision history": "section-revision-history",
}


def normalize_text(fragment: str) -> str:
    text = TAG_PATTERN.sub(" ", fragment)
    text = html.unescape(text)
    text = SPACE_PATTERN.sub(" ", text).strip().lower()
    text = re.sub(r"^\d+(?:\.\d+)*\.?\s+", "", text)
    return text


def add_class(attrs: str, class_name: str) -> str:
    match = re.search(r'class=(["\'])(.*?)\1', attrs, flags=re.IGNORECASE | re.DOTALL)
    if match:
        existing = match.group(2).split()
        if class_name not in existing:
            existing.append(class_name)
        merged = " ".join(existing)
        return attrs[: match.start(2)] + merged + attrs[match.end(2) :]
    return f'{attrs} class="{class_name}"'


def classify_heading(match: re.Match[str]) -> str:
    level, attrs, inner = match.groups()
    heading_text = normalize_text(inner)
    class_name = HEADING_CLASSES.get(heading_text)
    if not class_name:
        return match.group(0)
    return f"<h{level}{add_class(attrs, class_name)}>{inner}</h{level}>"


def classify_table(match: re.Match[str]) -> str:
    attrs, inner = match.groups()
    headers = tuple(normalize_text(header) for header in TH_PATTERN.findall(inner))
    class_name = TABLE_CLASSES.get(headers)
    if not class_name:
        return match.group(0)
    return f"<table{add_class(attrs, class_name)}>{inner}</table>"


def main() -> int:
    if len(sys.argv) != 2:
        print("Usage: postprocess_html.py <file.html>", file=sys.stderr)
        return 2

    path = pathlib.Path(sys.argv[1])
    contents = path.read_text(encoding="utf-8")
    contents = re.sub(r"<colgroup>.*?</colgroup>\s*", "", contents, flags=re.IGNORECASE | re.DOTALL)
    contents = HEADING_PATTERN.sub(classify_heading, contents)
    contents = TABLE_PATTERN.sub(classify_table, contents)
    path.write_text(contents, encoding="utf-8")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
