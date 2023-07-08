from django import template
from django.urls import reverse
from django.utils.safestring import SafeString

from base.general.logic.logic import prepare_str

register = template.Library()


@register.simple_tag
def url_section(url_name, section_id):
    return reverse(url_name) + "#" + section_id


# @register.simple_tag
# def url_section_param(url_name, params, section_name, section_id):

#     res = f"{reverse(url_name, args=[params])}#{section_name}{section_id}"
#     print(f"res,{res}")
#     return res


@register.simple_tag
def url_section_param(_reverse, section_name, section_id):

    res = f"{_reverse}#{section_name}_{section_id}"

    return res


@register.simple_tag
def add_section_param(url, sec_id):
    return f"{url}#{sec_id}"


@register.simple_tag
def concat(str1, str2):
    return f"{str1}{str2}"


@register.simple_tag
def span_world(q: str, world: str):

    if world.strip() in q.strip():
        return SafeString(q.replace(world, f"<span class = 'bg-warning text-dark'>{world}</span>"))
    else:
        return q


@register.simple_tag
def prep_str(val: str):
    return prepare_str(val)


# @register.simple_tag
# def slice_text_count(val: str,count:int):


@register.simple_tag
def slice_text(val: str, count=120):

    val = val.strip()
    start = count

    if len(val) < start:
        return val
    to = val[start:].find(" ")
    res = val[0 : to + start]

    return res
