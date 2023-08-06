import unittest
from furry_tool.docx_ops.docx_template import docx_ops


class Test_docx_ops(unittest.TestCase):
    def test_save_docx(self):
        template_path = r'./template/template.docx'
        save_path = r'./output/target.docx'
        context = {
            'title': 'test_save_docx'
        }
        docx_ops(path=template_path).save_doc(path=save_path, context=context)


unittest.main()
