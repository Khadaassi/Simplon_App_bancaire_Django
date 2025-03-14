FROM python:3.12.3-slim

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app


# # Copier et exécuter le script d'installation des drivers SQL Server
# COPY install_sql_driver.sh install_sql_driver.sh
# RUN chmod +x ./install_sql_driver.sh && ./install_sql_driver.sh

# Installation des dépendances nécessaires pour pyodbc et SQL Server
RUN apt-get update && apt-get install -y \
    unixodbc-dev \
    gcc \
    g++ \
    make \
    && rm -rf /var/lib/apt/lists/*

# Installation des bibliothèques spécifiques pour SQL Server ODBC
RUN apt-get update && apt-get install -y \
    curl \
    gnupg \
    apt-transport-https \
    && curl https://packages.microsoft.com/keys/microsoft.asc | apt-key add - \
    && curl https://packages.microsoft.com/config/debian/10/prod.list > /etc/apt/sources.list.d/mssql-release.list \
    && apt-get update \
    && ACCEPT_EULA=Y apt-get install -y msodbcsql18

# Copy requirements and install Python dependencies
COPY requirements.txt .
RUN pip install --upgrade pip && pip install -r requirements.txt

# Copy the entire project into the container
COPY . .

# Change to the directory containing manage.py
WORKDIR /app/Bamk

# Collect static files
RUN python manage.py collectstatic --noinput

# Expose port 8080
EXPOSE 8080

# Run Gunicorn using the WSGI module in the inner Bamk folder
CMD ["gunicorn", "Bamk.wsgi:application", "-w","3", "--bind", "0.0.0.0:8080"] 