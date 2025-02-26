
import requests
from django.conf import settings
# BANK_EMAIL = a
# BANK_PASSWORD = a
# definir une fonction qui recupere le token
# une fonction qui récupere les données du formulaire de demande de pret -> elle utilise un token valide -> 


class AuthService:
    """Service pour communiquer avec l'API d'authentification"""

    def login(self, email, password):
        """Connecte un utilisateur via l'API"""
        try:
            print(f"Tentative de connexion à l'API pour {email}")  # Débogage
            # Envoie une requête POST à l'API
            response = requests.post(
                f"{settings.FASTAPI_BASE_URL}/auth/login",
                json={"email": email, "password": password}
            )

            print(f"Réponse API: {response.status_code}")  # Débogage

            # Si la connexion réussit
            if response.status_code == 200:
                result = response.json()
                print(f"Token obtenu: {result.get('access_token', 'Aucun token')}")  # Débogage
                return result  # Retourne le token JWT

            # Si le compte n'est pas activé
            elif response.status_code == 403:
                print("Compte non activé")  # Débogage
                return {"error": "not_activated"}

            # Autres erreurs
            else:
                print(f"Erreur de connexion: {response.content}")  # Débogage
                return {"error": "login_failed"}

        except Exception as e:
            print(f"Exception lors de la connexion: {str(e)}")  # Débogage
            return {"error": "api_error", "message": str(e)}