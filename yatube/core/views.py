from django.apps import AppConfig
from django.shortcuts import render
from django.conf import settings
from django.views.generic import TemplateView


class CoreConfig(AppConfig):
    name = 'core'


def page_not_found(request, exception):
    return render(request, settings.HTML_404,
                  {'path': request.path}, status=404)


def server_error(request):
    return render(request, settings.HTML_500, status=500)


def permission_denied(request, exception):
    return render(request, settings.HTML_403, status=403)


def csrf_failure(request, reason=''):
    return render(request, settings.HTML_CSRF)


class ErrorHandler(TemplateView):

    """ Render error template """

    error_code = 404
    template_name = 'index/error.html'

    def dispatch(self, request, *args, **kwargs):
        """ For error on any methods return just GET """
        return self.get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['error_code'] = self.error_code
        return context

    def render_to_response(self, context, **response_kwargs):
        """ Return correct status code """
        response_kwargs = response_kwargs or {}
        response_kwargs.update(status=self.error_code)
        return super().render_to_response(context, **response_kwargs)
