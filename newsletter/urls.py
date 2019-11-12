from django.urls import path

from . import views
from .views import NewsCreateView, ReleaseCreateView, FutureCreateView, InstallsCreateView, NewsUpdateView, FutureUpdateView, ReleaseUpdateView, InstallsUpdateView, NewsDeleteView, FutureDeleteView, ReleaseDeleteView, InstallsDeleteView, send_email

urlpatterns = [
    # home page
    path('', NewsCreateView.as_view(
        template_name="newsletter/home.html"), name='home'),
    # edit home page
    path('edit/', NewsCreateView.as_view(
        template_name="newsletter/home_edit.html"), name='edit'),
    # send email
    path('email/', views.send_email, name='email'),
    # send email
    path('email/reset/', views.reset_email, name='reset'),
    # create page with final view
    path('news/', NewsCreateView.as_view(
        template_name="newsletter/add.html"), name='news'),
    path('release/', ReleaseCreateView.as_view(
        template_name="newsletter/add.html"), name='release'),
    path('future/', FutureCreateView.as_view(
        template_name="newsletter/add.html"), name='future'),
    path('installs/', InstallsCreateView.as_view(
        template_name="newsletter/add.html"), name='installs'),
    # create page with edit view
    path('news/editview/', NewsCreateView.as_view(
        template_name="newsletter/add_edit.html"), name='news-edit'),
    path('release/editview/', ReleaseCreateView.as_view(
        template_name="newsletter/add_edit.html"), name='release-edit'),
    path('future/editview/', FutureCreateView.as_view(
        template_name="newsletter/add_edit.html"), name='future-edit'),
    path('installs/editview/', InstallsCreateView.as_view(
        template_name="newsletter/add_edit.html"), name='installs-edit'),
    # update page with final view
    path('news/<int:pk>/update/',
         NewsUpdateView.as_view(template_name="newsletter/update.html"), name='news-update'),
    path('release/<int:pk>/update/',
         ReleaseUpdateView.as_view(template_name="newsletter/update.html"), name='release-update'),
    path('future/<int:pk>/update/',
         FutureUpdateView.as_view(template_name="newsletter/update.html"), name='future-update'),
    path('installs/<int:pk>/update/',
         InstallsUpdateView.as_view(template_name="newsletter/update.html"), name='instals-update'),
    # update page with edit view
    path('news/<int:pk>/update/editview/',
         NewsUpdateView.as_view(template_name="newsletter/update_edit.html"), name='news-update-edit'),
    path('release/<int:pk>/update/editview/',
         ReleaseUpdateView.as_view(template_name="newsletter/update_edit.html"), name='release-update-edit'),
    path('future/<int:pk>/update/editview/',
         FutureUpdateView.as_view(template_name="newsletter/update_edit.html"), name='future-update-edit'),
    path('installs/<int:pk>/update/editview/',
         InstallsUpdateView.as_view(template_name="newsletter/update_edit.html"), name='installs-update-edit'),
    # delete
    path('news/<int:pk>/delete/', NewsDeleteView.as_view(), name='news-delete'),
    path('release/<int:pk>/delete/',
         ReleaseDeleteView.as_view(), name='release-delete'),
    path('future/<int:pk>/delete/',
         FutureDeleteView.as_view(), name='future-delete'),
    path('installs/<int:pk>/delete/',
         InstallsDeleteView.as_view(), name='installs-delete'),
]
