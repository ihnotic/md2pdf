#!/bin/bash
set -euo pipefail

prefix="${PREFIX:-$HOME/.local}"
repo_root="$(cd -- "$(dirname -- "$0")" && pwd)"

install -d "$prefix/bin" "$prefix/share/md2pdf-vscode"
install -m 755 "$repo_root/bin/md2pdf" "$prefix/bin/md2pdf"
install -m 644 "$repo_root/share/md2pdf-vscode/vscode-gray-print.css" "$prefix/share/md2pdf-vscode/vscode-gray-print.css"
install -m 755 "$repo_root/share/md2pdf-vscode/postprocess_html.py" "$prefix/share/md2pdf-vscode/postprocess_html.py"
ln -sf "$prefix/bin/md2pdf" "$prefix/bin/md2pdf-vscode"

printf 'Installed md2pdf to %s\n' "$prefix/bin/md2pdf"
