# -*- coding: UTF-8 -*-
# Copyright 2020-2021 Rumma & Ko Ltd
# License: GNU Affero General Public License v3 (see file COPYING for details)

from django.conf import settings
from django import http
from django.views.generic import View

from lino.core import auth
from lino.core.requests import BaseRequest, ActionRequest

from django.shortcuts import redirect


class Element(View):

    actor = None

    def get(self, request, pk=None):
        # print("20220927 a get()")
        if pk is None:
            return http.HttpResponseNotFound()
        rnd = settings.SITE.kernel.default_renderer

        # kw = dict(actor=self.publisher_model.get_default_table(),
        #     request=request, renderer=rnd, permalink_uris=True)
        kw = dict(renderer=rnd, permalink_uris=True)
        if rnd.front_end.media_name == 'react':
            kw.update(hash_router=True)

        ar = self.actor.request(request=request, **kw)
        obj = ar.get_row_by_pk(pk)
        if obj is None:
            return http.HttpResponseNotFound()
        return obj.get_publisher_response(ar)


# class Index(View):
#     """
#     Render the main page.
#     """
#     @method_decorator(ensure_csrf_cookie)
#     def get(self, request, *args, **kw):
#         # raise Exception("20171122 {} {}".format(
#         #     get_language(), settings.MIDDLEWARE_CLASSES))
#         ar = BaseRequest(request=request, renderer=settings.SITE.kernel.default_renderer, permalink_uris=True)
#         env = settings.SITE.plugins.jinja.renderer.jinja_env
#         template = env.get_template("publisher/index.pub.html")
#         context = ar.get_printable_context(obj=self)
#         response = http.HttpResponse(
#             template.render(**context),
#             content_type='text/html;charset="utf-8"')
#         return response
#
# class Login(View):
#     """
#     Render the main page.
#     """
#     @method_decorator(ensure_csrf_cookie)
#     def get(self, request, *args, **kw):
#         # raise Exception("20171122 {} {}".format(
#         #     get_language(), settings.MIDDLEWARE_CLASSES))
#         ar = BaseRequest(request=request, renderer=settings.SITE.kernel.default_renderer, permalink_uris=True)
#         env = settings.SITE.plugins.jinja.renderer.jinja_env
#         template = env.get_template("publisher/login.html")
#         context = ar.get_printable_context(obj=self)
#         response = http.HttpResponse(
#             template.render(**context),
#             content_type='text/html;charset="utf-8"')
#         return response
#
#     @method_decorator(ensure_csrf_cookie)
#     def post(self, request, *args, **kw):
#         username = request.POST.get('username')
#         password = request.POST.get('password')
#         user = auth.authenticate(
#             request, username=username, password=password)
#         auth.login(request, user, backend='lino.core.auth.backends.ModelBackend')
#
#         return redirect("/")
