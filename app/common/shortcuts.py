from django.shortcuts import HttpResponsePermanentRedirect


class CustomSchemeRedirect(HttpResponsePermanentRedirect):
    allowed_schemes = ['tg']
