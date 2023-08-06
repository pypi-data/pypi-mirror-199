from htmldocx import HtmlToDocx
from docx2pdf import convert

import tempfile
import os

def main(url, pdf):
	with tempfile.TemporaryDirectory() as tmpdir:
		docx = os.path.join(tmpdir, "a.docx")
		new_parser = HtmlToDocx()
		new_parser.parse_html_file(url, docx)
		convert(docx, pdf)

