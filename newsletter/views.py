import datetime
import json

import htmlmin
import imgkit
from django.contrib import messages
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.models import User
from django.core.mail import EmailMessage, EmailMultiAlternatives
from django.core.serializers import serialize
from django.db import models
from django.forms import ModelForm, inlineformset_factory
from django.http import Http404, HttpResponse, JsonResponse, request
from django.shortcuts import redirect, render, reverse
from django.template import Context
from django.template.loader import get_template
from django.views.generic import CreateView, DeleteView, UpdateView
from django.views.generic.edit import FormMixin
from django.utils.encoding import smart_str
from django.core.files.storage import FileSystemStorage

from .forms import EmailForm, ResetForm
from .models import Installs, Future, News, Release

# to automatically give the newsletter the corrent day, month and year when entered into the context
now = datetime.datetime.now()
MONTHS = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September',
          'October', 'November', 'December']
DATE = str(now.day) + " " + MONTHS[now.month - 1] + " " + str(now.year)


@login_required
def download(request):
    html_email = get_template(
        'newsletter/newsletter.html')
    cnt = {'news1': News.objects.all(),
           'release1': Release.objects.all(),
           'future1': Future.objects.all(),
           'Installs1': Installs.objects.all(),
           'date': DATE, }
    # renders html email with the given context
    html_cont = html_email.render(cnt)
    # optimizes the email by removing spaces and comments
    html_cont = htmlmin.minify(
        html_cont, remove_all_empty_space=True, remove_comments=True)

    #path = r'C:\Program Files\wkhtmltopdf\bin\wkhtmltoimage.exe'
    path = 'bin/wkhtmltoimage'
    config = imgkit.config(wkhtmltoimage=path)
    imgkit.from_string(html_cont, 'out.jpg', config=config)
    #imgkit.from_string(html_cont, 'out.jpg')

    fs = FileSystemStorage()
    filename = 'out.jpg'
    with fs.open(filename) as pdf:
        response = HttpResponse(pdf, content_type='application/jpg')
        response['Content-Disposition'] = 'attachment; filename="out.jpg"'
        return response


# resets newsletter by deleting all posts added to it
@login_required
def reset_email(request):
    if request.user.is_staff or request.user.is_superuser:
        if request.method == 'POST':
            form = ResetForm(request.POST)
            if form.is_valid():
                current_user = request.user.username
                username = User.objects.get(username=current_user)
                password = form.cleaned_data.get('password')
                # user must put in password to reset email
                if username is not None and username.check_password(password):
                    Installs.objects.all().delete()
                    Future.objects.all().delete()
                    News.objects.all().delete()
                    Release.objects.all().delete()
                    messages.success(
                        request, f'The email was successfully reset!')
                    return redirect('reset')
                else:
                    messages.warning(
                        request, f'The password seems to be incorrect.')
                    return redirect('reset')
        else:
            form = ResetForm()
            context = {'news1': News.objects.all(),
                       'release1': Release.objects.all(),
                       'future1': Future.objects.all(),
                       'Installs1': Installs.objects.all(),
                       'date': DATE,
                       'form': form}
        return render(request, 'newsletter/email_modules/reset.html', context)
    else:
        return HttpResponse(
            "You do not have sufficient enough permission to access this page.")


# sends the newsletter with all the context attacked to it in pure html
@login_required
def send_email(request):
    if request.user.is_staff or request.user.is_superuser:
        if request.method == 'POST':
            form = EmailForm(request.POST)
            if form.is_valid():
                # gets the submitted title and email and stores them in variables
                title = form.cleaned_data.get('title')
                email = form.cleaned_data.get('email')
                html_email = get_template(
                    'newsletter/newsletter.html')
                cnt = {'news1': News.objects.all(),
                       'release1': Release.objects.all(),
                       'future1': Future.objects.all(),
                       'Installs1': Installs.objects.all(),
                       'date': DATE, }
                # renders html email with the given context
                html_cont = html_email.render(cnt)
                # optimizes the email by removing spaces and comments
                html_cont = htmlmin.minify(
                    html_cont, remove_all_empty_space=True, remove_comments=True)
                # creates the email by attaching title, content and email
                msg = EmailMessage(title, html_cont, to=[email])
                msg.content_subtype = "html"
                msg.send()
                messages.success(
                    request, f'The email was successfully sent to {email}!')
                return redirect('email')
        else:
            form = EmailForm()
            context = {'news1': News.objects.all(),
                       'release1': Release.objects.all(),
                       'future1': Future.objects.all(),
                       'Installs1': Installs.objects.all(),
                       'date': DATE,
                       'form': form}
        return render(request, 'newsletter/email_modules/send.html', context)
    else:
        return HttpResponse(
            "You do not have sufficient enough permission fo access this page.")


# template with all the needed functions and data for the form create and update pages
class NewsletterContext:

    def get_context_data(self, **kwargs):
        ctx = super(NewsletterContext, self).get_context_data(**kwargs)
        # had to make the names that got data from the database differnet than the database name
        # or when calling (e.g. news.id) will not work if not in a loop
        ctx['title'] = self.title
        ctx['news1'] = News.objects.all()
        ctx['release1'] = Release.objects.all()
        ctx['future1'] = Future.objects.all()
        ctx['installs1'] = Installs.objects.all()
        ctx['date'] = DATE
        return ctx

    def form_valid(self, form):
        response = super().form_valid(form)
        return response

    def get_success_url(self):
        return self.request.path


# template with all the needed functions and data needed to delete
class NewsletterDelete:

    def get(self, request, *args, **kwargs):
        return self.post(request, *args, **kwargs)

    def get_success_url(self):
        prev = self.request.META.get('HTTP_REFERER')
        # when you delete in the update view you have nothing to go back to so extra steps are needed
        if '/update/' in prev:
            if '/editview/' in prev:
                if 'news' in prev:
                    return reverse('news-edit')
                elif 'future' in prev:
                    return reverse('future-edit')
                elif 'data' in prev:
                    return reverse('data-edit')
                else:
                    return reverse('release-edit')
            else:
                if 'news' in prev:
                    return reverse('news')
                elif 'future' in prev:
                    return reverse('future')
                elif 'data' in prev:
                    return reverse('data')
                else:
                    return reverse('release')
        else:
            return prev


# needed for UserPassesTestMixin: authenticates if user can update or delete the post
class UserAuth:
    def test_func(self):
        post = self.get_object()
        auth = self.request.user
        if auth == post.author or auth.is_superuser or auth.is_staff:
            return True
        return False


# when post is created login in users gets added to author column of that post
class InsertAuth:
    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

# News views


class NewsCreateView(NewsletterContext, InsertAuth, LoginRequiredMixin, CreateView):
    model = News
    fields = ['content']
    title = "New Highlights"


class NewsUpdateView(NewsletterContext, UserAuth, UserPassesTestMixin, LoginRequiredMixin, UpdateView):
    model = News
    fields = ['content']
    title = "New Highlights"


class NewsDeleteView(NewsletterDelete, UserAuth, UserPassesTestMixin, LoginRequiredMixin, DeleteView):
    model = News


# Release views
class ReleaseCreateView(NewsletterContext, InsertAuth, LoginRequiredMixin, CreateView):
    model = Release
    fields = ['title', 'link', 'content']
    title = "Release Status"


class ReleaseUpdateView(NewsletterContext, LoginRequiredMixin, UpdateView):
    model = Release
    fields = ['title', 'link', 'content']
    title = "Release Status"


class ReleaseDeleteView(NewsletterDelete, UserAuth, UserPassesTestMixin, LoginRequiredMixin, DeleteView):
    model = Release


# Future views
class FutureCreateView(NewsletterContext, InsertAuth, LoginRequiredMixin, CreateView):
    model = Future
    fields = ['title', 'link', 'content']
    title = "Future Releases"


class FutureUpdateView(NewsletterContext, UserAuth, UserPassesTestMixin, LoginRequiredMixin, UpdateView):
    model = Future
    fields = ['title', 'link', 'content']
    title = "Future Releases"


class FutureDeleteView(NewsletterDelete, UserAuth, UserPassesTestMixin, LoginRequiredMixin, DeleteView):
    model = Future


# Data views
class InstallsCreateView(NewsletterContext, InsertAuth, LoginRequiredMixin, CreateView):
    model = Installs
    fields = ['content']
    title = "Installs & Users"


class InstallsUpdateView(NewsletterContext, UserAuth, UserPassesTestMixin, LoginRequiredMixin, UpdateView):
    model = Installs
    fields = ['content']
    title = "Installs & Users"


class InstallsDeleteView(NewsletterDelete, UserAuth, UserPassesTestMixin, LoginRequiredMixin, DeleteView):
    model = Installs
