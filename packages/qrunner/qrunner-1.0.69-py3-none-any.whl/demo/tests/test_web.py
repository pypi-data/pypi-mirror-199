import qrunner

from page.web_page import PatentPage


class TestPatentSearch(qrunner.TestCase):

    def start(self):
        self.page = PatentPage(self.driver)

    def test_pom(self):
        """pom模式代码"""
        self.open()
        keyword = '无人机'
        self.page.search_input.set_text(keyword)
        self.page.search_submit.click()
        self.assert_element_text(keyword,
                                 xpath='//*[@id="searchResultContentviewID"]/div[1]/div[1]/div[1]/div[2]/div/a/span',
                                 desc='第一条检索结果的标题')


if __name__ == '__main__':
    qrunner.main(
        platform='web',
        host='https://patents.qizhidao.com/'
    )
