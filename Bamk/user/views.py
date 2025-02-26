from django.shortcuts import redirect
from django.views.generic import TemplateView, FormView, ListView
from django.contrib.auth.views import LoginView as AuthLoginView
from django.urls import reverse_lazy
from django.contrib.auth import login
from .forms import RegistrationForm
from django.views.generic import ListView, DetailView
from .models import Profile
from loan.models import Loan

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

class UserLoginView(AuthLoginView):
    template_name = 'login.html'

    def get_success_url(self):
        user = self.request.user
        # Redirect: advisors go to advisor dashboard, others to client dashboard.
        if user.is_staff:
            return reverse_lazy('advisor_dashboard')
            return reverse_lazy('advisor_dashboard')
        else:
            return reverse_lazy('client_dashboard')

class ClientDashboardView(TemplateView):
    template_name = 'client.html'
    

class AdvisorDashboardView(TemplateView):
    template_name = 'advisor.html'

class ListClientView(ListView):
    template_name = 'list_clients.html'
    context_object_name = 'clients'

    def get_queryset(self):
        if self.request.user.is_authenticated:
            return Profile.objects.filter(advisor=self.request.user)
        return Profile.objects.none()


class ClientFileView(DetailView):
    model = Profile
    template_name = 'client_file.html'
    context_object_name = 'client'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['loans'] = Loan.objects.filter(user=self.object.user)
        return context
