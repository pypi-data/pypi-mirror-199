from typing import Type

from django.contrib.auth import REDIRECT_FIELD_NAME
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpRequest

from pursuitlib_django.forms import Form


def form_login_required(function, redirect_field_name=REDIRECT_FIELD_NAME, login_url=None):
    # request needs to be the first argument for compatibility with the "login_required" attribute
    def remap_wrapper(request: HttpRequest, form_type: Type[Form], *args, **kwargs) -> HttpResponse:
        return function(form_type, request, *args, **kwargs)

    result = login_required(remap_wrapper, redirect_field_name, login_url)

    # Remapping input arguments
    return lambda form_type, request, *args, **kwargs: result(request, form_type, *args, **kwargs)
