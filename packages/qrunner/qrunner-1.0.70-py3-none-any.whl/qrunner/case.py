import re
import time
from typing import Union

import jmespath
from jsonschema import validate
from jsonschema.exceptions import ValidationError

from qrunner.core.android.driver import AndroidDriver
from qrunner.core.android.element import AdrElem
from qrunner.core.api.request import HttpRequest, ResponseResult, formatting
from qrunner.core.ios.driver import IosDriver
from qrunner.core.ios.element import IosElem
from qrunner.core.web.driver import WebDriver
from qrunner.core.web.element import WebElem
from qrunner.utils.config import config
from qrunner.utils.log import logger
from qrunner.running.config import Qrunner
from qrunner.utils.exceptions import PlatformError, NoSuchDriverType, ElementNameEmptyException


class TestCase(HttpRequest):
    """
    测试用例基类，所有测试用例需要继承该类
    """

    driver: Union[AndroidDriver, IosDriver, WebDriver] = None

    # ---------------------初始化-------------------------------
    def start_class(self):
        """
        Hook method for setup_class fixture
        :return:
        """
        pass

    def end_class(self):
        """
        Hook method for teardown_class fixture
        :return:
        """
        pass

    @classmethod
    def setup_class(cls):
        cls.driver = Qrunner.driver
        if config.get_platform() == 'web':
            cls.driver = WebDriver(config.get_browser())
        cls().start_class()

    @classmethod
    def teardown_class(cls):
        if isinstance(cls().driver, WebDriver):
            cls().driver.quit()
        cls().end_class()

    def start(self):
        """
        Hook method for setup_method fixture
        :return:
        """
        pass

    def end(self):
        """
        Hook method for teardown_method fixture
        :return:
        """
        pass

    def setup_method(self):
        self.start_time = time.time()
        if isinstance(self.driver, (AndroidDriver, IosDriver)):
            # self.driver.start_error_handler()
            self.driver.start_app()
        self.start()

    def teardown_method(self):
        self.end()
        if self.driver is not None:
            self.driver.screenshot_with_time('用例执行完成截图')
        if isinstance(self.driver, (AndroidDriver, IosDriver)):
            self.driver.stop_app()
        take_time = time.time() - self.start_time
        logger.debug("[run_time]: {:.2f} s".format(take_time))

    # 公共方法
    @staticmethod
    def sleep(n: float):
        """休眠"""
        logger.debug(f"等待: {n}s")
        time.sleep(n)

    # UI自动化
    def open(self, url=None):
        if self.driver:
            self.driver.open_url(url)
        else:
            raise NoSuchDriverType('Browser为空')

    def elem(self,
             res_id: str = None,
             class_name: str = None,
             text: str = None,
             name: str = None,
             label: str = None,
             value: str = None,
             id_: str = None,
             link_text: str = None,
             partial_link_text: str = None,
             tag_name: str = None,
             css: str = None,
             xpath: str = None,
             index: int = None,
             desc: str = None
             ):
        _kwargs = {}
        if res_id is not None:
            _kwargs["res_id"] = res_id
        if class_name is not None:
            _kwargs["class_name"] = class_name
        if text is not None:
            _kwargs["text"] = text
        if name is not None:
            _kwargs["name"] = name
        if label is not None:
            _kwargs["label"] = label
        if value is not None:
            _kwargs["value"] = value
        if id_ is not None:
            _kwargs["id_"] = id_
        if link_text is not None:
            _kwargs["link_text"] = link_text
        if partial_link_text is not None:
            _kwargs["partial_link_text"] = partial_link_text
        if tag_name is not None:
            _kwargs["tag_name"] = tag_name
        if css is not None:
            _kwargs["css"] = css
        if xpath is not None:
            _kwargs["xpath"] = xpath
        if index is not None:
            _kwargs["index"] = index
        if desc is None:
            raise ElementNameEmptyException("请设置控件名称")
        else:
            _kwargs["desc"] = desc

        """封装安卓、ios、web元素"""
        if isinstance(self.driver, AndroidDriver):
            return AdrElem(self.driver, **_kwargs)
        elif isinstance(self.driver, IosDriver):
            return IosElem(self.driver, **_kwargs)
        elif isinstance(self.driver, WebDriver):
            return WebElem(self.driver, **_kwargs)
        else:
            raise NoSuchDriverType('不支持的驱动类型')

    def assert_element(self, timeout=5, **kwargs):
        """断言元素存在"""
        logger.info(f'断言 元素 {kwargs} 存在')
        assert self.elem(**kwargs).exists(timeout=timeout)

    def assert_element_text(self, text, **kwargs):
        """断言元素文本"""
        _text = self.elem(**kwargs).text
        logger.info(f'断言 元素文本 {_text} 包含 {text}')
        assert text in _text

    def assert_in_page(self, expect_value, timeout=5):
        """断言页面包含文本"""
        for _ in range(timeout + 1):
            try:
                page_source = self.driver.page_content
                logger.info(f"断言: 页面内容 包含 {expect_value}")
                assert expect_value in page_source, f"页面内容不包含 {expect_value}"
                break
            except AssertionError:
                time.sleep(1)
        else:
            page_source = self.driver.page_content
            logger.info(f"断言: 页面内容 包含 {expect_value}")
            assert expect_value in page_source, f"页面内容不包含 {expect_value}"
        self.driver.screenshot_with_time(f'断言页面内容包含-{expect_value}')

    def is_in_page(self, expect_value, timeout=5):
        """页面是否包含文本"""
        self.sleep(timeout)
        page_source = self.driver.page_content
        self.driver.screenshot_with_time(f'判断页面内容是否包含-{expect_value}')
        return True if expect_value in page_source else False

    def assert_not_in_page(self, expect_value, timeout=5):
        """断言页面不包含文本"""
        for _ in range(timeout + 1):
            try:
                page_source = self.driver.page_content
                logger.info(f"断言: 页面内容 不包含 {expect_value}")
                assert expect_value not in page_source, f"页面内容不包含 {expect_value}"
                break
            except AssertionError:
                time.sleep(1)
        else:
            page_source = self.driver.page_content
            logger.info(f"断言: 页面内容 不包含 {expect_value}")
            assert expect_value not in page_source, f"页面内容仍然包含 {expect_value}"
        self.driver.screenshot_with_time(f'断言页面内容不包含-{expect_value}')

    def is_title(self, expect_value=None, timeout=5):
        """断言页面标题等于"""
        for _ in range(timeout + 1):
            title = self.driver.title
            if expect_value == title:
                return True
            self.sleep(1)
        else:
            return False

    def assert_title(self, expect_value=None, timeout=5):
        """断言页面标题等于"""
        for _ in range(timeout + 1):
            try:
                title = self.driver.title
                logger.info(f"断言: 页面标题 {title} 等于 {expect_value}")
                assert expect_value == title, f"页面标题 {title} 不等于 {expect_value}"
                break
            except AssertionError:
                time.sleep(1)
        else:
            title = self.driver.title
            logger.info(f"断言: 页面标题 {title} 等于 {expect_value}")
            assert expect_value == title, f"页面标题 {title} 不等于 {expect_value}"

    def is_in_title(self, expect_value=None, timeout=5):
        """断言页面标题等于"""
        for _ in range(timeout + 1):
            title = self.driver.title
            if expect_value in title:
                return True
            self.sleep(1)
        else:
            return False

    def assert_in_title(self, expect_value=None, timeout=5):
        """断言页面标题包含"""
        for _ in range(timeout + 1):
            try:
                title = self.driver.title
                logger.info(f"断言: 页面标题 {title} 包含 {expect_value}")
                assert expect_value in title, f"页面标题 {title} 不包含 {expect_value}"
                break
            except AssertionError:
                time.sleep(1)
        else:
            title = self.driver.title
            logger.info(f"断言: 页面标题 {title} 包含 {expect_value}")
            assert expect_value in title, f"页面标题 {title} 不包含 {expect_value}"

    def assert_url(self, expect_value=None, timeout=5):
        """断言页面url等于"""
        for _ in range(timeout + 1):
            try:
                url = self.driver.url
                logger.info(f"断言: 页面url {url} 等于 {expect_value}")
                assert expect_value == url, f"页面url {url} 不等于 {expect_value}"
                break
            except AssertionError:
                time.sleep(1)
        else:
            url = self.driver.url
            logger.info(f"断言: 页面url {url} 等于 {expect_value}")
            assert expect_value == url, f"页面url {url} 不等于 {expect_value}"

    def assert_in_url(self, expect_value=None, timeout=5):
        """断言页面url包含"""
        for _ in range(timeout + 1):
            try:
                url = self.driver.url
                logger.info(f"断言: 页面url {url} 包含 {expect_value}")
                assert expect_value in url, f"页面url {url} 不包含 {expect_value}"
                break
            except AssertionError:
                time.sleep(1)
        else:
            url = self.driver.url
            logger.info(f"断言: 页面url {url} 包含 {expect_value}")
            assert expect_value in url, f"页面url {url} 不包含 {expect_value}"

    def assert_alert_text(self, expect_value):
        """断言弹窗文本"""
        alert_text = self.driver.alert_text
        logger.info(f"断言: 弹窗文本 {alert_text} 等于 {expect_value}")
        assert expect_value == alert_text, f"弹窗文本 {alert_text} 等于 {expect_value}"

    # API专用方法
    @staticmethod
    def assert_status_code(status_code):
        """
        断言状态码
        """
        actual_code = ResponseResult.status_code
        logger.info(f"断言: {actual_code} 等于 {status_code}")
        assert (
                actual_code == status_code
        ), f"status_code {ResponseResult} != {status_code}"

    @staticmethod
    def assertStatusCode(status_code):
        """
        兼容历史版本
        """
        actual_code = ResponseResult.status_code
        logger.info(f"断言: {actual_code} 等于 {status_code}")
        assert (
                actual_code == status_code
        ), f"status_code {ResponseResult} != {status_code}"

    @staticmethod
    def assert_schema(schema, response=None) -> None:
        """
        Assert JSON Schema
        doc: https://json-schema.org/
        """
        logger.info(f"assertSchema -> {formatting(schema)}.")

        if response is None:
            response = ResponseResult.response

        try:
            validate(instance=response, schema=schema)
        except ValidationError as msg:
            assert "Response data" == "Schema data", msg

    @staticmethod
    def assert_eq(path, value):
        """
        功能同assertPath，用于兼容历史代码
        doc: https://jmespath.org/
        """
        search_value = jmespath.search(path, ResponseResult.response)
        logger.info(f"断言: {search_value} 等于 {value}")
        assert search_value == value, f"{search_value} != {value}"

    @staticmethod
    def assertEq(path, value):
        """
        兼容历史版本
        """
        search_value = jmespath.search(path, ResponseResult.response)
        logger.info(f"断言: {search_value} 等于 {value}")
        assert search_value == value, f"{search_value} != {value}"

    @staticmethod
    def assertPath(path, value):
        """
        兼容历史版本，同assert_eq
        """
        search_value = jmespath.search(path, ResponseResult.response)
        logger.info(f"断言: {search_value} 等于 {value}")
        assert search_value == value, f"{search_value} != {value}"

    @staticmethod
    def assert_not_eq(path, value):
        """
        值不等于
        doc: https://jmespath.org/
        """
        search_value = jmespath.search(path, ResponseResult.response)
        logger.info(f"断言: {search_value} 不等于 {value}")
        assert search_value != value, f"{search_value} 等于 {value}"

    @staticmethod
    def assertNotEq(path, value):
        """
        兼容历史版本
        """
        search_value = jmespath.search(path, ResponseResult.response)
        logger.info(f"断言: {search_value} 不等于 {value}")
        assert search_value != value, f"{search_value} 等于 {value}"

    @staticmethod
    def assert_len_eq(path, value):
        """
        断言列表长度等于多少
        doc: https://jmespath.org/
        """
        search_value = jmespath.search(path, ResponseResult.response)
        logger.info(f"断言: {len(search_value)} 等于 {value}")
        assert len(search_value) == value, f"{search_value} 的长度不等于 {value}"

    @staticmethod
    def assertLenEq(path, value):
        """
        兼容历史版本
        """
        search_value = jmespath.search(path, ResponseResult.response)
        logger.info(f"断言: {len(search_value)} 等于 {value}")
        assert len(search_value) == value, f"{search_value} 的长度不等于 {value}"

    @staticmethod
    def assert_len_gt(path, value):
        """
        断言列表长度大于多少
        doc: https://jmespath.org/
        """
        search_value = jmespath.search(path, ResponseResult.response)
        logger.info(f"断言: {len(search_value)} 大于 {value}")
        assert len(search_value) > value, f"{search_value} 的长度不大于 {value}"

    @staticmethod
    def assertLenGt(path, value):
        """
        兼容历史版本
        """
        search_value = jmespath.search(path, ResponseResult.response)
        logger.info(f"断言: {len(search_value)} 大于 {value}")
        assert len(search_value) > value, f"{search_value} 的长度不大于 {value}"

    @staticmethod
    def assert_len_gt_or_eq(path, value):
        """
        断言列表长度大于等于多少
        doc: https://jmespath.org/
        """
        search_value = jmespath.search(path, ResponseResult.response)
        logger.info(f"断言: {len(search_value)} 大于等于 {value}")
        assert len(search_value) >= value, f"{search_value} 的长度不大于 {value}"

    @staticmethod
    def assertLenGtOrEq(path, value):
        """
        兼容历史版本
        """
        search_value = jmespath.search(path, ResponseResult.response)
        logger.info(f"断言: {len(search_value)} 大于等于 {value}")
        assert len(search_value) >= value, f"{search_value} 的长度不大于 {value}"

    @staticmethod
    def assert_len_lt(path, value):
        """
        断言列表长度小于多少
        doc: https://jmespath.org/
        """
        search_value = jmespath.search(path, ResponseResult.response)
        logger.info(f"断言: {len(search_value)} 小于 {value}")
        assert len(search_value) < value, f"{search_value} 的长度不大于 {value}"

    @staticmethod
    def assertLenLt(path, value):
        """
        兼容历史版本
        """
        search_value = jmespath.search(path, ResponseResult.response)
        logger.info(f"断言: {len(search_value)} 小于 {value}")
        assert len(search_value) < value, f"{search_value} 的长度不大于 {value}"

    @staticmethod
    def assert_len_lt_or_eq(path, value):
        """
        断言列表长度小于等于多少
        doc: https://jmespath.org/
        """
        search_value = jmespath.search(path, ResponseResult.response)
        logger.info(f"断言: {len(search_value)} 小于等于 {value}")
        assert len(search_value) <= value, f"{search_value} 的长度不大于 {value}"

    @staticmethod
    def assertLenLtOrEq(path, value):
        """
        兼容历史版本
        """
        search_value = jmespath.search(path, ResponseResult.response)
        logger.info(f"断言: {len(search_value)} 小于等于 {value}")
        assert len(search_value) <= value, f"{search_value} 的长度不大于 {value}"

    @staticmethod
    def assert_gt(path, value):
        """
        值大于多少
        doc: https://jmespath.org/
        """
        search_value = jmespath.search(path, ResponseResult.response)
        if isinstance(search_value, str):
            if "." in search_value:
                search_value = float(search_value)
            else:
                search_value = int(search_value)
        logger.info(f"断言: {search_value} 大于 {value}")
        assert search_value > value, f"{search_value} 不大于 {value}"

    @staticmethod
    def assertGt(path, value):
        """
        兼容历史版本
        """
        search_value = jmespath.search(path, ResponseResult.response)
        if isinstance(search_value, str):
            if "." in search_value:
                search_value = float(search_value)
            else:
                search_value = int(search_value)
        logger.info(f"断言: {search_value} 大于 {value}")
        assert search_value > value, f"{search_value} 不大于 {value}"

    @staticmethod
    def assert_gt_or_eq(path, value):
        """
        值大于等于
        doc: https://jmespath.org/
        """
        search_value = jmespath.search(path, ResponseResult.response)
        if isinstance(search_value, str):
            if "." in search_value:
                search_value = float(search_value)
            else:
                search_value = int(search_value)
        logger.info(f"断言: {search_value} 大于等于 {value}")
        assert search_value >= value, f"{search_value} 小于 {value}"

    @staticmethod
    def assertGtOrEq(path, value):
        """
        兼容历史版本
        """
        search_value = jmespath.search(path, ResponseResult.response)
        if isinstance(search_value, str):
            if "." in search_value:
                search_value = float(search_value)
            else:
                search_value = int(search_value)
        logger.info(f"断言: {search_value} 大于等于 {value}")
        assert search_value >= value, f"{search_value} 小于 {value}"

    @staticmethod
    def assert_lt(path, value):
        """
        值小于多少
        doc: https://jmespath.org/
        """
        search_value = jmespath.search(path, ResponseResult.response)
        if isinstance(search_value, str):
            if "." in search_value:
                search_value = float(search_value)
            else:
                search_value = int(search_value)
        logger.info(f"断言: {search_value} 小于 {value}")
        assert search_value < value, f"{search_value} 不大于 {value}"

    @staticmethod
    def assertLt(path, value):
        """
        兼容历史版本
        """
        search_value = jmespath.search(path, ResponseResult.response)
        if isinstance(search_value, str):
            if "." in search_value:
                search_value = float(search_value)
            else:
                search_value = int(search_value)
        logger.info(f"断言: {search_value} 小于 {value}")
        assert search_value < value, f"{search_value} 不大于 {value}"

    @staticmethod
    def assert_lt_or_eq(path, value):
        """
        值小于等于多少
        doc: https://jmespath.org/
        """
        search_value = jmespath.search(path, ResponseResult.response)
        if isinstance(search_value, str):
            if "." in search_value:
                search_value = float(search_value)
            else:
                search_value = int(search_value)
        logger.info(f"断言: {search_value} 小于等于 {value}")
        assert search_value <= value, f"{search_value} 不大于 {value}"

    @staticmethod
    def assertLtOrEq(path, value):
        """
        兼容历史版本
        """
        search_value = jmespath.search(path, ResponseResult.response)
        if isinstance(search_value, str):
            if "." in search_value:
                search_value = float(search_value)
            else:
                search_value = int(search_value)
        logger.info(f"断言: {search_value} 小于等于 {value}")
        assert search_value <= value, f"{search_value} 不大于 {value}"

    @staticmethod
    def assert_range(path, start, end):
        """值在(start, end)范围内
        doc: https://jmespath.org/
        """
        search_value = jmespath.search(path, ResponseResult.response)
        if isinstance(search_value, str):
            if "." in search_value:
                search_value = float(search_value)
            else:
                search_value = int(search_value)
        logger.info(f"断言: {search_value} 在 [{start}, {end}] 范围内")
        assert (search_value >= start) & (
                search_value <= end
        ), f"{search_value} 不在[{start}, {end}]范围内"

    @staticmethod
    def assertRange(path, start, end):
        """兼容历史版本
        """
        search_value = jmespath.search(path, ResponseResult.response)
        if isinstance(search_value, str):
            if "." in search_value:
                search_value = float(search_value)
            else:
                search_value = int(search_value)
        logger.info(f"断言: {search_value} 在 [{start}, {end}] 范围内")
        assert (search_value >= start) & (
                search_value <= end
        ), f"{search_value} 不在[{start}, {end}]范围内"

    @staticmethod
    def assert_in(path, value):
        """
        断言匹配结果被value_list包含
        doc: https://jmespath.org/
        """
        search_value = jmespath.search(path, ResponseResult.response)
        logger.info(f"断言: {search_value} 被 {value} 包含")
        assert search_value in value, f"{value} 不包含 {search_value}"

    @staticmethod
    def assertIn(path, value):
        """
        兼容历史版本
        """
        search_value = jmespath.search(path, ResponseResult.response)
        logger.info(f"断言: {search_value} 被 {value} 包含")
        assert search_value in value, f"{value} 不包含 {search_value}"

    @staticmethod
    def assert_not_in(path, value):
        """
        断言匹配结果不被value_list包含
        doc: https://jmespath.org/
        """
        search_value = jmespath.search(path, ResponseResult.response)
        logger.info(f"断言: {search_value} 不被 {value} 包含")
        assert search_value not in value, f"{value} 包含 {search_value}"

    @staticmethod
    def assertNotIn(path, value):
        """
        兼容历史版本
        """
        search_value = jmespath.search(path, ResponseResult.response)
        logger.info(f"断言: {search_value} 不被 {value} 包含")
        assert search_value not in value, f"{value} 包含 {search_value}"

    @staticmethod
    def assert_not_exists(path):
        """断言字段不存在"""
        search_value = jmespath.search(path, ResponseResult.response)
        logger.info(f"断言: {path} 不存在或值为None")
        assert search_value is None, f"仍然包含 {path} 为 {search_value}"

    @staticmethod
    def assertNotExists(path):
        """兼容历史版本"""
        search_value = jmespath.search(path, ResponseResult.response)
        logger.info(f"断言: {path} 不存在或值为None")
        assert search_value is None, f"仍然包含 {path} 为 {search_value}"

    @staticmethod
    def assert_contain(path, value):
        """
        断言匹配结果包含value
        doc: https://jmespath.org/
        """
        search_value = jmespath.search(path, ResponseResult.response)
        logger.info(f"断言: {search_value} 包含 {value}")
        assert value in search_value, f"{search_value} 不包含 {value}"

    @staticmethod
    def assertContain(path, value):
        """
        兼容历史版本
        """
        search_value = jmespath.search(path, ResponseResult.response)
        logger.info(f"断言: {search_value} 包含 {value}")
        assert value in search_value, f"{search_value} 不包含 {value}"

    @staticmethod
    def assert_not_contain(path, value):
        """
        断言匹配结果不包含value
        doc: https://jmespath.org/
        """
        search_value = jmespath.search(path, ResponseResult.response)
        logger.info(f"断言: {search_value} 不包含 {value}")
        assert value not in search_value, f"{search_value} 包含 {value}"

    @staticmethod
    def assertNotContain(path, value):
        """
        兼容历史版本
        """
        search_value = jmespath.search(path, ResponseResult.response)
        logger.info(f"断言: {search_value} 不包含 {value}")
        assert value not in search_value, f"{search_value} 包含 {value}"

    @staticmethod
    def assert_type_match(path, value_type):
        """
        类型匹配
        doc: https://jmespath.org/
        """
        if not isinstance(value_type, type):
            if value_type == "int":
                value_type = int
            elif value_type == "str":
                value_type = str
            elif value_type == "list":
                value_type = list
            elif value_type == "dict":
                value_type = dict
            else:
                value_type = str

        search_value = jmespath.search(path, ResponseResult.response)
        logger.info(f"断言: {search_value} 是 {value_type} 类型")
        assert isinstance(
            search_value, value_type
        ), f"{search_value} 不是 {value_type} 类型"

    @staticmethod
    def assertTypeMatch(path, value_type):
        """
        兼容历史版本
        """
        if not isinstance(value_type, type):
            if value_type == "int":
                value_type = int
            elif value_type == "str":
                value_type = str
            elif value_type == "list":
                value_type = list
            elif value_type == "dict":
                value_type = dict
            else:
                value_type = str

        search_value = jmespath.search(path, ResponseResult.response)
        logger.info(f"断言: {search_value} 是 {value_type} 类型")
        assert isinstance(
            search_value, value_type
        ), f"{search_value} 不是 {value_type} 类型"

    @staticmethod
    def assert_starts_with(path, value):
        """
        以什么开头
        doc: https://jmespath.org/
        """
        search_value: str = jmespath.search(path, ResponseResult.response)
        logger.info(f"断言: {search_value} 以 {value} 开头")
        assert search_value.startswith(value), f"{search_value} 不以 {value} 开头"

    @staticmethod
    def assertStartsWith(path, value):
        """
        兼容历史版本
        """
        search_value: str = jmespath.search(path, ResponseResult.response)
        logger.info(f"断言: {search_value} 以 {value} 开头")
        assert search_value.startswith(value), f"{search_value} 不以 {value} 开头"

    @staticmethod
    def assert_ends_with(path, value):
        """
        以什么结尾
        doc: https://jmespath.org/
        """
        search_value: str = jmespath.search(path, ResponseResult.response)
        logger.info(f"断言: {search_value} 以 {value} 结尾")
        assert search_value.endswith(value), f"{search_value} 不以 {value} 结尾"

    @staticmethod
    def assertEndsWith(path, value):
        """
        兼容历史版本
        """
        search_value: str = jmespath.search(path, ResponseResult.response)
        logger.info(f"断言: {search_value} 以 {value} 结尾")
        assert search_value.endswith(value), f"{search_value} 不以 {value} 结尾"

    @staticmethod
    def assert_regex_match(path, value):
        """
        正则匹配
        doc: https://jmespath.org/
        """
        search_value = jmespath.search(path, ResponseResult.response)
        match_obj = re.match(r"" + value, search_value, flags=re.I)
        logger.info(f"断言: {search_value} 匹配正则表达式 {value} 成功")
        assert match_obj is not None, f"结果 {search_value} 匹配失败"

    @staticmethod
    def assertRegexMatch(path, value):
        """同assert_regex_match，兼容历史版本"""
        search_value = jmespath.search(path, ResponseResult.response)
        match_obj = re.match(r"" + value, search_value, flags=re.I)
        logger.info(f"断言: {search_value} 匹配正则表达式 {value} 成功")
        assert match_obj is not None, f"结果 {search_value} 匹配失败"
