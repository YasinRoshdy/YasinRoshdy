from importlib.util import resolve_name
from django import urls
from django.shortcuts import redirect, resolve_url
from django.utils.translation import gettext as _
from django.utils.safestring import SafeString


def if_val_get(val, val2):
    return val2 if val else val


def if_val(var):
    return True if var else False


def get_val(var):
    return var if var else ""


def _v(var):
    return get_val(var)


def if_get(cond, val):

    return val if cond else ""


def sizify(value):
    """
    Simple kb/mb/gb size snippet for templates:

    {{ product.file.size|sizify }}
    """
    # value = ing(value)
    if value < 512000:
        value = value / 1024.0
        ext = _("kb")
    elif value < 4194304000:
        value = value / 1048576.0
        ext = _("mb")
    else:
        value = value / 1073741824.0
        ext = _("gb")
    return "%s %s" % (str(round(value, 2)), ext)


def enToArNumb(number: str):

    dic = {
        "0": "۰",
        "1": "١",
        "2": "٢",
        "3": "۳",
        "4": "٤",
        "5": "۵",
        "6": "٦",
        "7": "۷",
        "8": "۸",
        "9": "۹",
    }
    # (٠، ١، ٢، ٣، ٤، ٥، ٦، ٧، ٨، ٩)

    res = dic.get(number)

    return res if res else number


def en_to_ar(number):
    # print("number", number)
    if number is not str:
        inp = str(number)
    else:
        inp = number

    return "".join([enToArNumb(num) for num in inp])


def get_title_url(title: str, _url: str, params={}):
    # return "<a href='"+urls('base:saheh')+"'></a>"
    base: str = f"base:{_url}"
    path = urls.reverse(base, kwargs=params)

    return f"<a href='{path}'>{title}</a>"


def remove_None_vals(data):

    if data is None or not isinstance(data, dict):
        return data
    return {k: v for k, v in data.items() if v is not None}
