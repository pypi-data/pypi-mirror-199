from page.web_page import PatentPage


class PatentFunc:

    def __init__(self, driver):
        self.page = PatentPage(driver)

    def search(self, keyword):
        self.page.search_input.set_text(keyword)
        self.page.search_submit.click()
