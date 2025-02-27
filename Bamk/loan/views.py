# loan/views.py
from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from loan.api_client import get_auth_token
from .forms import LoanRequestForm
from .models import LoanRequest, LoanStatus
import requests
from user.models import User

# Variables pour l'authentification (à stocker ailleurs pour plus de sécurité)
EMAIL = "Raouf@Bamk.com"
PASSWORD = "admin123"


# URLs de l'API
API_LOGIN_URL = "http://127.0.0.1:8000/auth/login"
API_PREDICT_URL = "http://127.0.0.1:8000/loans/request"

@login_required
def loan_request_view(request):
    user = request.user  # Utilisateur Django

    # Récupération du token API
    token = get_auth_token(EMAIL, PASSWORD)
    if not token:
        messages.error(request, "Impossible de se connecter à l'API")
        return redirect("loan_request")  # Rediriger si l'authentification échoue

    if request.method == "POST":
        form = LoanRequestForm(request.POST)
        if form.is_valid():
            loan_request = form.save(commit=False)
            loan_request.user = user  # Associer la prédiction au User Django
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

            if response.status_code == 200:
                prediction_values = response.json()
                prediction = prediction_values.get("eligible")
                loan_request.prediction = prediction

                # Mise à jour du statut en fonction de la prédiction
                if prediction >= 0.5:  # Supposons que 0.5 est le seuil
                    loan_request.status = 'ai_approved'
                else:
                    loan_request.status = 'ai_rejected'

                loan_request.save()
                return render(request, "loan/result.html", {
                    "prediction": prediction_values["eligible"],
                    "shap_plot": prediction_values.get("shap_plot"),
                    "loan_id": loan_request.id
                })
            else:
                messages.error(request, "Erreur lors de la prédiction")
                return render(request, "loan/error.html", {"error": "Erreur API"})

    else:
        form = LoanRequestForm()

    return render(request, "loan/form.html", {"form": form})

@login_required
def loan_detail(request, loan_id):
    """Voir les détails du prêt"""
    loan = get_object_or_404(LoanRequest, id=loan_id)

    # Vérification des permissions
    is_advisor = request.user.is_staff
    is_owner = loan.user == request.user

    if not (is_owner or is_advisor):
        messages.error(request, "Vous n'avez pas accès à cette demande")
        return redirect('home')

    # Gestion de l'approbation/rejet du prêt par le conseiller
    if is_advisor and request.method == "POST":
        if 'approve' in request.POST:
            loan.status = LoanStatus.ADVISOR_APPROVED
            loan.advisor_notes = request.POST.get('notes', '')
            loan.save()
            messages.success(request, "Prêt approuvé avec succès")
        elif 'reject' in request.POST:
            loan.status = LoanStatus.ADVISOR_REJECTED
            loan.advisor_notes = request.POST.get('notes', '')
            loan.save()
            messages.success(request, "Prêt rejeté")

    return render(request, 'loan/loan_detail.html', {
        'loan': loan,
        'is_advisor': is_advisor,
        'is_owner': is_owner
    })

@login_required
def advisor_loans(request):
    """Liste des prêts pour les conseillers"""
    if not request.user.is_staff:
        messages.error(request, "Accès non autorisé")
        return redirect('home')

    # Récupérer les prêts des clients assignés à ce conseiller
    clients = request.user.clients.all().values_list('user', flat=True)
    loans = LoanRequest.objects.filter(user__in=clients).order_by('-created_at')

    # Récupérer aussi les prêts en attente d'approbation par un conseiller
    pending_loans = LoanRequest.objects.filter(
        status=LoanStatus.AI_APPROVED
    ).order_by('-created_at')

    return render(request, 'loan/advisor_loans.html', {
        'loans': loans,
        'pending_loans': pending_loans
    })

@login_required
def client_history(request, client_id):
    """Voir l'historique des prêts d'un client pour les conseillers"""
    if not request.user.is_staff:
        messages.error(request, "Accès non autorisé")
        return redirect('home')

    client = get_object_or_404(User, id=client_id)
    loans = LoanRequest.objects.filter(user=client).order_by('-created_at')

    return render(request, 'loan/client_history.html', {
        'client': client,
        'loans': loans
    })

@login_required
def client_loans(request):
    """Liste des prêts pour un client"""
    loans = LoanRequest.objects.filter(user=request.user).order_by('-created_at')
    return render(request, 'loan/client_loans.html', {'loans': loans})