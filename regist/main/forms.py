from allauth.account.forms import LoginForm
from allauth.account.forms import get_login_redirect_url, EmailAwarePasswordResetTokenGenerator
from allauth.account.utils import user_email, perform_login
from allauth.utils import email_address_exists
from django import forms
from django.contrib.auth import authenticate, get_user_model
from django.contrib.auth.forms import UsernameField
from django.utils.translation import gettext_lazy as _
import phonenumbers

UserModel = get_user_model()


class PhoneNumberLoginForm(LoginForm):
    phone_number = forms.CharField(
        label=_("Phone number"),
        max_length=30,
        widget=forms.TextInput(attrs={'type': 'tel'}))

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields.pop('email')
        self.fields.move_to_end('password')
        self.fields.move_to_end('remember')

    def clean(self):
        phone_number = self.cleaned_data.get('phone_number')
        password = self.cleaned_data.get