#!/bin/bash
set -e

echo "Vérification des variables d'environnement:"
echo "AZURE_SERVER=${AZURE_SERVER}"
echo "AZURE_DATABASE=${AZURE_DATABASE}"
echo "AZURE_USERNAME=${AZURE_USERNAME}"
echo "AZURE_PASSWORD=********"

echo "Vérification de la connectivité réseau:"
ping -c 2 ${AZURE_SERVER} || echo "Le ping a échoué mais nous continuons"

echo "Vérification des drivers ODBC installés:"
odbcinst -q -d

echo "Test de connexion Azure SQL..."
python - << EOF
import os
import pyodbc
import time

print('🔍 Test de connexion Azure SQL...')
conn_str = f'DRIVER={{ODBC Driver 18 for SQL Server}};SERVER={os.getenv("AZURE_SERVER")},1433;DATABASE={os.getenv("AZURE_DATABASE")};UID={os.getenv("AZURE_USERNAME")};PWD={os.getenv("AZURE_PASSWORD")};Encrypt=yes;TrustServerCertificate=yes;Connection Timeout=60;'

try:
    print(f"Tentative de connexion avec: {conn_str.replace(os.getenv('AZURE_PASSWORD'), '********')}")
    conn = pyodbc.connect(conn_str, timeout=60)
    print('✅ Connexion réussie, la base est bien accessible !')
    conn.close()
except Exception as e:
    print(f'❌ Erreur de connexion : {e}')
EOF

echo "Appliquer les migrations..."
python manage.py migrate

echo "Collecte des fichiers statiques..."
python manage.py collectstatic --noinput

echo "Lancement de l'application..."
exec "$@"
