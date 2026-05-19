from django.shortcuts import redirect
from django.urls import resolve, Resolver404


class RedirectInvalidURLMiddleware:

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):

        try:
            resolve(request.path_info)
        except Resolver404:
            return redirect("pages:home")

        response = self.get_response(request)
        return response