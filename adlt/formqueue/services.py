import adlt.core.models as core_models


def get_next(user):
    """Get next item from queue"""
    return core_models.Queue.objects.filter(user=user, completed=False).order_by('-created').first()
