import yattag
import markdown
from adlt.common.helpers import formrenderer

from django import template
from django.utils.safestring import mark_safe
from django.contrib.staticfiles.storage import staticfiles_storage

register = template.Library()


@register.filter(name='markdown')
def markdown_tag(value):
    return mark_safe(markdown.markdown(value, extensions=['markdown.extensions.attr_list']))


@register.simple_tag(name='formrenderer', takes_context=True)
def formrenderer_filter(context, form):
    return mark_safe(formrenderer.render_fields(context['request'], form))


@register.simple_tag()
def stars(value):
    star_path = staticfiles_storage.url('img/star-icon.png')
    doc = yattag.Doc()
    for i in range(round(value)):
        doc.stag('img', src=star_path)
    return doc.getvalue()
