import unittest
from furry_tool.docx_ops.pdf2docx import pdf2docx


class Test_docx_ops(unittest.TestCase):
    def test_save_docx(self):
        pdf_file = '/path/to/sample.pdf'
        docx_file = 'path/to/sample.docx'
        pdf2docx(pdf_file,docx_file)


unittest.main()