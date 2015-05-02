from functools import wraps

from django.http import HttpResponse, JsonResponse, HttpResponseNotAllowed
from django.utils.decorators import available_attrs


def request(*permitted_methods):
    def decorator(func):
        @wraps(func, assigned=available_attrs(func))
        def wrapper(request, *args, **kwargs):
            if request.method not in permitted_methods:
                return HttpResponseNotAllowed(permitted_methods)

            result = func(request, *args, **kwargs)

            if isinstance(result, HttpResponse):
                return result
            else:
                return JsonResponse(result, safe=False)

        return wrapper
    return decorator
