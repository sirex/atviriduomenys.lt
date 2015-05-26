import yattag
import markdown

from django import template
from django.utils.safestring import mark_safe
from django.utils.translation import ugettext
from django.core.urlresolvers import reverse
from django.contrib.staticfiles.storage import staticfiles_storage

import adlt.core.models as core_models
from adlt.common.helpers import formrenderer

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
    for i in range(round(value)):  # pylint: disable=unused-variable
        doc.stag('img', src=star_path)
    return doc.getvalue()


@register.simple_tag(takes_context=True)
def likebutton(context, obj):
    if isinstance(obj, core_models.Project):
        object_type = 'project'
    elif isinstance(obj, core_models.Dataset):
        object_type = 'dataset'
    else:
        raise ValueError('Invalid obj type: %r.' % obj)

    request = context['request']

    if request.user.is_authenticated():
        likes = core_models.Likes.objects.filter(user=request.user, object_type=object_type, object_id=obj.pk).exists()
    else:
        likes = False

    doc = yattag.Doc()
    with doc.tag('div', klass='input-group'):
        with doc.tag('span', klass='input-group-addon'):
            with doc.tag('a', href='#', klass='btn btn-success btn-sm like-button'):
                if request.user.is_authenticated():
                    doc.attr(
                        ('data-action', reverse('like-toggle', args=(object_type, obj.pk))),
                        ('data-likes', 'true' if likes else 'false'),
                    )
                else:
                    doc.attr(href=reverse('accounts_login'))

                with doc.tag('span', klass='like'):
                    if likes:
                        doc.attr(style='display: none;')

                    with doc.tag('span', ('aria-hidden', 'true'), klass='glyphicon glyphicon-thumbs-up'):
                        doc.text('')

                    doc.asis('&nbsp;' + ugettext('Patinka'))

                with doc.tag('span', klass='unlike'):
                    if not likes:
                        doc.attr(style='display: none;')

                    with doc.tag('span', ('aria-hidden', 'true'), klass='glyphicon glyphicon-thumbs-down'):
                        doc.text('')

                    doc.asis('&nbsp;' + ugettext('Nebepatinka'))

        with doc.tag('span', klass='input-group-addon'):
            with doc.tag('strong', klass='total-likes'):
                doc.text(str(obj.likes))

    return doc.getvalue()
