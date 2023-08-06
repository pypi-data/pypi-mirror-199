import os

from docxtpl import DocxTemplate

BASE_DIR = os.path.dirname(__file__)


class docx_ops:
    def __init__(self, path: str):
        # path = os.path.join(BASE_DIR, r'templates\hzxy.docx')
        # path = r'./templates/hzxy.docx'
        self.doc = DocxTemplate(path)

    def save_doc(self, path: str, context):
        self.doc.render(context)
        self.doc.save(path)
