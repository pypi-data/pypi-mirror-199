from qrunner.case import TestCase
from qrunner.page import Page
from qrunner.core.api.request import HttpRequest
from qrunner.core.android.element import AdrElem
from qrunner.core.ios.element import IosElem
from qrunner.core.web.element import WebElem
from qrunner.running.runner import main
from qrunner.utils.config import config
from qrunner.utils.decorate import *
from qrunner.utils.log import logger


__version__ = "1.0.69"
__description__ = "Api/Web/App端自动化测试框架"
