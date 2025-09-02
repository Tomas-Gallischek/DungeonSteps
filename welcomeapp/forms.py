import email
from django import forms
from django.contrib.auth.forms import UserCreationForm
from hracapp import models as hracapp
from hracapp.models import Playerinfo

class RegistrationForm(UserCreationForm):
    GENDER_CHOICES = (
    ('male', 'Muž'),
    ('female', 'Žena'),
    ('other', 'Jiné'),
)
    
    username = forms.CharField(label="Uživatelské jméno", max_length=150, required=True)
    name = forms.CharField(label="Jméno", max_length=100, required=True)
    surname = forms.CharField(label="Příjmení", max_length=100, required=True)
    gender = forms.ChoiceField(label="Pohlaví", choices=GENDER_CHOICES, required=True)
    email = forms.EmailField(label="Email", required=True)
    password1 = forms.CharField(label="Heslo", widget=forms.PasswordInput, required=True)
    password2 = forms.CharField(label="Potvrzení hesla", widget=forms.PasswordInput, required=True)
    rasa = forms.ChoiceField(label="Rasa", choices=hracapp.Playerinfo.RASA_CHOICES, required=True)
    povolani = forms.ChoiceField(label="Povolání", choices=hracapp.Playerinfo.POVOLANI_CHOICES, required=True)

    class Meta(UserCreationForm.Meta):
        model = Playerinfo
        fields = UserCreationForm.Meta.fields + ('username', 'name', 'surname', 'gender', 'email', 'password1', 'password2', 'rasa', 'povolani')
