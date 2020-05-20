#获得pdf词频
import sys
import importlib
importlib.reload(sys) #

import jieba  #Python 中文分词组件(好用)

from pdfminer.pdfparser import PDFParser, PDFDocument
from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.converter import PDFPageAggregator
from pdfminer.layout import LTTextBoxHorizontal, LAParams
from pdfminer.pdfinterp import PDFTextExtractionNotAllowed

def readPDF(path):
    s = ""
    # 以二进制形式打开pdf文件
    with open(path, "rb") as f:
        # 创建一个pdf文档分析器
        parser = PDFParser(f)
        # 创建pdf文档
        pdfFile = PDFDocument()
        # 链接分析器与文档对象
        parser.set_document(pdfFile)
        pdfFile.set_parser(parser)
        # 提供初始化密码
        pdfFile.initialize()
        # 检测文档是否提供txt转换
    if not pdfFile.is_extractable:
        raise PDFTextExtractionNotAllowed
    else:
        # 解析数据
        # 数据管理
        manager = PDFResourceManager()
        # 创建一个PDF设备对象
        laparams = LAParams()
        device = PDFPageAggregator(manager, laparams=laparams)
        # 解释器对象
        interpreter = PDFPageInterpreter(manager, device)

        # 开始循环处理，每次处理一页
        for page in pdfFile.get_pages():
            interpreter.process_page(page)
            layout = device.get_result()
            for x in layout:
                if (isinstance(x, LTTextBoxHorizontal)):
                    s += x.get_text()
    return s.replace("\n", "")


path = r"attach/test.pdf"
s = readPDF(path)
s = jieba.cut(s, cut_all=False)
d = {}
for i in s:
    try:
        d[i] = d[i] + 1
    except KeyError:
        d[i] = 1
print(d)
file = open("3.txt", "w",encoding='utf-8')
file.write(str(d))
file.close()

input("程序运行完成，请按回车退出~")





