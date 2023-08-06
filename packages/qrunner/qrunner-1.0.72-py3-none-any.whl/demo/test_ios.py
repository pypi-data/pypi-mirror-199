import qrunner
from qrunner import IosElem


class HomePage(qrunner.Page):
    """APP首页"""
    my_entry = IosElem(text='我的', desc='我的入口')


class TestSearch(qrunner.TestCase):
    """搜索无人机"""

    def start(self):
        self.page = HomePage(self.driver)

    def test_pom(self):
        self.page.my_entry.click()
        self.sleep(10)


if __name__ == '__main__':
    qrunner.main(
        platform='ios',
        device_id='00008101-000E646A3C29003A',
        pkg_name='com.qizhidao.company'
    )
