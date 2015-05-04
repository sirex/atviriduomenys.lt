import markdown

from django import template
from django.utils.safestring import mark_safe

register = template.Library()


@register.filter(name='markdown')
def markdown_tag(value):
    return mark_safe(markdown.markdown(value, extensions=['markdown.extensions.attr_list']))
