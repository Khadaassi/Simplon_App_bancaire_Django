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
EMAIL = "admin@example.com"
PASSWORD = "password123"

# def connect_to_api(request):
#     """
#     Vue qui tente de se connecter à l'API et affiche un message dans un template.
#     """
#     token = get_auth_token(EMAIL, PASSWORD)

#     if token:
#         message = "Vous êtes connectés à l'API"
#     else:
#         message = "Échec de la connexion à l'API"

#     return render(request, "loan/connection_status.html", {"message": message})

# URLs de l'API
API_LOGIN_URL = "http://127.0.0.1:8000/auth/login"
API_PREDICT_URL = "http://127.0.0.1:8000/loans/request"

# @login_required
# def loan_request_view(request):
#     user = request.user  # Utilisateur Django

#     # Récupération du token API
#     token = get_auth_token(EMAIL, PASSWORD)
#     if not token:
#         messages.error(request, "Impossible de se connecter à l'API")
#         return redirect("loan:loan_request")  # Rediriger si l'authentification échoue

#     if request.method == "POST":
#         form = LoanRequestForm(request.POST)
#         if form.is_valid():
#             loan_request = form.save(commit=False)
#             loan_request.user = user  # Associer la prédiction au User Django
#             loan_request.save()

#             # Préparation des données à envoyer
#             data = {
#                 "State": loan_request.state,
#                 "NAICS": loan_request.naics,
#                 "NewExist": loan_request.new_exist,
#                 "RetainedJob": loan_request.retained_job,
#                 "FranchiseCode": loan_request.franchise_code,
#                 "UrbanRural": loan_request.urban_rural,
#                 "GrAppv": loan_request.gr_appv,
#                 "Bank": loan_request.bank,
#                 "Term": loan_request.term,
#             }

#             headers = {"Authorization": f"Bearer {token}"}

#             # Envoi de la requête à l'API
#             response = requests.post(API_PREDICT_URL, json=data, headers=headers)

#             if response.status_code == 200:
#                 prediction = response.json().get("eligible")
#                 prediction_values = response.json()
#                 loan_request.prediction = prediction
#                 loan_request.save()
#                 return render(request, "loan/result.html", {"prediction": prediction_values["eligible"], "shap_plot":prediction_values["shap_plot"] })
#             else:
#                 messages.error(request, "Erreur lors de la prédiction")
#                 return render(request, "loan/error.html", {"error": "Erreur API"})

#     else:
#         form = LoanRequestForm()

#     return render(request, "loan/form.html", {"form": form})


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

@login_required
def loan_detail(request, loan_id):
    """Voir les détails du prêt et permettre au conseiller de valider/rejeter"""
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
            loan.status = 'advisor_approved'
            loan.save()
            messages.success(request, "Prêt approuvé avec succès")
        elif 'reject' in request.POST:
            loan.status = 'advisor_rejected'
            loan.save()
            messages.success(request, "Prêt rejeté")

    return render(request, 'loan/loan_detail.html', {
        'loan': loan,
        'is_advisor': is_advisor,
        'is_owner': is_owner
    })

@login_required
def advisor_loans(request):
    """Afficher les prêts approuvés par l'IA pour validation par le conseiller."""
    if not request.user.is_staff:
        messages.error(request, "Accès non autorisé")
        return redirect('client_dashboard')

    # Récupérer les prêts approuvés par l'IA
    loans = LoanRequest.objects.filter(status=LoanStatus.AI_APPROVED).order_by('-created_at')

    return render(request, 'loan/advisor_loans.html', {'loans': loans})

@login_required
def loan_request_view(request):
    user = request.user  # Utilisateur Django

    # Récupération du token API
    token = get_auth_token(EMAIL, PASSWORD)
    if not token:
        messages.error(request, "Impossible de se connecter à l'API")
        return redirect("loan:loan_request")  # Rediriger si l'authentification échoue

    if request.method == "POST":
        form = LoanRequestForm(request.POST)
        if form.is_valid():
            loan_request = form.save(commit=False)
            loan_request.user = user  # Associer la prédiction au User Django
            loan_request.status = LoanStatus.PENDING  # Initialiser le statut à "pending"
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
                prediction = response.json().get("eligible")
                prediction_values = response.json()
                loan_request.prediction = prediction

                # Mettre à jour le statut en fonction de la prédiction
                if prediction:
                    loan_request.status = LoanStatus.AI_APPROVED  # Approuvé par l'IA
                else:
                    loan_request.status = LoanStatus.AI_REJECTED  # Rejeté par l'IA

                loan_request.save()
                return render(request, "loan/result.html", {"prediction": prediction_values["eligible"], "shap_plot":prediction_values["shap_plot"] })
            else:
                messages.error(request, "Erreur lors de la prédiction")
                return render(request, "loan/error.html", {"error": "Erreur API"})
            
    else:
        form = LoanRequestForm()

    return redirect("loan:loan_request")
