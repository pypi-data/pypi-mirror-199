from pdf2docx import Converter


def pdf2docx(pdf_file, docx_file):
    """
    pdf文件转docx文件
    :param pdf_file: pdf文件路径，如/path/to/sample.pdf
    :param docx_file: 要保存的docx文件路径，如path/to/sample.docx
    :return:
    """
    cv = Converter(pdf_file)
    cv.convert(docx_file, start=0, end=None)
    cv.close()
