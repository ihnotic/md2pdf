import subprocess
import sys
import tempfile
import textwrap
import unittest
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parent.parent
POSTPROCESS = REPO_ROOT / "share" / "md2pdf-vscode" / "postprocess_html.py"


class PostprocessHtmlTests(unittest.TestCase):
    def test_classifies_known_tables_and_sections(self) -> None:
        sample = textwrap.dedent(
            """\
            <html>
              <body>
                <h2 id="revision-history">8. Revision History</h2>
                <table>
                  <colgroup><col style="width: 25%" /></colgroup>
                  <thead>
                    <tr>
                      <th>Version</th>
                      <th>Date</th>
                      <th>Author</th>
                      <th>Summary Of Change</th>
                    </tr>
                  </thead>
                </table>
                <h2 id="open-items-assumptions">7. Open Items / Assumptions</h2>
                <table>
                  <thead>
                    <tr>
                      <th>ID</th>
                      <th>Type</th>
                      <th>Description</th>
                      <th>Owner</th>
                    </tr>
                  </thead>
                </table>
              </body>
            </html>
            """
        )

        with tempfile.TemporaryDirectory() as tmpdir:
            html_path = Path(tmpdir) / "sample.html"
            html_path.write_text(sample, encoding="utf-8")
            subprocess.run([sys.executable, str(POSTPROCESS), str(html_path)], check=True)
            output = html_path.read_text(encoding="utf-8")

        self.assertIn('class="section-revision-history"', output)
        self.assertIn('class="table-revision-history"', output)
        self.assertIn('class="table-open-items"', output)
        self.assertNotIn("<colgroup>", output)


if __name__ == "__main__":
    unittest.main()
