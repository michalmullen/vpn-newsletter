from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from crispy_forms.bootstrap import AppendedText
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Fieldset, ButtonHolder, Submit


class UserRegisterForm(UserCreationForm):
    email = forms.EmailField(widget=forms.TextInput(
        attrs={'value': '@avast.com'}), help_text=("You must register with an Avast email account."))

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

    # checks any errors with email when creating an account
    def clean_email(self):
        # Get the email
        email = self.cleaned_data.get('email')
        if email.split('@')[1] != "avast.com":
            raise forms.ValidationError(
                'To register you must use an Avast account.')

        # Check to see if any users already exist with this email as a username.
        try:
            match = User.objects.get(email=email)
        except User.DoesNotExist:
            # Unable to find a user, this is fine
            return email

        # A user was found with this as a username, raise an error.
        raise forms.ValidationError('This email address is already in use.')
