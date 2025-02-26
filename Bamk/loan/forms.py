# loan/forms.py
from django import forms

class LoanRequestForm(forms.Form):
    State = forms.CharField(label="État", max_length=2)
    NAICS = forms.IntegerField(label="Code NAICS")
    NewExist = forms.IntegerField(label="Nouvelle entreprise (1) ou existante (2)")
    RetainedJob = forms.IntegerField(label="Emplois conservés")
    FranchiseCode = forms.IntegerField(label="Code de franchise")
    UrbanRural = forms.IntegerField(label="Urbain (1) ou rural (2)")
    GrAppv = forms.FloatField(label="Montant du prêt")
    Bank = forms.CharField(label="Banque", max_length=100)
    Term = forms.IntegerField(label="Durée (mois)")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Ajouter des classes Bootstrap aux champs
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'


# class PasswordConfirmForm(forms.Form):
#     password = forms.CharField(widget=forms.PasswordInput(), label="Mot de passe")