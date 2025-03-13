from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import View

from loan.api_client import get_auth_token
from user.models import User
from .forms import LoanRequestForm
from .models import LoanRequest, LoanStatus

import os
import requests
from dotenv import load_dotenv

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
load_dotenv(os.path.join(BASE_DIR, ".env"))

# Authentication variables (à stocker ailleurs pour une sécurité accrue)
EMAIL = os.getenv("API_EMAIL")
PASSWORD = os.getenv("API_PASSWORD")
API_LOGIN_URL = os.getenv("API_LOGIN_URL")
API_PREDICT_URL = os.getenv("API_PREDICT_URL")
print("DEBUG : ", API_LOGIN_URL)
print("DEBUG : ", API_PREDICT_URL)

class ClientHistoryView(LoginRequiredMixin, View):
    """
    Affiche l'historique des prêts d'un client pour les conseillers.
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
    Affiche la liste des prêts pour un client.
    """
    def get(self, request, *args, **kwargs):
        loans = LoanRequest.objects.filter(user=request.user).order_by('-created_at')
        return render(request, 'loan/client_loans.html', {'loans': loans})

class LoanDetailView(LoginRequiredMixin, View):
    """
    Affiche le détail d'un prêt et permet au conseiller de l'approuver/rejeter.
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
        # La vérification de request.method est inutile ici
        if is_advisor:
            if 'approve' in request.POST:
                loan.status = LoanStatus.ADVISOR_APPROVED  # Utilisation de la constante de l'énumération
                loan.save()
                messages.success(request, "Loan successfully approved")
            elif 'reject' in request.POST:
                loan.status = LoanStatus.ADVISOR_REJECTED  # Utilisation de la constante de l'énumération
                loan.save()
                messages.success(request, "Loan rejected")
        return render(request, 'loan/loan_detail.html', {
            'loan': loan,
            'is_advisor': is_advisor,
            'is_owner': is_owner
        })

class AdvisorLoansView(LoginRequiredMixin, View):
    """
    Affiche les prêts approuvés par l'IA pour validation par le conseiller.
    """
    def get(self, request, *args, **kwargs):
        if not request.user.is_staff:
            messages.error(request, "Unauthorized access")
            return redirect('client_dashboard')
        loans = LoanRequest.objects.filter(status=LoanStatus.AI_APPROVED).order_by('-created_at')
        return render(request, 'loan/advisor_loans.html', {'loans': loans})

class LoanRequestView(LoginRequiredMixin, View):
    """
    Traite le formulaire de demande de prêt et envoie les données à l'API de prédiction.
    """
    def get(self, request, *args, **kwargs):
        form = LoanRequestForm()
        return render(request, "loan/form.html", {"form": form})

    def post(self, request, *args, **kwargs):
        user = request.user  # Utilisateur Django

        # Récupère le token de l'API
        token = get_auth_token(EMAIL, PASSWORD)
        if not token:
            messages.error(request, "Unable to connect to the API")
            return redirect("loan:loan_request")  # Redirection en cas d'échec d'authentification

        form = LoanRequestForm(request.POST)
        if form.is_valid():
            loan_request = form.save(commit=False)
            loan_request.user = user  # Association avec l'utilisateur Django
            loan_request.status = LoanStatus.PENDING  # Statut initial "pending"
            loan_request.save()

            # Préparation des données à envoyer
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

            # Envoi de la requête à l'API
            response = requests.post(API_PREDICT_URL, json=data, headers=headers)
            print("Response status:", response.status_code)
            print("Response text:", response.text)

            if response.status_code == 200:
                prediction = response.json().get("eligible")
                prediction_values = response.json()
                print("Prediction Values:", prediction_values)  # Affichage pour debug

                loan_request.prediction = prediction

                if prediction:
                    loan_request.status = LoanStatus.AI_APPROVED
                else:
                    loan_request.status = LoanStatus.AI_REJECTED

                loan_request.save()
                context = {"prediction": prediction_values["eligible"]}
                print("Context for result page:", context)  # Affichage pour debug
                return render(request, "loan/result.html", context)

            else:
                messages.error(request, "Error during prediction")
                return render(request, "loan/error.html", {"error": "API error"})
        else:
            form = LoanRequestForm()

        return render(request, "loan/form.html", {"form": form})
