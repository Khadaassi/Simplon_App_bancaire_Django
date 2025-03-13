# <p align="center">Django Banking Application</p>
<p align="center">
    <img src="Bamk/theme/static/images/project_logo.png" alt="Project Logo" width=auto>
</p>

## Description

Django Banking Application is a secure and scalable banking system built using Django. It enables users to manage bank accounts, perform transactions, and track financial activity efficiently. The application includes features such as user authentication, loan management, real-time chat, financial news, and a responsive UI built with Tailwind.

## ➔ Menu

* [➔ Project Structure](#-project-structure)
* [➔ How to Run](#-how-to-run)
* [➔ Requirements](#-requirements)
* [➔ Outputs](#-outputs)
* [➔ Evaluation Criteria](#-evaluation-criteria)
* [➔ Performance Metrics](#-performance-metrics)
* [➔ License](#-license)
* [➔ Authors](#-authors)

---

## Project Structure

This project includes the following primary files and modules:

- **manage.py**: The entry point of the Django project. Used for administrative tasks.
- **Bamk/**: Contains the main banking application modules and different apps:
  - **chat/**: Handles real-time messaging between users.
  - **loan/**: Manages loan requests and approvals.
  - **news/**: Displays financial news and updates.
  - **user/**: Manages user authentication and profiles.
  - **models.py**: Defines the data models for accounts and transactions.
  - **views.py**: Handles the logic for processing user requests and returning responses.
  - **urls.py**: Maps URLs to the corresponding views.
  - **templates/**: Contains HTML templates for rendering web pages.
- **requirements.txt**: Lists all Python dependencies required for the project.

### Additional Modules

- **theme/**: Contains static files such as CSS (Tailwind), JavaScript, and images.
- **migrations/**: Tracks changes to the models and handles database schema updates.

### Dockerfiles

- **Dockerfile**: Defines the containerized environment for the Django application.
- **docker-compose.yml**: Configures multi-container deployment.

### Deploy Files

- **deploy.sh**: Automates deployment using Bash scripting.
- **Azure configuration files**: Ensures seamless deployment to Azure services.

---

## How to Run

Follow these steps to execute the project:

1. Ensure Python 3.x is installed on your system.
2. Clone this repository to your local machine:

    ```bash
    git clone https://github.com/Khadaassi/Simplon_App_bancaire_Django.git
    ```

3. Navigate to the project directory:

    ```bash
    cd Simplon_App_bancaire_Django/Bamk
    ```

4. Install the required dependencies:

    ```bash
    pip install -r requirements.txt
    ```

5. Apply the database migrations:

    ```bash
    python manage.py migrate
    ```

6. Create a superuser to access the admin interface:

    ```bash
    python manage.py createsuperuser
    ```

7. Run the development server:

    ```bash
    daphne -b localhost -p 8080 Bamk.asgi:application
    ```

8. Access the application in your browser at `http://127.0.0.1:8000/`.

#### OR

Run the project using Docker:

1. Ensure Python 3.x is installed on your system.
2. Clone this repository to your local machine:

    ```bash
    git clone https://github.com/Khadaassi/Simplon_App_bancaire_Django.git
    ```

3. Navigate to the project directory:

    ```bash
    cd Simplon_App_bancaire_Django/Bamk
    ```
4. Build and run your image.
    ```bash
    docker-compose up --build
    ```

Deploy to Azure using Bash script:

    chmod +x script.sh
    ./script.sh


---

## Outputs

Users can expect the following outputs:

- **Account Management**: Create, update, and delete bank accounts.
- **Transactions**: Perform deposits, withdrawals, and transfers between accounts.
- **Transaction History**: View detailed transaction histories for each account.
- **Real-time Chat**: Communicate securely within the application.
- **Loan Management**: Request and manage loans.
- **Financial News**: Stay updated with the latest financial trends.

### Example Output

<p align="center">
    <img src="Bamk/theme/static/images/HomePage.png" alt="Project Logo" width=auto>
</p>

<p align="center"><i>Link only valid for internal use.</i></p>

<p align="center">Link ➔ <a href="http://bamkapp.francecentral.azurecontainer.io:8080">http://bamkapp.francecentral.azurecontainer.io:8080 </a>
</p>

---

## Evaluation Criteria

For evaluation purposes, consider the following criteria:

- **Timeline**: Ensure timely completion of project milestones.
- **Grading**: Focus on functionality, code quality, and adherence to project requirements.
- **Bonus Objectives**: Implementation of additional features such as budgeting tools or analytics.

---

## Performance Metrics

Performance and success can be measured by:

- **Accuracy**: Correct handling of transactions and account balances.
- **Code Quality**: Adherence to coding standards, proper documentation, and maintainability.
- **Git Usage**: Regular commits with clear messages and collaborative workflows.
- **Efficiency**: Responsive user interface and optimized database queries.
- **Security Compliance**: No sensitive information exposed in the GitHub repository.
- **Infrastructure Readiness**: Proper use of Azure services.
- **Documentation**: Well-structured and detailed README.

---

## License

[MIT License](LICENSE)

---

## Authors

Khadija Aassi
<a href="https://github.com/Khadaassi" target="_blank">
    <img loading="lazy" src="Bamk/theme/static/images/github-mark copie.png" width="30" height="30" style="vertical-align: middle; margin-left: 10px;" alt="GitHub Logo">
</a>
