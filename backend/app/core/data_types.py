import datetime
import re
from typing import Annotated
from pydantic import AfterValidator, PlainSerializer, WithJsonSchema


def date_str_vali(value: str | datetime.date | int | float):
    if isinstance(value, str):
        pattern = "%Y-%m-%d"
        try:
            datetime.datetime.strptime(value, pattern)
            return value
        except ValueError:
            pass
    elif isinstance(value, datetime.date):
        return value.strftime("%Y-%m-%d")
    raise ValueError("无效的日期时间或字符串数据")


# 实现自定义一个日期字符串的数据类型
DateStr = Annotated[
    str | datetime.date | int | float,
    AfterValidator(date_str_vali),
    PlainSerializer(lambda x: x, return_type=str),
    WithJsonSchema({'type': 'string'}, mode='serialization')
]


def datetime_str_vali(value: str | datetime.datetime | int | float | dict):
    if isinstance(value, str):
        pattern = "%Y-%m-%d %H:%M:%S"
        try:
            datetime.datetime.strptime(value, pattern)
            return value
        except ValueError:
            pass
    elif isinstance(value, datetime.datetime):
        return value.strftime("%Y-%m-%d %H:%M:%S")
    elif isinstance(value, dict):
        # 用于处理 mongodb 日期时间数据类型
        date_str = value.get("$date")
        date_format = '%Y-%m-%dT%H:%M:%S.%fZ'
        # 将字符串转换为datetime.datetime类型
        datetime_obj = datetime.datetime.strptime(date_str, date_format)
        # 将datetime.datetime对象转换为指定的字符串格式
        return datetime_obj.strftime('%Y-%m-%d %H:%M:%S')
    raise ValueError("无效的日期时间或字符串数据")


# 实现自定义一个日期时间字符串的数据类型
DatetimeStr = Annotated[
    str | datetime.datetime | int | float | dict,
    AfterValidator(datetime_str_vali),
    PlainSerializer(lambda x: x, return_type=str),
    WithJsonSchema({'type': 'string'}, mode='serialization')
]


def vali_telephone(value: str | None) -> str:
    if not value:
        return ''
    if len(value) != 11 or not value.isdigit():
        raise ValueError("请输入正确手机号")

    regex = r'^1(3\d|4[4-9]|5[0-35-9]|6[67]|7[013-8]|8[0-9]|9[0-9])\d{8}$'

    if not re.match(regex, value):
        raise ValueError("请输入正确手机号")

    return value


def vali_email(value: str | None) -> str:
    if not value:
        return ''

    regex = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'

    if not re.match(regex, value):
        raise ValueError("请输入正确邮箱地址")

    return value


# 实现自定义一个邮箱类型
Email = Annotated[
    str,
    AfterValidator(lambda x: vali_email(x)),
    PlainSerializer(lambda x: x, return_type=str),
    WithJsonSchema({'type': 'string'}, mode='serialization')
]

# 实现自定义一个手机号类型
Mobile = Annotated[
    str,
    AfterValidator(lambda x: vali_telephone(x)),
    PlainSerializer(lambda x: x, return_type=str),
    WithJsonSchema({'type': 'string'}, mode='serialization')
]
