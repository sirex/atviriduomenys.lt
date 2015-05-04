import yattag

from django import template

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
