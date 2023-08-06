import qrunner


class TestSearch(qrunner.TestCase):

    def test_normal(self):
        self.elem(text='我的', desc='我的入口').click()
        self.elem(text='settings navi', desc='设置入口').click()
        self.assert_in_page('设置')


if __name__ == '__main__':
    # 连接本地设备
    qrunner.main(
        platform='ios',
        device_id='00008101-000E646A3C29003A',
        pkg_name='com.qizhidao.company'
    )

