from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class RegistrationForm(UserCreationForm):
    username = forms.CharField(
        label="Username",
        max_length=30,
        required=True,
        widget=forms.TextInput(attrs={
            'placeholder': 'Enter your username',
            'class': 'form-control'
        })
    )
    
    email = forms.EmailField(
        label="Email",
        max_length=254,
        required=True,
        widget=forms.EmailInput(attrs={
            'placeholder': 'Enter your email address',
            'class': 'form-control'
        })
    )
    
    password1 = forms.CharField(
        label="Password",
        strip=False,
        widget=forms.PasswordInput(attrs={
            'autocomplete': 'new-password',
            'placeholder': 'Enter your password',
            'class': 'form-control'
        }),
    )
    
    password2 = forms.CharField(
        label="Confirm Password",
        strip=False,
        widget=forms.PasswordInput(attrs={
            'placeholder': 'Confirm your password',
            'class': 'form-control'
        }),
    )
    
    advisor = forms.ModelChoiceField(
        label="Advisor",
        queryset=User.objects.filter(is_staff=True),
        required=True,
        widget=forms.Select(attrs={'class': 'form-control'}),
        empty_label="Select an advisor"
    )

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2', 'advisor']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Ensure the advisor queryset is always up-to-date.
        self.fields['advisor'].queryset = User.objects.filter(is_staff=True)

    def save(self, commit=True):
        # First, save the user instance.
        user = super().save(commit=commit)
        
        # Then, associate the selected advisor to the user's profile.
        advisor = self.cleaned_data.get('advisor')
        profile = user.profile
        profile.advisor = advisor
        
        if commit:
            profile.save()
        
        return user
