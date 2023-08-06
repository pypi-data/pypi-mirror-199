import qrunner


@qrunner.module("PC首页")
class TestGetToolCardListForPc(qrunner.TestCase):

    def test_getToolCardListForPc(self):
        """获取金刚位"""
        payload = {"type": 2}
        self.post('/qzd-bff-app/qzd/v1/home/getToolCardListForPc', json=payload)
        self.assert_eq('code', 0)


if __name__ == '__main__':
    qrunner.main(
        host='https://app-pre.qizhidao.com',
        path='test_api.py::TestGetToolCardListForPc::test_getToolCardListForPc'
    )
