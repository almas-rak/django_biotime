from django.urls import path
from accounts.views import LoginView

urlpatterns = [
    path("login/", LoginView.as_view(), name='login'),
    path("logout/", LoginView.as_view(), name='logout'),
]
