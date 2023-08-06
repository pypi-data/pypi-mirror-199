# @Time    : 2022/2/22 9:35
# @Author  : kang.yang@qizhidao.com
# @File    : request.py
import json as json_util
import logging
from requests.packages import urllib3
from urllib import parse

import requests

from qrunner.utils.config import config
from qrunner.utils.log import logger

# 去掉requests本身的日志
urllib3_logger = logging.getLogger("urllib3")
urllib3_logger.setLevel(logging.CRITICAL)

# 去掉不设置证书的报警
urllib3.disable_warnings()


def formatting(msg):
    """formatted message"""
    if isinstance(msg, dict):
        return json_util.dumps(msg, indent=2, ensure_ascii=False)
    return msg


def request(func):
    def wrapper(*args, **kwargs):
        logger.info("-------------- Request -----------------[🚀]")
        # 给接口带上默认域名
        # 从配置文件中读取域名
        host = config.get_host()
        # 如果接口路径不以http开头，把域名写到key为url的位置参数中或者第一个参数中
        if "url" in kwargs:
            path: str = kwargs.get("url", "")
            if not path.startswith('http'):
                url = parse.urljoin(host, path)
                kwargs["url"] = url
            else:
                url = path
        else:
            path = list(args)[1]
            if not path.startswith('http'):
                url = parse.urljoin(host, path)
                args_list = list(args)
                args_list[1] = url
                args = tuple(args_list)
            else:
                url = path

        # 请求头处理，写入登录态
        # 从配置文件获取登录用户和游客的请求头
        if kwargs.get("login", True):
            login_header: dict = config.get_login()
        else:
            login_header: dict = config.get_visit()
        # 把用例脚本中设置的请求头加进来
        header_user_set = kwargs.pop("headers", {})
        login_header.update(header_user_set)
        # 把组装好的请求头装回到kwargs当中
        kwargs["headers"] = login_header

        # 设置默认超时时间
        timeout_config = config.get_timeout()  # 配置文件中的默认超时时间
        timeout_user_set = kwargs.pop("timeout", None)  # 用例脚本中设置的超时时间
        if timeout_user_set:
            kwargs["timeout"] = timeout_user_set
        else:
            kwargs["timeout"] = timeout_config

        # 发送请求
        r = func(*args, **kwargs)

        # 输出请求参数日志
        logger.debug("[method]: {m}      [url]: {u}".format(m=func.__name__.upper(), u=url))
        auth = kwargs.get("auth", "")
        if auth:
            logger.debug(f"[auth]:\n {formatting(auth)}")
        logger.debug(f"[headers]:\n {formatting(dict(r.request.headers))}")
        cookies = kwargs.get("cookies", "")
        if cookies:
            logger.debug(f"[cookies]:\n {formatting(cookies)}")
        params = kwargs.get("params", "")
        if params:
            logger.debug(f"[params]:\n {formatting(params)}")
        data = kwargs.get("data", "")
        if data:
            logger.debug(f"[data]:\n {formatting(data)}")
        json = kwargs.get("json", "")
        if json:
            logger.debug(f"[json]:\n {formatting(json)}")

        # 保存响应结果并输出日志
        status_code = r.status_code
        headers = r.headers
        content_type = headers.get("Content-Type")
        ResponseResult.status_code = status_code
        logger.info("-------------- Response ----------------")
        logger.debug(f"[status]: {status_code}")
        logger.debug(f"[headers]: {formatting(headers)}")
        try:
            resp = r.json()
            logger.debug(f"[type]: json")
            logger.debug(f"[response]:\n {formatting(resp)}")
            ResponseResult.response = resp
        except Exception:
            # 非json响应数据，根据响应内容类型进行判断
            if content_type is not None:
                if "text" not in content_type:
                    logger.debug(f"[type]: {content_type}")
                    logger.debug(f"[response]:\n {r.content}")
                    ResponseResult.response = r.content
                else:
                    logger.debug(f"[type]: {content_type}")
                    logger.debug(f"[response]:\n {r.text}")
                    ResponseResult.response = r.text
            else:
                logger.debug('ContentType为空，响应异常！！！')
                ResponseResult.response = r.text

    return wrapper


class ResponseResult:
    status_code = 200
    response = None


class HttpRequest(object):
    @request
    def get(self, url, params=None, verify=False, login=True, **kwargs):
        return requests.get(url, params=params, verify=verify, **kwargs)

    @request
    def post(self, url, data=None, json=None, verify=False, login=True, **kwargs):
        return requests.post(url, data=data, json=json, verify=verify, **kwargs)

    @request
    def put(self, url, data=None, json=None, verify=False, login=True, **kwargs):
        if json is not None:
            data = json_util.dumps(json)
        return requests.put(url, data=data, verify=verify, **kwargs)

    @request
    def delete(self, url, verify=False, login=True, **kwargs):
        return requests.delete(url, verify=verify, **kwargs)

    @property
    def response(self):
        """
        Returns the result of the response
        :return: response
        """
        return ResponseResult.response

