import yattag

from django import template
from django.contrib import messages

from adlt.website import menus as website_menus

register = template.Library()


@register.simple_tag(takes_context=True)
def topmenu(context):
    if 'active_topmenu_item' in context:
        current = context['active_topmenu_item']
    else:
        current = context.request.resolver_match.url_name

    doc, tag, text = yattag.Doc().tagtext()
    with tag('ul', klass='nav navbar-nav top-menu'):
        for item in website_menus.menus['topmenu']:
            is_active = current == item.name
            classes = 'active' if is_active else ''
            with tag('li', role='presentation', klass=classes):
                with tag('a', href=item.url()):
                    text(item.label)
    return doc.getvalue()


@register.simple_tag(name='messages', takes_context=True)
def messages_tag(context):
    level_mappig = {
        messages.SUCCESS: 'success',
        messages.INFO: 'info',
        messages.WARNING: 'warning',
        messages.ERROR: 'danger',
    }

    doc, tag, text = yattag.Doc().tagtext()
    for message in messages.get_messages(context['request']):
        level = level_mappig.get(message.level, 'info')
        with tag('div', klass='alert alert-%s' % level, role='alert'):
            text(str(message))
    return doc.getvalue()
