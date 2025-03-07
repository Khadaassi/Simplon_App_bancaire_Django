FROM python:3.12-slim

WORKDIR /app

# Installer les dépendances système nécessaires
RUN apt-get update && apt-get install -y \
    build-essential \
    libpq-dev \
    unixodbc \
    unixodbc-dev \
    curl \
    gnupg2 \
    telnet \
    iputils-ping \
    netcat-openbsd \
    && rm -rf /var/lib/apt/lists/*

# Installation du driver ODBC Microsoft avec la bonne importation de clé GPG
RUN curl https://packages.microsoft.com/keys/microsoft.asc | gpg --dearmor > /usr/share/keyrings/microsoft-archive-keyring.gpg \
    && echo "deb [arch=amd64 signed-by=/usr/share/keyrings/microsoft-archive-keyring.gpg] https://packages.microsoft.com/debian/12/prod bookworm main" > /etc/apt/sources.list.d/mssql-release.list \
    && apt-get update \
    && ACCEPT_EULA=Y apt-get install -y msodbcsql18 \
    && rm -rf /var/lib/apt/lists/*

# Vérification de l'installation du driver ODBC
RUN odbcinst -j

# Copie et installation des dépendances
COPY requirements.txt .
RUN pip install --upgrade pip && pip install --no-cache-dir -r requirements.txt

# Copie du projet Django dans l'image
COPY . .

# Collecte des fichiers statiques
RUN python manage.py collectstatic --noinput

# Rendre le script entrypoint.sh exécutable
RUN chmod +x /app/entrypoint.sh

# Définition du point d'entrée
ENTRYPOINT ["/app/entrypoint.sh"]

# Commande par défaut pour lancer Daphne
CMD ["daphne", "-b", "0.0.0.0", "-p", "8080", "Bamk.asgi:application"]

# Exposition du port 8080
EXPOSE 8080