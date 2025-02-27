# loan/urls.py
from django.urls import path
from .views import (
    loan_request_view, loan_detail, advisor_loans, client_history, client_loans
)

urlpatterns = [
    path("request/", loan_request_view, name="loan_request"),
    path("detail/<int:loan_id>/", loan_detail, name="loan_detail"),
    path("advisor/loans/", advisor_loans, name="advisor_loans"),
    path("advisor/client/<int:client_id>/", client_history, name="client_history"),
    path("client/loans/", client_loans, name="client_loans"),
]