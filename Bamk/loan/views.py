# loan/views.py
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.views import View
from django.utils.decorators import method_decorator
from .forms import LoanRequestForm #PasswordConfirmForm
from .services import LoanAPIService


@method_decorator(login_required, name='dispatch')
class LoanRequestView(View):
    """Vue pour soumettre une demande de prêt"""
    def get(self, request):
        form = LoanRequestForm()
        return render(request, "loan/loan_request.html", {"form": form})

    # loan/views.py - Modifiez la méthode post de LoanRequestView
    def post(self, request):
        form = LoanRequestForm(request.POST)
        print(f"Form data: {request.POST}")  # Débogage

        if form.is_valid():
            print("Form is valid, checking JWT token")  # Débogage

            # Vérifier si le token JWT existe
            if 'jwt_token' not in request.session:
                print("No JWT token found, requesting a new one")  # Débogage

                # Demander un nouveau token
                from user.services import AuthService
                auth_service = AuthService()
                api_result = auth_service.login(
                    request.user.username,  # Utilisez le nom d'utilisateur comme email
                    request.user.password  # Ceci ne fonctionnera pas car le mot de passe est haché
                )

                if "error" not in api_result:
                    # Stocker le nouveau token JWT dans la session
                    request.session['jwt_token'] = api_result['access_token']
                    print(f"New JWT token obtained: {api_result['access_token']}")  # Débogage
                else:
                    # Gérer les erreurs d'authentification API
                    error_msg = "Erreur d'authentification API, veuillez vous reconnecter"
                    messages.error(request, error_msg)
                    print(f"API authentication error: {api_result}")  # Débogage
                    return redirect('login')

            # Soumettre à l'API FastAPI
            print("Submitting loan request to API")  # Débogage
            result = LoanAPIService.submit_loan_request(request, form.cleaned_data)
            print(f"API result: {result}")  # Débogage

            if "error" not in result:
                # Vérifier la prédiction
                if result.get("eligible", False):
                    return redirect("loan_approved")
                else:
                    return redirect("loan_rejected")
            else:
                error_msg = "Erreur lors de la soumission de la demande"
                if result.get("error") == "authentication_error":
                    error_msg = "Erreur d'authentification, veuillez vous reconnecter"
                messages.error(request, error_msg)
        else:
            print(f"Form errors: {form.errors}")  # Débogage

        return render(request, "loan/loan_request.html", {"form": form})

@method_decorator(login_required, name='dispatch')
class UserLoansView(View):
    """Vue pour afficher l'historique des prêts"""
    def get(self, request):
        result = LoanAPIService.get_loan_history(request)

        if "error" in result:
            error_msg = "Impossible de récupérer l'historique des prêts"
            if result.get("error") == "authentication_error":
                error_msg = "Erreur d'authentification, veuillez vous reconnecter"
            messages.error(request, error_msg)
            loans = []
        else:
            loans = result

        return render(request, "loan/user_loans.html", {"loans": loans})

@method_decorator(login_required, name='dispatch')
class LoanApprovedView(View):
    """Vue pour afficher la page de prêt approuvé"""
    def get(self, request):
        return render(request, "loan/loan_approved.html")

@method_decorator(login_required, name='dispatch')
class LoanRejectedView(View):
    """Vue pour afficher la page de prêt rejeté"""
    def get(self, request):
        return render(request, "loan/loan_rejected.html")

@method_decorator(login_required, name='dispatch')
class AdvisorLoansView(View):
    """Vue pour les conseillers pour voir les prêts"""
    def get(self, request):
        if not request.user.is_staff:
            messages.error(request, "Accès refusé")
            return redirect("home")

        result = LoanAPIService.get_advisor_loans(request)

        if "error" in result:
            error_msg = "Impossible de récupérer les prêts des clients"
            if result.get("error") == "authentication_error":
                error_msg = "Erreur d'authentification, veuillez vous reconnecter"
            messages.error(request, error_msg)
            client_loans = {}
        else:
            client_loans = result

        return render(request, "loan/advisor_loans.html", {"client_loans": client_loans})
    

# @method_decorator(login_required, name='dispatch')
# class TokenRefreshView(View):
#     """Vue pour demander le mot de passe et obtenir un nouveau token JWT"""
#     def get(self, request):
#         return render(request, "loan/password_confirm.html", {"form": PasswordConfirmForm()})

#     def post(self, request):
#         form = PasswordConfirmForm(request.POST)
#         if form.is_valid():
#             # Authentification API
#             from user.services import AuthService
#             auth_service = AuthService()

#             # Débogage
#             print(f"Tentative d'authentification pour {request.user.username}")

#             api_result = auth_service.login(
#                 request.user.username,  # Utilisez le nom d'utilisateur comme email
#                 form.cleaned_data['password']
#             )

#             # Débogage
#             print(f"Résultat de l'authentification: {api_result}")

#             if "error" not in api_result:
#                 # Stocker le nouveau token JWT dans la session
#                 request.session['jwt_token'] = api_result['access_token']
#                 messages.success(request, "Authentification réussie")

#                 # Rediriger vers la page précédente ou la page d'accueil
#                 next_url = request.GET.get('next', 'home')
#                 print(f"Redirection vers: {next_url}")  # Débogage
#                 return redirect(next_url)
#             else:
#                 # Gérer les erreurs d'authentification API
#                 error_msg = "Erreur d'authentification API"
#                 if api_result.get("error") == "login_failed":
#                     error_msg = "Mot de passe incorrect"
#                 messages.error(request, error_msg)
#                 print(f"Erreur d'authentification: {error_msg}")  # Débogage
#         else:
#             print(f"Erreurs de formulaire: {form.errors}")  # Débogage

#         return render(request, "loan/password_confirm.html", {"form": form})