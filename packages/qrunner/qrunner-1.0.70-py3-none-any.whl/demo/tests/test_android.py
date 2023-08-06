import qrunner

from page.adr_page import HomePage


class TestSearch(qrunner.TestCase):
    """进入我的页"""

    def start(self):
        self.page = HomePage(self.driver)

    def test_pom(self):
        self.page.my_entry.click()
        self.page.setting_entry.click()
        self.assert_in_page('设置')


if __name__ == '__main__':
    # 连接本地设备
    qrunner.main(
        platform='android',
        device_id='UJK0220521066836',
        pkg_name='com.qizhidao.clientapp'
    )

