import qrunner
from qrunner import WebElem


class PatentPage(qrunner.Page):
    """查专利首页"""
    search_input = WebElem(id_='driver-home-step1', desc='查专利首页输入框')
    search_submit = WebElem(id_='driver-home-step2', desc='查专利首页搜索确认按钮')