from django import forms
from .models import LoanRequest

# Déclaration des choix pour plus de clarté et de réutilisation
BUSINESS_CHOICES = [(1, "New Business"), (2, "Existing Business")]
ZONE_CHOICES = [(1, "Urban"), (2, "Rural"), (0, "Non specified")]

class LoanRequestForm(forms.ModelForm):
    """ Form for clients to request a loan. """

    state = forms.CharField(
        label="State",
        max_length=50,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Ex: CA'
        })
    )

    naics = forms.IntegerField(
        label="NAICS code",
        widget=forms.NumberInput(attrs={
            'class': 'form-control',
            'placeholder': 'Ex: 541330'
        })
    )

    new_exist = forms.ChoiceField(
        label="New or existing business",
        choices=BUSINESS_CHOICES,
        widget=forms.Select(attrs={'class': 'form-control'})
    )

    retained_job = forms.IntegerField(
        label="Retained jobs",
        min_value=0,
        widget=forms.NumberInput(attrs={
            'class': 'form-control',
            'placeholder': 'Ex: 5'
        })
    )

    franchise_code = forms.IntegerField(
        label="Franchise Code (0 if not a franchise)",
        min_value=0,
        widget=forms.NumberInput(attrs={
            'class': 'form-control',
            'placeholder': 'Ex: 1234'
        })
    )

    urban_rural = forms.ChoiceField(
        label="Zone (urban or rural)",
        choices=ZONE_CHOICES,
        widget=forms.Select(attrs={'class': 'form-control'})
    )

    gr_appv = forms.FloatField(
        label="Approved amount ($)",
        min_value=0,
        widget=forms.NumberInput(attrs={
            'class': 'form-control',
            'placeholder': 'Ex: 50000.00',
            'step': '0.01'
        })
    )

    term = forms.IntegerField(
        label="Term (months)",
        min_value=1,
        widget=forms.NumberInput(attrs={
            'class': 'form-control',
            'placeholder': 'Ex: 36'
        })
    )

    class Meta:
        model = LoanRequest
        fields = ['state', 'naics', 'new_exist', 'retained_job', 'franchise_code', 
                  'urban_rural', 'gr_appv', 'term']

    def clean_naics(self):
        """ Validation for NAICS code (should be a 6-digit number). """
        naics = self.cleaned_data.get('naics')
        if not (100000 <= naics <= 999999):
            raise forms.ValidationError("NAICS code must be a 6-digit number.")
        return naics
