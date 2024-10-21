from django.urls import path
from rest_framework.authtoken.views import obtain_auth_token

from api import views

urlpatterns = [
    path('get_emp/', views.GetEmp.as_view(), name='get_emp'),
    path('api_token_auth/', obtain_auth_token, name='api_token_auth'),
    path('get_status_report/', views.GetMonthlyStatusReport.as_view(), name='get_status_report'),
    path('get_punch_report/', views.GetMonthlyPunchReport.as_view(), name='get_punch_report'),
    path('life_search/', views.EmpSearch.as_view(), name='life_search'),
    path('get_emp_report/', views.GetEmpReport.as_view(), name='get_emp_report'),
    path('protected/', views.Protected.as_view(), name='protected'),
]
