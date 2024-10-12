from django.urls import path
from rest_framework.authtoken.views import obtain_auth_token

from api import views

urlpatterns = [
    path('get_emp/', views.GetEmp.as_view(), name='get_emp'),
    path('api-token-accounts/', obtain_auth_token, name='api_token_auth'),
    path('get_status_report/', views.GetMonthlyStatusReport.as_view(), name='get_status_report'),
]
