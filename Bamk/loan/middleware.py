# loan/middleware.py
from django.shortcuts import redirect
from django.contrib import messages

# loan/middleware.py - Modifiez le middleware
class JWTMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Liste des URLs qui nécessitent un token JWT
        protected_urls = [
            '/loan/request/',
            '/loan/history/',
            '/loan/advisor/',
        ]

        # # Ne pas vérifier le token pour la page de rafraîchissement du token
        # if request.path == '/loan/refresh-token/':
        #     return self.get_response(request)

        # # Ne vérifier le token que pour les URLs protégées
        # current_path = request.path
        # requires_token = any(current_path.startswith(url) for url in protected_urls)

        # if requires_token and request.user.is_authenticated:
        #     # Vérifier si le token existe
        #     if 'jwt_token' not in request.session:
        #         messages.error(request, "Veuillez confirmer votre identité pour accéder à cette page")
        #         return redirect(f'/loan/refresh-token/?next={request.path}')

        # Continuer le traitement normal pour toutes les autres URLs
        response = self.get_response(request)
        return response