# loan/urls.py
from django.urls import path
from .views import (
    LoanRequestView,
    UserLoansView,
    LoanApprovedView,
    LoanRejectedView,
    AdvisorLoansView,
    # TokenRefreshView
)

urlpatterns = [
    path("request/", LoanRequestView.as_view(), name="loan_request"),
    path("history/", UserLoansView.as_view(), name="user_loans"),
    path("approved/", LoanApprovedView.as_view(), name="loan_approved"),
    path("rejected/", LoanRejectedView.as_view(), name="loan_rejected"),
    path("advisor/", AdvisorLoansView.as_view(), name="advisor_loans"),
    # path("refresh-token/", TokenRefreshView.as_view(), name="refresh_token"),
]
