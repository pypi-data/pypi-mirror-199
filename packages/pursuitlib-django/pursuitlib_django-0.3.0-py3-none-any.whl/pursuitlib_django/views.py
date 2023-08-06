from typing import Type

from pursuitlib_django.forms import Form


def view_form(form_type: Type[Form]):
    return lambda request, **kwargs: form_type.handle_request(form_type, request, **kwargs)
