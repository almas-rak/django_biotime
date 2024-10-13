from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect
from django.shortcuts import redirect
from django.urls import reverse
from django.views.generic import TemplateView
from rest_framework.authtoken.models import Token

from accounts.forms import LoginForm


class LoginView(TemplateView):
    template_name = 'login_form.html'
    form = LoginForm

    def get(self, request, *args, **kwargs):
        form = self.form()
        context = {'form': form}
        return self.render_to_response(context)

    def post(self, request):
        form = self.form(request.POST)
        if not form.is_valid():
            messages.error(request, "Некорректные данные")
            return redirect('login')

        username = form.cleaned_data.get('username')
        password = form.cleaned_data.get('password')

        user = authenticate(request, username=username, password=password)
        if not user:
            messages.warning(request, "Пользователь не найден")
            return redirect('login')

        login(request, user)

        token, created = Token.objects.get_or_create(user=user)

        response = HttpResponseRedirect(reverse('index'))

        response.set_cookie(
            'auth_token',
            token.key,  # Используем сгенерированный токен
            httponly=True,  # Защищает от доступа через JavaScript
            secure=True,  # Устанавливается только через HTTPS
            samesite='Lax'  # Предотвращает отправку токена при запросах с других сайтов
        )

        return response


def logout_view(request):
    logout(request)
    return redirect('login')
