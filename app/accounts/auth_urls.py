from django.urls import path
from accounts.views import LoginView, ChangePasswordView, RegisterView

urlpatterns = [
    path("login/", LoginView.as_view(), name='login'),
    path("logout/", LoginView.as_view(), name='logout'),
    path('change_password/', ChangePasswordView.as_view(), name='change_password'),
    path('registration/', RegisterView.as_view(), name='registration'),
]
