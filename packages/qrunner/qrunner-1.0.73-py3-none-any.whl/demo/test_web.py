import qrunner
from qrunner import WebElem


class PatentPage(qrunner.Page):
    """查专利首页"""
    search_input = WebElem(id_='driver-home-step1', desc='查专利首页输入框')
    search_submit = WebElem(id_='driver-home-step2', desc='查专利首页搜索确认按钮')


class TestPatentSearch(qrunner.TestCase):
    """搜索无人机"""

    def start(self):
        """页面和元素初始化"""
        self.page = PatentPage(self.driver)

    def test_pom(self):
        """pom模式代码"""
        self.driver.open_url()
        self.page.search_input.set_text('无人机')
        self.page.search_submit.click()
        self.assert_in_page('王刚毅')


if __name__ == '__main__':
    qrunner.main(
        platform='web',
        base_url='https://patents.qizhidao.com/'
    )
