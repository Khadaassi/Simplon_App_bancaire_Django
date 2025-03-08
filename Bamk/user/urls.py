from django.urls import path
from django.contrib.auth.views import LogoutView

from .views import (
    HomeView,
    UserRegistrationView,
    UserLoginView,
    ClientDashboardView,
    AdvisorDashboardView,
    ListClientView,
    ClientFileView,
)

app_name = 'user'

urlpatterns = [
    # General pages
    path('', HomeView.as_view(), name='home'),
    path('register/', UserRegistrationView.as_view(), name='register'),
    path('login/', UserLoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),

    # Dashboards
    path('dashboard/client/', ClientDashboardView.as_view(), name='client_dashboard'),
    path('dashboard/advisor/', AdvisorDashboardView.as_view(), name='advisor_dashboard'),

    # Clients management (Advisor views)
    path('clients/', ListClientView.as_view(), name='clients_list'),
    path('clients/<int:pk>/', ClientFileView.as_view(), name='client_detail'),
    path("list_clients/", ListClientView.as_view(), name="list_clients"),
]
