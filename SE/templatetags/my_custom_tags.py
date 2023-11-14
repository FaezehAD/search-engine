from django import template
from django.utils.html import format_html
import base64


register = template.Library()


@register.simple_tag
def display_lists(input_list):
    output = ""
    for item in input_list:
        output += format_html(f'<button class="role">{item.name}</button>\n')
    return format_html(output)


@register.filter
def base64_encode(value):
    return base64.b64encode(value).decode("utf-8")
