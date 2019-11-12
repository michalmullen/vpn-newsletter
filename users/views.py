from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import EmailMessage
from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode

from .forms import UserRegisterForm
from .tokens import account_activation_token


def register(request):
    # if request is a POST this means user sent a form submission to register
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            # get form fields
            username = form.cleaned_data.get('username')
            email = form.cleaned_data.get('email')
            user = form.save(commit=False)
            user.is_active = False
            user.save()
            current_site = get_current_site(request)
            # we don't want any user that doesn't have an avast account to create one
            # so we send the user an activation link to confirm their email
            mail_subject = 'Activate your account.'
            message = render_to_string('users/activate_email.html', {
                'user': user,
                'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': account_activation_token.make_token(user),
            })
            email = EmailMessage(
                mail_subject, message, to=[email]
            )
            email.send()
            return render(request, 'users/check_email.html')
    # else the user has simply opened the page
    else:
        form = UserRegisterForm()
    # render html page with form as context
    return render(request, 'users/register.html', {'form': form})


# creates account if activation link is entered
def activate(request, uidb64, token):
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        return render(request, 'users/account_created.html')
    else:
        return HttpResponse('Activation link is invalid!')
