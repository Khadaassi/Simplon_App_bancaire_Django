from django.urls import path
from .views import loan_request_view, client_history, client_loans, loan_detail, advisor_loans

app_name = "loan"

urlpatterns = [
    path("request/", loan_request_view, name="loan_request"),  # ✅ Correction de la redirection
    path("history/", client_history, name="client_history"),  # ✅ Ajout du `/`
    path("client/loans/", client_loans, name="client_loans"),  # ✅ Suppression de la duplication
    path("detail/<int:loan_id>/", loan_detail, name="loan_detail"),
    path("advisor/loans/", advisor_loans, name="advisor_loans"),
]
