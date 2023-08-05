# -*- coding: utf-8 -*-
import re
import time
import calendar
import datetime
from typing import List
from requests.utils import dict_from_cookiejar
from requests.cookies import RequestsCookieJar
from urllib.parse import urlparse, urljoin, quote, unquote, urlencode as urlencode_
from w3lib.url import canonicalize_url as canonicalize_url_


def canonicalize_url(url):
    """
    url 归一化 会参数排序 及去掉锚点
    """
    return canonicalize_url_(url)


def get_timestamp(timestamp=None, length=13) -> int:
    """

    :param timestamp: 1679555452.7439947
    :param length: 13
    :return: 1679555452743
    """
    if timestamp is None:
        timestamp = time.time()
    return int(str(timestamp).replace('.', '')[:length])


def get_datetime(datetime_=None, datetime_format="%Y-%m-%d %H:%M:%S") -> str:
    if datetime_ is None:
        datetime_ = datetime.datetime.now()
    return datetime_.strftime(datetime_format)


def get_date_number(year=None, month=None, day=None):
    """
    获取指定日期对应的日期数
    默认当前周
    :param year: 2023
    :param month: 3
    :param day: 23
    :return:  (年号，第几周，第几天) 如 (2010, 24, 3)
    """
    if year and month and day:
        return datetime.date(year, month, day).isocalendar()
    elif not any([year, month, day]):
        return datetime.datetime.now().isocalendar()
    else:
        assert year, "year 不能为空"
        assert month, "month 不能为空"
        assert day, "day 不能为空"


def get_between_date(begin_date, end_date=None, date_format="%Y-%m-%d", **time_interval):
    """
    获取一段时间间隔内的日期，默认为每一天
    :param begin_date: 开始日期 str 如 2018-10-01
    :param end_date: 默认为今日
    :param date_format: 日期格式，应与begin_date的日期格式相对应
    :param time_interval: 时间间隔 默认一天 支持 days、seconds、microseconds、milliseconds、minutes、hours、weeks
    :return: list 值为字符串
    """

    date_list = []

    begin_date = datetime.datetime.strptime(begin_date, date_format)
    end_date = (
        datetime.datetime.strptime(end_date, date_format)
        if end_date
        else datetime.datetime.strptime(
            time.strftime(date_format, time.localtime(time.time())), date_format
        )
    )
    time_interval = time_interval or dict(days=1)

    while begin_date <= end_date:
        date_str = begin_date.strftime(date_format)
        date_list.append(date_str)

        begin_date += datetime.timedelta(**time_interval)

    if end_date.strftime(date_format) not in date_list:
        date_list.append(end_date.strftime(date_format))

    return date_list


def get_between_months(begin_date, end_date=None):
    """
    获取一段时间间隔内的月份
    需要满一整月
    :param begin_date: 开始时间 如 2018-01-01
    :param end_date: 默认当前时间
    :return: 列表 如 ['2018-01', '2018-02']
    """

    def add_months(dt, months):
        month = dt.month - 1 + months
        year = dt.year + month // 12
        month = month % 12 + 1
        day = min(dt.day, calendar.monthrange(year, month)[1])
        return dt.replace(year=year, month=month, day=day)

    date_list = []
    begin_date = datetime.datetime.strptime(begin_date, "%Y-%m-%d")
    end_date = (
        datetime.datetime.strptime(end_date, "%Y-%m-%d")
        if end_date
        else datetime.datetime.strptime(
            time.strftime("%Y-%m-%d", time.localtime(time.time())), "%Y-%m-%d"
        )
    )
    while begin_date <= end_date:
        date_str = begin_date.strftime("%Y-%m")
        date_list.append(date_str)
        begin_date = add_months(begin_date, 1)
    return date_list


def quote_url(url, encoding="utf-8"):
    """
    URL 编码
    :param url: "https://www.baidu.com/s?wd=百度一下"
    :param encoding: "utf-8"
    :return: "https://www.baidu.com/s?wd=%E7%99%BE%E5%BA%A6%E4%B8%80%E4%B8%8B"
    """

    return quote(url, safe="%;/?:@&=+$,", encoding=encoding)


def unquote_url(url, encoding="utf-8"):
    """
    URL 解码
    :param url: "https://www.baidu.com/s?wd=%E7%99%BE%E5%BA%A6%E4%B8%80%E4%B8%8B"
    :param encoding: "utf-8"
    :return: "https://www.baidu.com/s?wd=百度一下"
    """

    return unquote(url, encoding=encoding)


def urlencode(params):
    """

    :param params: {'a': 1, 'b': 2}
    :return: "a=1&b=2"
    """
    return urlencode_(params)


def urldecode(url):
    """

    :param url: "xxx?a=1&b=2"
    :return: {'a': '1', 'b': '2'}
    """
    params_dict = dict()
    params = url.split("?")[-1].split("&")
    for param in params:
        key, value = param.split("=", 1)
        params_dict[key] = unquote_url(value)

    return params_dict


def get_param(url, key):
    """

    :param url: "https://www.baidu.com/s?wd=%E7%99%BE%E5%BA%A6%E4%B8%80%E4%B8%8B"
    :param key: "wd"
    :return: "百度一下"
    """
    match = re.search(f"{key}=([^&]+)", url)
    if match:
        return unquote_url(match.group(1))
    return None


def get_params(url):
    """

    :param url: "https://www.baidu.com/s?wd=%E7%99%BE%E5%BA%A6%E4%B8%80%E4%B8%8B"
    :return: {'wd': '百度一下'}
    """
    params_dict = {}
    params = url.split("?", 1)[-1].split("&")
    for param in params:
        key_value = param.split("=", 1)
        if len(key_value) == 2:
            params_dict[key_value[0]] = unquote_url(key_value[1])
        else:
            params_dict[key_value[0]] = ""

    return params_dict


def get_url_params(url):
    """

    :param url: "https://www.baidu.com/s?wd=%E7%99%BE%E5%BA%A6%E4%B8%80%E4%B8%8B"
    :return: ('https://www.baidu.com/s', {'wd': '百度一下'})
    """
    root_url = ""
    params = {}
    if "?" not in url:
        if re.search("[&=]", url) and not re.search("/", url):
            # 只有参数
            params = get_params(url)
        else:
            root_url = url

    else:
        root_url = url.split("?", 1)[0]
        params = get_params(url)

    return root_url, params


def join_url(root_url, sub_url):
    """

    :param root_url: "https://tieba.baidu.com/"
    :param sub_url: "/index.html"
    :return: "https://tieba.baidu.com/index.html"
    """
    return urljoin(root_url, sub_url)


def join_params(url, params):
    """

    :param url: "https://www.baidu.com/s?wd=百度一下"
    :param params: {'ie': 'utf-8'}
    :return: "https://www.baidu.com/s?wd=%E7%99%BE%E5%BA%A6%E4%B8%80%E4%B8%8B&ie=utf-8"
    """
    if not params:
        return url

    params = urlencode(params)
    separator = "?" if "?" not in url else "&"
    return quote_url(url + separator + params)


def get_cookies(response):
    """

    :param response: requests.get('https://www.baidu.com/')
    :return: {'BDORZ': '27315'}
    """
    cookies = dict_from_cookiejar(response.cookies)
    return cookies


def get_cookies_str2dict(cookie_str):
    """

    :param cookie_str: "key=value; key2=value2; key3=; key4="
    :return: {'key': 'value', 'key2': 'value2', 'key3': '', 'key4': ''}
    """
    cookies = {}
    for cookie in cookie_str.split(";"):
        cookie = cookie.strip()
        if not cookie:
            continue
        key, value = cookie.split("=", 1)
        key = key.strip()
        value = value.strip()
        cookies[key] = value

    return cookies


def get_cookies_jar_from_selenium_cookies(cookies: List[dict]):
    """
    requests.get(url, cookies=cookies_jar)
    :param cookies: [{},{}]
    :return: cookies_jar
    """
    cookies_jar = RequestsCookieJar()
    for cookie in cookies:
        if cookie.get("name"):
            cookies_jar.set(cookie["name"], cookie["value"])

    return cookies_jar


def get_cookies_dict_from_selenium_cookies(cookies: List[dict]):
    """
    requests.get(url, cookies=cookies_dict)
    :param cookies: [{},{}]
    :return: cookies_dict
    """
    cookies_dict = {}
    for cookie in cookies:
        if cookie.get("name"):
            cookies_dict[cookie["name"]] = cookie["value"]

    return cookies_dict


def cookies_jar2str(cookies):
    str_cookie = ""
    for k, v in dict_from_cookiejar(cookies).items():
        str_cookie += k
        str_cookie += "="
        str_cookie += v
        str_cookie += "; "
    return str_cookie


def cookies_dict2str(cookies):
    str_cookie = ""
    for k, v in cookies.items():
        str_cookie += k
        str_cookie += "="
        str_cookie += v
        str_cookie += "; "
    return str_cookie
