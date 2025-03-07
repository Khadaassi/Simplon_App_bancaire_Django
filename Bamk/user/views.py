from django.shortcuts import redirect
from django.views.generic import TemplateView, FormView, ListView
from django.contrib.auth.views import LoginView as AuthLoginView
from django.urls import reverse_lazy
from django.contrib.auth import login
from .forms import RegistrationForm
from django.views.generic import ListView, DetailView
from .models import Profile
from loan.models import LoanRequest
from news.models import News
import random

class HomeView(TemplateView):
    template_name = 'home.html'

class UserRegistrationView(FormView):
    template_name = 'register.html'
    form_class = RegistrationForm
    success_url = reverse_lazy('user:home')  # Fallback redirection

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        # Redirect based on user role:
        # If the user is marked as staff, assume they are an advisor.
        if user.is_staff:
            return redirect('user:advisor_dashboard')
        else:
            return redirect('user:client_dashboard')

class UserLoginView(AuthLoginView):
    template_name = 'login.html'

    def get_success_url(self):
        user = self.request.user
        # Redirect: advisors go to advisor dashboard, others to client dashboard.
        if user.is_staff:
            return reverse_lazy('user:advisor_dashboard')
        else:
            return reverse_lazy('user:client_dashboard')

class ClientDashboardView(TemplateView):
    template_name = 'client.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['news'] = list(News.objects.all())[:10]  # Récupérer tous les articles
        random.shuffle(context['news'])  # Mélanger aléatoirement
        context['news'] = context['news'][:3]  # Limiter à 5 articles max
        return context
    

class AdvisorDashboardView(TemplateView):
    template_name = 'advisor.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['news'] = list(News.objects.all())  # Récupérer tous les articles
        random.shuffle(context['news'])  # Mélanger aléatoirement
        context['news'] = context['news'][:5]  # Limiter à 5 articles max
        return context

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
        context['loans'] = LoanRequest.objects.filter(user=self.object.user)
        return context
