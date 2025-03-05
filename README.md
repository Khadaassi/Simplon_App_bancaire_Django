# <p align="center">Simplon_App_bancaire_Django</p>
<p align="center">
    <img src="images/project_logo.png" alt="Project Logo" width="200">
</p>

## ➤ Menu

* [➤ Project Structure](#-project-structure)
* [➤ How to Run](#-how-to-run)
* [➤ Requirements](#-requirements)
* [➤ Outputs](#-outputs)
* [➤ Evaluation Criteria](#-evaluation-criteria)
* [➤ Performance Metrics](#-performance-metrics)
* [➤ License](#-license)
* [➤ Authors](#-authors)

---

## Project Structure

This project includes the following primary files and modules:

- **manage.py**: Django's command-line utility.
- **settings.py**: Configuration file for the Django project.
- **urls.py**: Defines the project's URL routing.
- **models.py**: Contains database models for users, loans, messages, and news.
- **views.py**: Handles HTTP requests and application logic.
- **consumers.py**: Manages WebSocket communication for real-time chat.
- **theme/**: Contains Tailwind CSS styles and configurations.

### Additional Modules

- **channels/**: Manages WebSocket connections.
- **authentication/**: Handles user authentication and permissions.
- **loans/**: Manages loan requests and processing.
- **chat/**: Implements real-time messaging between clients and advisors.
- **news/**: Handles banking news publications.

---

## How to Run

Follow these steps to execute the project:

1. Ensure Python is installed on your system.
2. Clone this repository to your local machine:

```bash
    git clone https://github.com/username/Simplon_App_bancaire_Django.git
```
3. Navigate to the project directory:

```bash
    cd Simplon_App_bancaire_Django
```
4. Create and activate a virtual environment:

```bash
    python -m venv venv
    source venv/bin/activate  # On macOS/Linux
    venv\Scripts\activate  # On Windows
```
5. Install the required dependencies:

```bash
    pip install -r requirements.txt
```
6. Apply database migrations:

```bash
    python manage.py migrate
```
7. Create a superuser:

```bash
    python manage.py createsuperuser
```
8. Run the development server using Daphne:

```bash
    daphne -b 0.0.0.0 -p 8000 Simplon_App_bancaire_Django.asgi:application
```

---

## Requirements

The project depends on the following Python packages:

```
asgiref==3.8.1
attrs==25.1.0
autobahn==24.4.2
Automat==24.8.1
cffi==1.17.1
channels==4.2.0
channels_redis==4.2.1
constantly==23.10.4
cryptography==44.0.1
daphne==4.1.2
Django==5.1.6
django-browser-reload==1.18.0
django-tailwind==3.8.0
hyperlink==21.0.0
idna==3.10
incremental==24.7.2
msgpack==1.1.0
pillow==11.1.0
pyasn1==0.6.1
pyasn1_modules==0.4.1
pycparser==2.22
pyOpenSSL==25.0.0
redis==5.2.1
service-identity==24.2.0
setuptools==75.8.0
sqlparse==0.5.3
tailwind==3.1.5b0
Twisted==24.11.0
txaio==23.1.1
typing_extensions==4.12.2
whitenoise==6.9.0
```

---

## Outputs

The application provides the following outputs:

- **Loan Requests Management**: Users can submit, track, and receive updates on loan requests.
- **Real-Time Messaging**: Clients can chat with their assigned advisors.
- **Bank News Portal**: Clients can view published banking news.
- **Admin Dashboard**: Administrators can manage users and review loan applications.

### Example Output

<p align="center">
  <img src="images/example_output.png" alt="Example Output" width="600"/>
</p>

<p align="center"><i>Example of loan request dashboard</i></p>

---

## Evaluation Criteria

This project was developed as part of a **2-week group project**. The evaluation criteria include:

- **Part 1: API Development (FastAPI)**
  - Secure authentication system using JWT.
  - Loan request processing and database storage.
  - Role-based access control for users and admins.
  
- **Part 2: Banking Application (Django)**
  - Full web interface for clients and advisors.
  - Real-time chat functionality using Django Channels.
  - Secure and scalable architecture.

---

## Performance Metrics

Success is measured based on the following criteria:

- **Security**: Authentication mechanisms, role-based access, and password encryption.
- **Scalability**: Performance with concurrent WebSocket connections.
- **Code Quality**: Maintainability and modular structure.
- **Database Integrity**: Efficient storage and retrieval of loan data.

---

## License

[MIT License](LICENSE)

---

## Authors

- **Ludivine Raby**
- **Raouf Addeche**
- **Khadija Aassi**

<a href="https://github.com/YourGitHubProfile" target="_blank">
    <img loading="lazy" src="images/github-mark.png" width="30" height="30" style="vertical-align: middle; float: middle; margin-left: 30px;" alt="GitHub Logo">
</a>

