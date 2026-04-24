# md2pdf

Browser-style Markdown to PDF for technical documents.

`md2pdf` renders Markdown with `pandoc`, applies a small HTML postprocessor to fix common technical-document table layouts, then prints the result to PDF with headless Chrome. The output is meant to look closer to a browser/editor preview than a traditional typeset PDF engine.

## Why

- local and deterministic
- good-looking technical PDFs from plain Markdown
- sane table widths for requirements docs, open-items tables, and revision histories
- easy to automate from agents and shell scripts

## Requirements

- `pandoc`
- `python3`
- Google Chrome on macOS at `/Applications/Google Chrome.app/Contents/MacOS/Google Chrome`

You can override the Chrome path with `MD2PDF_CHROME_BIN=/path/to/chrome`.

## Install

```bash
./install.sh
```

By default this installs into `~/.local`:

- `~/.local/bin/md2pdf`
- `~/.local/bin/md2pdf-vscode`
- `~/.local/share/md2pdf-vscode/*`

To install somewhere else:

```bash
PREFIX=/usr/local ./install.sh
```

## Usage

Render next to the Markdown source:

```bash
md2pdf /path/to/file.md
```

Write to an explicit destination:

```bash
md2pdf --output /path/to/file.pdf /path/to/file.md
```

Keep the generated HTML for debugging:

```bash
md2pdf --html-output /tmp/file.html /path/to/file.md
```

## Validation

For important exports, validate the real PDF rather than only the HTML:

```bash
pdfinfo /path/to/file.pdf
pdftoppm -png -f 1 -l 1 /path/to/file.pdf /tmp/preview
```

## Layout model

The pipeline is:

1. Markdown to standalone HTML with `pandoc`
2. HTML cleanup and classification with `share/md2pdf-vscode/postprocess_html.py`
3. Browser-print styling from `share/md2pdf-vscode/vscode-gray-print.css`
4. PDF output from headless Chrome

The postprocessor strips Pandoc `colgroup` width hints and assigns table classes by header names. That lets the stylesheet keep `table-layout: auto` while still nudging specific technical tables into sane proportions.

## Development

Run the unit test for the postprocessor:

```bash
python3 -m unittest tests/test_postprocess.py
```
