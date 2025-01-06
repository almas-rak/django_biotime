from django.views.generic import TemplateView
from django.http import HttpResponseRedirect
from django.urls import reverse
from api.custom_auth import TokenFromCookieAuthentication
from rest_framework.exceptions import AuthenticationFailed


class TokenRequiredMixin:
    def dispatch(self, request, *args, **kwargs):
        try:
            auth_result = TokenFromCookieAuthentication().authenticate(request)
            if auth_result is None:
                return HttpResponseRedirect(reverse('login'))
            user, token = auth_result
            request.user = user
        except AuthenticationFailed:
            return super().dispatch(request, *args, **kwargs)
        return super().dispatch(request, *args, **kwargs)


class IndexView(TokenRequiredMixin, TemplateView):
    template_name = 'index.html'
    login_url = 'login'
    redirect_field_name = 'next'
