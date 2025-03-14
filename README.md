# <p align="center">Django Banking Application</p>
<p align="center">
    <img src="Bamk/theme/static/images/project_logo.png" alt="Project Logo" width=auto>
</p>

## Description

**Django Banking Application** est un système bancaire sécurisé et évolutif développé avec Django. Il permet aux utilisateurs de gérer leurs comptes bancaires, d'effectuer des transactions et de suivre leur activité financière de manière efficace. L'application comprend des fonctionnalités telles que l'authentification des utilisateurs, la gestion des prêts, un chat en temps réel, des actualités financières et une interface utilisateur responsive construite avec Tailwind.

## ➔ Menu

* [➔ Structure du projet](#-structure-du-projet)
* [➔ Comment exécuter le projet](#-comment-exécuter-le-projet)
* [➔ Prérequis](#-prérequis)
* [➔ Résultats](#-résultats)
* [➔ Critères d'évaluation](#-critères-dévaluation)
* [➔ Indicateurs de performance](#-indicateurs-de-performance)
* [➔ Licence](#-licence)
* [➔ Auteurs](#-auteurs)

---

## Structure du projet

Ce projet comprend les fichiers et modules principaux suivants :

- **manage.py** : Point d’entrée du projet Django, utilisé pour les tâches administratives.
- **Bamk/** : Contient les modules principaux de l’application bancaire et ses différentes applications :
  - **chat/** : Gère la messagerie en temps réel entre utilisateurs.
  - **loan/** : Gère les demandes et les validations de prêts.
  - **news/** : Affiche les actualités et mises à jour financières.
  - **user/** : Gère l’authentification et les profils des utilisateurs.
  - **models.py** : Définit les modèles de données pour les comptes et transactions.
  - **views.py** : Gère la logique de traitement des requêtes utilisateurs et des réponses.
  - **urls.py** : Associe les URLs aux vues correspondantes.
  - **templates/** : Contient les modèles HTML pour l'affichage des pages web.
- **requirements.txt** : Liste toutes les dépendances Python requises pour le projet.

### Modules supplémentaires

- **theme/** : Contient les fichiers statiques comme le CSS (Tailwind), le JavaScript et les images.
- **migrations/** : Suit les modifications des modèles et gère les mises à jour de la base de données.
- **migration_az.py** : Gestion des migrations initiales sur un base de données azur. Les données clients et administrateurs ont été conservées lors de la migration. Les modifications nécessaires pour convertir les tables en mssql ont été réalisées directement sur le portail par requête.

### Fichiers Docker

- **Dockerfile** : Définit l’environnement conteneurisé pour l’application Django.
- **install_sql_driver.sh** : installation des drivers odbc.

### Fichiers de déploiement

- **deploy.sh** : Automatise le déploiement via un script Bash et assure un déploiement fluide sur les services Azure.


---

## Comment exécuter le projet

Suivez ces étapes pour exécuter l’application :

1. Assurez-vous que Python 3.x est installé sur votre système.
2. Clonez ce dépôt sur votre machine locale :

    ```bash
    git clone https://github.com/Khadaassi/Simplon_App_bancaire_Django.git
    ```

3. Accédez au répertoire du projet :

    ```bash
    cd Simplon_App_bancaire_Django/Bamk
    ```

4. Installez les dépendances requises :

    ```bash
    pip install -r requirements.txt
    ```

5. Appliquez les migrations de la base de données :

    ```bash
    python manage.py migrate
    ```

6. Créez un super-utilisateur pour accéder à l’interface d’administration :

    ```bash
    python manage.py createsuperuser
    ```

7. Exécutez le serveur de développement :

    ```bash
    daphne -b localhost -p 8080 Bamk.asgi:application
    ```

8. Accédez à l’application dans votre navigateur à l’adresse `http://127.0.0.1:8000/`.

#### OU

Exécutez le projet avec Docker :

```bash
docker-compose up --build
```

Déployez sur Azure en utilisant le script Bash :

```bash
chmod +x script.sh
./script.sh
```

---

## Résultats

Les utilisateurs peuvent s’attendre aux fonctionnalités suivantes :

- **Gestion des comptes** : Création, mise à jour et suppression des comptes bancaires.
- **Transactions** : Dépôts, retraits et virements entre comptes.
- **Historique des transactions** : Affichage des historiques détaillés des transactions.
- **Chat en temps réel** : Communication sécurisée au sein de l’application.
- **Gestion des prêts** : Demande et gestion des prêts.
- **Actualités financières** : Suivi des dernières tendances financières.

### Exemple de rendu

<p align="center">
    <img src="Bamk/theme/static/images/HomePage.png" alt="Project Logo" width=auto>
</p>

<p align="center">Lien ➔ <a href="http://bamkapplr.francecentral.azurecontainer.io:8080">http://bamkapplr.francecentral.azurecontainer.io:8080</a>
</p>
<p align="center"><i>Ce lien est réservé à un usage interne.</i></p>

---

## Critères d'évaluation

Pour évaluer le projet, considérez les critères suivants :

- **Délais** : Respect des jalons du projet.
- **Notation** : Fonctionnalité, qualité du code et conformité aux exigences du projet.
- **Objectifs bonus** : Ajout de fonctionnalités supplémentaires comme des outils de budgétisation ou d’analyse.

---

## Indicateurs de performance

La performance et le succès du projet peuvent être mesurés selon :

- **Exactitude** : Gestion correcte des transactions et soldes des comptes.
- **Qualité du code** : Respect des standards de codage, bonne documentation et maintenabilité.
- **Utilisation de Git** : Commits réguliers avec des messages clairs et workflows collaboratifs.
- **Efficacité** : Interface utilisateur réactive et requêtes de base de données optimisées.
- **Conformité en matière de sécurité** : Aucune fuite d’information sensible dans le dépôt GitHub.
- **Préparation de l’infrastructure** : Bonne utilisation des services Azure.
- **Documentation** : README bien structuré et détaillé.

---

## Licence

[MIT License](LICENSE)

---

## Auteurs

- **Khadija Aassi**  
  [GitHub](https://github.com/Khadaassi)
- **Ludivine Raby**  
  [GitHub](https://github.com/ludivineRB)
- **Raouf Addeche**  
  [GitHub](https://github.com/RaoufAddeche)
