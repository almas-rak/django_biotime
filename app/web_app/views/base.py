from django.views.generic import TemplateView
from django.http import JsonResponse
from api.custom_auth import TokenFromCookieAuthentication


class TokenRequiredMixin:
    def dispatch(self, request, *args, **kwargs):
        auth_result = TokenFromCookieAuthentication().authenticate(request)
        if auth_result is None:
            return JsonResponse({'detail': 'Учетные данные для аутентификации не были предоставлены'}, status=401)
        user, token = auth_result
        request.user = user
        return super().dispatch(request, *args, **kwargs)


class IndexView(TokenRequiredMixin, TemplateView):
    template_name = 'index.html'
    login_url = 'login'
    redirect_field_name = 'next'

