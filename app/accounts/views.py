from datetime import timedelta
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseRedirect
from django.shortcuts import redirect
from django.urls import reverse
from django.utils import timezone
from django.views.generic import TemplateView
from rest_framework.authtoken.models import Token
from rest_framework.exceptions import AuthenticationFailed

from accounts.forms import LoginForm, PasswordChangeForm, RegisterForm


class LoginView(TemplateView):
    template_name = 'form_base.html'
    form_class = LoginForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = self.form_class()
        context['class'] = "login-button"
        context['btn'] = "Войти"
        context['title'] = "Авторизация"
        return context

    def post(self, request):
        form = self.form_class(request.POST)
        if not form.is_valid():
            messages.error(request, "Некорректные данные")
            return redirect('login')

        username = form.cleaned_data.get('username')
        password = form.cleaned_data.get('password')

        try:
            user = User.objects.get(username=username)
            if not user.is_active:
                messages.warning(request, "Ваш аккаунт не активен, обратитесь к администратору.")
                return redirect('login')
        except User.DoesNotExist:
            pass  # Пользователь не существует, продолжаем аутентификацию

        user = authenticate(request, username=username, password=password)
        if not user:
            messages.error(request, "Неверное имя пользователя или пароль")
            return redirect('login')

        token, created = Token.objects.get_or_create(user=user)
        if token.created < timezone.now() - timedelta(hours=1):
            token.delete()
            token = Token.objects.create(user=user)
        login(request, user)
        response = HttpResponseRedirect(reverse('index'))

        response.set_cookie(
            'auth_token',
            token.key,  # Используем сгенерированный токен
            httponly=True,  # Защищает от доступа через JavaScript
            # secure=True,  # Устанавливается только через HTTPS
            samesite='Lax'  # Предотвращает отправку токена при запросах с других сайтов
        )

        return response


class LogoutView(TemplateView):

    def get(self, request, **kwargs):
        token_key = request.COOKIES.get('auth_token')
        if not token_key:
            return redirect('login')
        try:
            token = Token.objects.get(key=token_key)
            token.delete()  # Удаление токена из базы данных
        except Token.DoesNotExist:
            return redirect('login')
        logout(request)
        return redirect('login')


# def logout_view(request):
#     token_key = request.COOKIES.get('auth_token')
#     if not token_key:
#         return HttpResponseRedirect('/auth/login/')  # Перенаправление при отсутствии токена
#
#     try:
#         token = Token.objects.get(key=token_key)
#         token.delete()  # Удаление токена из базы данных
#     except Token.DoesNotExist:
#         raise AuthenticationFailed('Invalid token')
#
#     logout(request)
#
#     response = HttpResponseRedirect('/auth/login/')
#     response.delete_cookie('auth_token')  # Удаление куки с токеном
#     response.delete_cookie('sessionid')  # Удаление куки с сессионным идентификатором
#
#     return response


class ChangePasswordView(LoginRequiredMixin, TemplateView):
    template_name = "form_base.html"
    form_class = PasswordChangeForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = self.form_class()
        context['class'] = "btn btn-danger"
        context['btn'] = "Сменить пароль"
        context['title'] = "Смена пароля"
        return context

    # def get(self, request, *args, **kwargs):
    #     form = self.form_class()
    #     return self.render_to_response({'form': form})

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            # Логика для смены пароля
            old_password = form.cleaned_data['old_password']
            new_password = form.cleaned_data['new_password']

            if not request.user.check_password(old_password):
                messages.error(request, "Старый пароль неверен.")
            else:
                request.user.set_password(new_password)
                request.user.save()
                messages.success(request, "Пароль успешно изменен.")
                return redirect('index')  # Перенаправление на главную страницу

        return self.render_to_response({
            'form': form,
            'class': "btn btn-danger",
            'btn': "Сменить пароль",
            'title': "Смена пароля",
        })


class RegisterView(TemplateView):
    template_name = "form_base.html"
    form_class = RegisterForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = self.form_class()
        context['class'] = "btn btn-danger"
        context['btn'] = "Регистрация"
        context['title'] = "Регистрация"
        return context

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = User.objects.create_user(username=username, password=password)
            user.is_active = False  # Устанавливаем учетную запись как неактивную
            user.save()
            messages.success(request, "Ваш аккаунт создан. Ожидайте активации.")
            return redirect('login')

        # Если форма недействительна, отобразите её снова с ошибками
        return self.render_to_response(
            {'form': form, 'class': "btn btn-danger", 'btn': "Регистрация", 'title': "Регистрация"})
