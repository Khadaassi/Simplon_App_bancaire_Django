from django import forms
from .models import LoanRequest

class LoanRequestForm(forms.ModelForm):

    state = forms.CharField(
        label="State",
        max_length=50,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Ex: California'
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
        choices=[(1, "Nouvelle entreprise"), (2, "Entreprise existante")],
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
        choices=[(1, "Urban"), (2, "Rural"), (0, "Non specified")],
        widget=forms.Select(attrs={'class': 'form-control'})
    )

    gr_appv = forms.FloatField(
        label="Approved amount",
        min_value=0,
        widget=forms.NumberInput(attrs={
            'class': 'form-control',
            'placeholder': 'Ex: 50000.00',
            'step': '0.01'
        })
    )

    bank = forms.CharField(
        label="Bank",
        max_length=100,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Ex: Bank of America'
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
                  'urban_rural', 'gr_appv', 'bank', 'term']
    
