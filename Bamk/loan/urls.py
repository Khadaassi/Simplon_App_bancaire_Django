from django.urls import path
from .views import (
    ClientHistoryView,
    ClientLoansView,
    LoanDetailView,
    AdvisorLoansView,
    LoanRequestView,
)


app_name = "loan"

urlpatterns = [
    path("request/", LoanRequestView.as_view(), name="request"),
    path("history/<int:client_id>/", ClientHistoryView.as_view(), name="client_history"),
    path("client/loans/", ClientLoansView.as_view(), name="client_loans"),
    path("detail/<int:loan_id>/", LoanDetailView.as_view(), name="loan_detail"),
    path("advisor/loans/", AdvisorLoansView.as_view(), name="advisor_loans"),
]