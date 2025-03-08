import os
import requests
from dotenv import load_dotenv

from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse_lazy
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import ListView, DetailView, FormView

from loan.api_client import get_auth_token
from .forms import LoanRequestForm
from .models import LoanRequest, LoanStatus
from user.models import User

# Load environment variables
BASEDIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
load_dotenv(os.path.join(BASEDIR, '.env'))

EMAIL = os.getenv("API_EMAIL")
PASSWORD = os.getenv("API_PASSWORD")
API_LOGIN_URL = os.getenv("API_LOGIN_URL")
API_PREDICT_URL = os.getenv("API_PREDICT_URL")


class ClientHistoryView(LoginRequiredMixin, UserPassesTestMixin, ListView):
    model = LoanRequest
    template_name = 'loan/client_history.html'
    context_object_name = 'loans'

    def test_func(self):
        return self.request.user.is_staff

    def get_queryset(self):
        self.client_obj = get_object_or_404(User, id=self.kwargs['client_id'])
        return LoanRequest.objects.filter(user=self.client_obj).order_by('-created_at')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['client'] = self.client_obj
        return context


class ClientLoansView(LoginRequiredMixin, ListView):
    model = LoanRequest
    template_name = 'loan/client_loans.html'
    context_object_name = 'loans'

    def get_queryset(self):
        return LoanRequest.objects.filter(user=self.request.user).order_by('-created_at')


class LoanDetailView(LoginRequiredMixin, DetailView):
    model = LoanRequest
    template_name = 'loan/loan_detail.html'
    context_object_name = 'loan'
    pk_url_kwarg = 'loan_id'

    def dispatch(self, request, *args, **kwargs):
        self.object = self.get_object()
        if not (request.user.is_staff or self.object.user == request.user):
            messages.error(request, "You do not have access to this loan request.")
            return redirect('home')
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        if request.user.is_staff:
            action = request.POST.get('action')
            if action := request.POST.get('approve'):
                self.object.status = LoanStatus.ADVISOR_APPROVED
                messages.success(request, "Loan successfully approved.")
            elif 'reject' in request.POST:
                self.object.status = LoanStatus.ADVISOR_REJECTED
                messages.success(request, "Loan rejected.")
            self.object.save()
        return redirect(request.path)


class AdvisorLoansView(LoginRequiredMixin, UserPassesTestMixin, ListView):
    model = LoanRequest
    template_name = 'loan/advisor_loans.html'
    context_object_name = 'loans'

    def test_func(self):
        return self.request.user.is_staff

    def get_queryset(self):
        return LoanRequest.objects.filter(status=LoanStatus.AI_APPROVED).order_by('-created_at')


class LoanRequestView(LoginRequiredMixin, FormView):
    template_name = 'loan/form.html'
    form_class = LoanRequestForm
    success_url = reverse_lazy('loan:loan_request')

    def form_valid(self, form):
        token = get_auth_token(EMAIL, PASSWORD)
        if not token:
            messages.error(self.request, "Unable to connect to prediction API.")
            return self.form_invalid(form)

        loan_request = form.save(commit=False)
        loan_request.user = self.request.user
        loan_request.status = LoanStatus.PENDING
        loan_request.bank = "BAMK"  # Enforce default bank value
        loan_request.save()

        data = {
            "State": loan_request.state,
            "NAICS": loan_request.naics,
            "NewExist": loan_request.new_exist,
            "RetainedJob": loan_request.retained_job,
            "FranchiseCode": loan_request.franchise_code,
            "UrbanRural": loan_request.urban_rural,
            "GrAppv": loan_request.gr_appv,
            "Bank": loan_request.bank,
            "Term": loan_request.term,
        }

        headers = {"Authorization": f"Bearer {token}"}
        response = requests.post(API_PREDICT_URL, json=data, headers=headers)

        if response.status_code == 200:
            prediction_data = response.json()
            loan_request.prediction = prediction = prediction_data["eligible"]
            loan_request.status = LoanStatus.AI_APPROVED if prediction else LoanStatus.AI_REJECTED
            loan_request.save()

            context = self.get_context_data(form=form, prediction=prediction, shap_plot=response_data.get("shap_plot"))
            return self.render_to_response(context)

        messages.error(self.request, "An error occurred during the prediction process.")
        return self.render_to_response(self.get_context_data(form=form))
