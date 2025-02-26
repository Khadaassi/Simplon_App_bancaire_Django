from django.shortcuts import redirect
from django.views.generic import TemplateView, FormView
from django.contrib.auth.views import LoginView as AuthLoginView
from django.urls import reverse_lazy
from django.contrib.auth import login
from .forms import RegistrationForm

class HomeView(TemplateView):
    template_name = 'home.html'

class UserRegistrationView(FormView):
    template_name = 'register.html'
    form_class = RegistrationForm
    success_url = reverse_lazy('home')  # Fallback redirection

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        # Redirect based on user role:
        # If the user is marked as staff, assume they are an advisor.
        if user.is_staff:
            return redirect('advisor_dashboard')
        else:
            return redirect('client_dashboard')

# user/views.py - Modifiez votre UserLoginView
from django.contrib.auth.views import LoginView as AuthLoginView
from django.shortcuts import redirect
from django.contrib import messages
from .services import AuthService


class UserLoginView(AuthLoginView):
    template_name = 'login.html'

    def get_success_url(self):
        user = self.request.user
        # Redirect: advisors go to advisor dashboard, others to client dashboard.
        if user.is_staff:
            return reverse_lazy('advisor_dashboard')
        else:
            return reverse_lazy('client_dashboard')

    def form_valid(self, form):
        # Authentification Django standard
        response = super().form_valid(form)

        # Authentification API
        auth_service = AuthService()
        api_result = auth_service.login(
            form.cleaned_data['username'],  # ou email selon votre configuration
            form.cleaned_data['password']
        )

        if "error" not in api_result:
            # Stocker le token JWT dans la session
            self.request.session['jwt_token'] = api_result['access_token']
        else:
            # Gérer les erreurs d'authentification API
            messages.error(self.request, "Erreur d'authentification API")

        return response
    

class ClientDashboardView(TemplateView):
    template_name = 'client.html'
    

class AdvisorDashboardView(TemplateView):
    template_name = 'advisor.html'
