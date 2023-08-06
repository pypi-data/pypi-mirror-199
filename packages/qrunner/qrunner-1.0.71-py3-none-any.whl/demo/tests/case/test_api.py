import qrunner


class TestGetToolCardListForPc(qrunner.TestCase):
    """pc首页金刚位"""

    def test_getToolCardListForPc(self):
        """获取金刚位"""
        payload = {"type": 2}
        headers = {"user-agent-web": "X/b67aaff2200d4fc2a2e5a079abe78cc6"}
        self.post('/qzd-bff-app/qzd/v1/home/getToolCardListForPc', headers=headers, json=payload)
        self.assert_eq('code', 0)


if __name__ == '__main__':
    qrunner.main(host='https://app-pre.qizhidao.com')
