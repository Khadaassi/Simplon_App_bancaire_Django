import requests
#from dotenv import load_dotenv
import os


API_LOGIN_URL = os.getenv("API_LOGIN_URL")


def get_auth_token(email, password):
    url = API_LOGIN_URL
    payload = {"email": email, "password": password}
    
    try:
        response = requests.post(url, json=payload)
        response.raise_for_status()  # Vérifie s'il y a une erreur HTTP
        
        data = response.json()
        return data.get("access_token")  # Adapte selon la structure de réponse de ton API

    except requests.exceptions.RequestException as e:
        print(f"Erreur lors de l'authentification : {e}")
        return None
