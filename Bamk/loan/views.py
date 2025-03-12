from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from django.contrib import messages
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
from loan.api_client import get_auth_token
from .forms import LoanRequestForm
from .models import LoanRequest, LoanStatus
import requests
from user.models import User
import os
from dotenv import load_dotenv

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
load_dotenv(os.path.join(BASE_DIR, ".env"))

# Authentication variables (to be stored elsewhere for increased security)
EMAIL = os.getenv("API_EMAIL")
PASSWORD = os.getenv("API_PASSWORD")
API_LOGIN_URL = os.getenv("API_LOGIN_URL")
API_PREDICT_URL = os.getenv("API_PREDICT_URL")
print("DEBUG : ", API_LOGIN_URL)
print("DEBUG : ", API_PREDICT_URL)

class ClientHistoryView(LoginRequiredMixin, View):
    """
    View the loan history of a client for advisors.
    """
    def get(self, request, client_id, *args, **kwargs):
        if not request.user.is_staff:
            messages.error(request, "Unauthorized access")
            return redirect('home')
        client = get_object_or_404(User, id=client_id)
        loans = LoanRequest.objects.filter(user=client).order_by('-created_at')
        return render(request, 'loan/client_history.html', {
            'client': client,
            'loans': loans
        })

class ClientLoansView(LoginRequiredMixin, View):
    """
    List of loans for a client.
    """
    def get(self, request, *args, **kwargs):
        loans = LoanRequest.objects.filter(user=request.user).order_by('-created_at')
        return render(request, 'loan/client_loans.html', {'loans': loans})

class LoanDetailView(LoginRequiredMixin, View):
    """
    View loan details and allow the advisor to approve/reject.
    """
    def get(self, request, loan_id, *args, **kwargs):
        loan = get_object_or_404(LoanRequest, id=loan_id)
        is_advisor = request.user.is_staff
        is_owner = loan.user == request.user
        if not (is_owner or is_advisor):
            messages.error(request, "You do not have access to this request")
            return redirect('home')
        return render(request, 'loan/loan_detail.html', {
            'loan': loan,
            'is_advisor': is_advisor,
            'is_owner': is_owner
        })

    def post(self, request, loan_id, *args, **kwargs):
        loan = get_object_or_404(LoanRequest, id=loan_id)
        is_advisor = request.user.is_staff
        is_owner = loan.user == request.user
        if not (is_owner or is_advisor):
            messages.error(request, "You do not have access to this request")
            return redirect('home')
        if is_advisor and request.method == "POST":
            if 'approve' in request.POST:
                loan.status = 'advisor_approved'
                loan.save()
                messages.success(request, "Loan successfully approved")
            elif 'reject' in request.POST:
                loan.status = 'advisor_rejected'
                loan.save()
                messages.success(request, "Loan rejected")
        return render(request, 'loan/loan_detail.html', {
            'loan': loan,
            'is_advisor': is_advisor,
            'is_owner': is_owner
        })

class AdvisorLoansView(LoginRequiredMixin, View):
    """
    Display loans approved by AI for advisor validation.
    """
    def get(self, request, *args, **kwargs):
        if not request.user.is_staff:
            messages.error(request, "Unauthorized access")
            return redirect('client_dashboard')
        loans = LoanRequest.objects.filter(status=LoanStatus.AI_APPROVED).order_by('-created_at')
        return render(request, 'loan/advisor_loans.html', {'loans': loans})

class LoanRequestView(LoginRequiredMixin, View):
    """
    Process a loan request form and send data to the prediction API.
    """
    def get(self, request, *args, **kwargs):
        form = LoanRequestForm()
        return render(request, "loan/form.html", {"form": form})

    def post(self, request, *args, **kwargs):
        user = request.user  # Django User

        # Retrieve the API token
        token = get_auth_token(EMAIL, PASSWORD)
        if not token:
            messages.error(request, "Unable to connect to the API")
            return redirect("loan:request")  # Redirect if authentication fails

        form = LoanRequestForm(request.POST)
        if form.is_valid():
            loan_request = form.save(commit=False)
            loan_request.user = user  # Associate the prediction with the Django User
            loan_request.status = LoanStatus.PENDING  # Initialize status to "pending"
            loan_request.save()

            # Prepare the data to send
            data = {
                "State": loan_request.state,
                "NAICS": loan_request.naics,
                "NewExist": loan_request.new_exist,
                "RetainedJob": loan_request.retained_job,
                "FranchiseCode": loan_request.franchise_code,
                "UrbanRural": loan_request.urban_rural,
                "GrAppv": loan_request.gr_appv,
                "Bank": loan_request.bank,
                "Term": loan_request.term,
            }

            headers = {"Authorization": f"Bearer {token}"}

            # Send the request to the API
            response = requests.post(API_PREDICT_URL, json=data, headers=headers)

            if response.status_code == 200:
                prediction = response.json().get("eligible")
                prediction_values = response.json()
                loan_request.prediction = prediction

                # Update the status based on the prediction
                if prediction:
                    loan_request.status = LoanStatus.AI_APPROVED  # Approved by AI
                else:
                    loan_request.status = LoanStatus.AI_REJECTED  # Rejected by AI

                loan_request.save()
                return render(request, "loan/result.html", {"prediction": prediction_values["eligible"]})
            else:
                messages.error(request, "Error during prediction")
                return render(request, "loan/error.html", {"error": "API error"})
        else:
            form = LoanRequestForm()

        return render(request, "loan/form.html", {"form": form})
