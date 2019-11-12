from django import forms


class EmailForm(forms.Form):
    title = forms.CharField(max_length=100)
    email = forms.EmailField()

    class Meta:
        fields = ['title', 'email']


class ResetForm(forms.Form):
    password = forms.CharField(widget=forms.PasswordInput())

    class Meta:
        fields = ['password']
