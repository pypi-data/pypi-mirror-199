import qrunner
from qrunner import IosElem
from qrunner.core.image.element import ImageElem


class HomePage(qrunner.Page):
    """APP首页"""
    ad_close = IosElem(label='close white big', desc='广告关闭按钮')
    patent_entry = IosElem(text='查专利', desc='查专利入口')


class PatentSearch(qrunner.Page):
    """查专利"""
    report_entry = ImageElem(image='tpl1678093612402.png', desc='分析报告')


class TestSearch(qrunner.TestCase):
    """搜索无人机"""

    def start(self):
        self.hp = HomePage(self.driver)
        self.ps = PatentSearch(self.driver)

    def test_pom(self):
        self.hp.ad_close.click_exists()
        self.hp.patent_entry.click()
        self.ps.report_entry.click()
        self.sleep(10)


if __name__ == '__main__':
    qrunner.main(
        platform='ios',
        device_id='00008101-000E646A3C29003A',
        pkg_name='com.qizhidao.company'
    )
