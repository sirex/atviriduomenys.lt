from django import template

register = template.Library()


@register.simple_tag()
def username(user):
    if user.first_name or user.last_name:
        return user.get_full_name()
    elif user.username and user.username != 'user':
        return user.username
    elif user.email and '@' in user.email:
        return user.email.split('@')[0]
    else:
        return 'User #%d' % user.pk
