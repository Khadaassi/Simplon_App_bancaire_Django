import requests
from django.conf import settings

class LoanAPIService:
    """Service pour communiquer avec l'API FastAPI pour les prêts"""

    @staticmethod
    def api_request(method, endpoint, request, data=None):
        """Méthode générique pour faire des requêtes à l'API"""
        token = request.session.get('jwt_token')
        if not token:
            return {"error": "authentication_error"}

        try:
            headers = {"Authorization": f"Bearer {token}"}
            url = f"{settings.FASTAPI_BASE_URL}{endpoint}"

            if method.lower() == 'get':
                response = requests.get(url, headers=headers)
            elif method.lower() == 'post':
                response = requests.post(url, headers=headers, json=data)

            if response.status_code == 200:
                return response.json()
            else:
                return {"error": "api_error", "status": response.status_code}
        except Exception as e:
            return {"error": "connection_error", "message": str(e)}

    @staticmethod
    def get_loan_history(request):
        """Récupère l'historique des prêts de l'utilisateur"""
        return LoanAPIService.api_request('get', '/loans/history', request)


    @staticmethod
    def submit_loan_request(request, loan_data):
        """Soumet une demande de prêt à l'API"""
        token = LoanAPIService.get_jwt_token(request)
        if not token:
            print("No JWT token found in session")  # Débogage
            return {"error": "authentication_error"}

        try:
            headers = {"Authorization": f"Bearer {token}"}
            print(f"Sending request to API with data: {loan_data}")  # Débogage
            print(f"Using token: {token}")  # Débogage

            response = requests.post(
                f"{settings.FASTAPI_BASE_URL}/loans/request",
                headers=headers,
                json=loan_data
            )

            print(f"API response status: {response.status_code}")  # Débogage
            print(f"API response content: {response.content}")  # Débogage

            if response.status_code == 200:
                return response.json()
            elif response.status_code == 401:
                # Token expiré ou invalide
                print("Token expired or invalid")  # Débogage
                # Supprimer le token de la session
                if 'jwt_token' in request.session:
                    del request.session['jwt_token']
                return {"error": "authentication_error"}
            else:
                return {"error": "api_error", "status": response.status_code}
        except Exception as e:
            print(f"API request error: {str(e)}")  # Débogage
            return {"error": "connection_error", "message": str(e)}

    @staticmethod
    def get_advisor_loans(request):
        """Récupère les prêts des clients pour un conseiller"""
        return LoanAPIService.api_request('get', '/loans/advisor', request)