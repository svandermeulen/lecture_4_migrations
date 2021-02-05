"""
-*- coding: utf-8 -*-
Written by: sme30393
Date: 05/02/2021
"""
from django.conf import settings
from django.contrib import messages
from django.contrib.auth import REDIRECT_FIELD_NAME, decorators
from django.contrib.auth.decorators import login_required
from django.shortcuts import resolve_url
from functools import wraps
from urllib.parse import urlparse


default_message = "Please log in, in order to see the requested page."


def user_passes_test(test_func, login_url=None, redirect_field_name=REDIRECT_FIELD_NAME, message=default_message):
    """
    Decorator for views that checks that the user passes the given test,
    setting a message in case of no success. The test should be a callable
    that takes the user object and returns True if the user passes.
    """

    def decorator(view_func):
        @wraps(view_func)
        def _wrapped_view(request, *args, **kwargs):
            if test_func(request.user):
                return view_func(request, *args, **kwargs)
            path = request.build_absolute_uri()
            resolved_login_url = resolve_url(login_url or settings.LOGIN_URL)
            # If the login url is the same scheme and net location then just
            # use the path as the "next" url.
            login_scheme, login_netloc = urlparse(resolved_login_url)[:2]
            current_scheme, current_netloc = urlparse(path)[:2]
            if ((not login_scheme or login_scheme == current_scheme) and
                    (not login_netloc or login_netloc == current_netloc)):
                path = request.get_full_path()
            from django.contrib.auth.views import redirect_to_login
            messages.error(request, message)
            return redirect_to_login(
                path, resolved_login_url, redirect_field_name)
        return _wrapped_view
    return decorator


def login_required_message(function=None, message=default_message):
    """
    Decorator for views that checks that the user is logged in, redirecting
    to the log-in page if necessary.
    """
    actual_decorator = user_passes_test(
        lambda u: u.is_authenticated,  # fixed by removing ()
        message=message,
    )
    if function:
        return actual_decorator(function)
    return actual_decorator


def login_required_message_and_redirect(function=None, redirect_field_name=REDIRECT_FIELD_NAME, login_url=None, message=default_message):

    if function:
        return login_required_message(
            login_required(function, redirect_field_name, login_url),
            message
        )

    return lambda deferred_function: login_required_message_and_redirect(deferred_function, redirect_field_name, login_url, message)


def main():
    pass


if __name__ == "__main__":
    main()
