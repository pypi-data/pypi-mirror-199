# -*- coding: utf-8 -*-
"""日期/时间相关的字符串处理

"""

import contextlib
# 日期：Rola 2016.12.23

import datetime


def getToday():
    """
    返回当天日期的 %Y%m%d 格式的8位字符串
    :return:
    """
    return datetime.datetime.now().strftime('%Y%m%d')


def getYesterday():
    """
    返回昨天日期的 %Y%m%d 格式的8位字符串
    :return:
    """
    today = datetime.datetime.now().strftime('%Y%m%d')

    return addDays(today, -1)


def getTomorrow():
    """
    返回明天日期的 %Y%m%d 格式的8位字符串
    :return:
    """
    today = datetime.datetime.now().strftime('%Y%m%d')

    return addDays(today, 1)


def getNow():
    """
    获取当前时刻的字符串(格式为 %Y-%m-%d %H:%M:%S)
    :return:
    """
    return datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')


def getNowstr():
    """
    获取当前时刻的字符串(格式为 %Y%m%d%H%M%S)
    :return:
    """
    return datetime.datetime.now().strftime('%Y%m%d%H%M%S')


def convertToTime(strDate):
    """
    将 %Y%m%d 格式的8位字符串，转换为日期
    :param strDate: %Y%m%d 格式的8位日期字符串
    :return: datetime 类型的日期
    """
    date = datetime.datetime.now()  # 默认取当天日期

    with contextlib.suppress(Exception):
        if len(strDate) == 8:
            date = datetime.datetime.strptime(strDate, "%Y%m%d")
        elif len(strDate) == 10:
            date = datetime.datetime.strptime(strDate, "%Y%m%d%H")
        elif len(strDate) == 12:
            date = datetime.datetime.strptime(strDate, "%Y%m%d%H%M")
        elif len(strDate) == 14:
            date = datetime.datetime.strptime(strDate, "%Y%m%d%H%M%S")
    return date


def addDays(strDate, days):
    """
    在字符串日期上面增加天数
    :param strDate: %Y%m%d 格式的8位日期字符串
    :param days: 要增加的天数
    :return: 增加天数后的 %Y%m%d 格式的8位日期字符串
    """
    date = convertToTime(strDate)
    date_t = date + datetime.timedelta(days=int(days))

    return date_t.strftime('%Y%m%d')


def addTimes(strDate, days=0, hours=0, minutes=0, seconds=0):
    """
    在字符串日期上面增加时间(天/小时/分钟/秒)
    :param strDate: %Y%m%d 格式的8位日期字符串
    :param days: 要增加的天数
    :param hours: 要增加的小时数
    :param minutes: 要增加的分钟数
    :param seconds: 要增加的秒数
    :return: 增加时间间隔后的 等长度 字符串
    """
    date = convertToTime(strDate)
    date_t = date + datetime.timedelta(days=int(days), hours=int(hours), minutes=int(minutes), seconds=int(seconds))

    if len(strDate) == 8:
        return date_t.strftime('%Y%m%d')
    elif len(strDate) == 10:
        return date_t.strftime('%Y%m%d%H')
    elif len(strDate) == 12:
        return date_t.strftime('%Y%m%d%H%M')
    elif len(strDate) == 14:
        return date_t.strftime('%Y%m%d%H%M%S')


def addHours(strDate, hours):
    """
    在字符串日期上面增加小时数
    :param strDate: %Y-%m-%d %H:%M:%S 格式的8位日期字符串
    :param hours: 要增加的小时数
    :return: 增加天数后的 %Y%m%d 格式的8位日期字符串
    """
    date = convertToTime(strDate)
    date_t = date+datetime.timedelta(hours=int(hours))

    return date_t.strftime('%Y-%m-%d %H:%M:%S')


def getYear(strDate):
    # sourcery skip: inline-immediately-returned-variable, remove-redundant-slice-index
    """
    将 %Y%m%d 格式的8位字符串，获取其 YYYY 格式的年份
    :param strDate: %Y%m%d 格式的8位日期字符串
    :return: YYYY 格式的年份
    """
    year = strDate[0:4]

    return year


def getMonth(strDate):  # sourcery skip: inline-immediately-returned-variable
    """
    将 %Y%m%d 格式的8位字符串，获取其 MM 格式的月份
    :param strDate: %Y%m%d 格式的8位日期字符串
    :return: MM 格式的月份
    """
    month = strDate[4:6]

    return month


def getDay(strDate):  # sourcery skip: inline-immediately-returned-variable
    """
    将 %Y%m%d 格式的8位字符串，获取其 dd 格式的日期
    :param strDate: %Y%m%d 格式的8位日期字符串
    :return: dd 格式的日期
    """
    day = strDate[6:]

    return day


def compareDate(date1, date2):
    """
    比较两个日期的前后
    :param date1:
    :param date2:
    :return: 1 -- date1 早于 date2  0 --date1 与 date2 同一日期   -1 -- date1 晚于 date2
    """
    newDate1 = convertToTime(date1)
    newDate2 = convertToTime(date2)

    if newDate1 < newDate2:  # newDate1 早
        return 1
    elif newDate1 == newDate2:  # newDate1 等 newDate2
        return 0
    elif newDate1 > newDate2:  # newDate1 晚
        return -1


def addHoursByDate(strDate, hours):
    """
    在字符串日期上面增加小时数
    :param strDate:
    :param hours:
    :return:
    """
    date = convertToTime(strDate)
    date_t = date + datetime.timedelta(hours=int(hours))

    return date_t.strftime('%Y%m%d_%H%M%S')


def convertTimeToTime(strTime):
    """
    将 %Y%m%d_%H%M%S 格式的字符串，转换为日期时间
    :param strTime: %Y%m%d_%H%M%S 格式的时间字符串
    :return: datetime 类型的日期
    """

    with contextlib.suppress(Exception):
        date = datetime.datetime.strptime(strTime, "%Y%m%d_%H%M%S")
    return date


def getDDMMYYYY(strDate):
    """
    将日期字符串给为 DDMMYYYY 格式
    :param strDate:
    :return:
    """
    return f"{getDay(strDate)}-{getMonth(strDate)}-{getYear(strDate)}"
