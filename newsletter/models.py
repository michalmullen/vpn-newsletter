from django.db import models
from django.contrib.auth.models import User
from tinymce import HTMLField
from django.conf import settings


class News(models.Model):
    content = HTMLField('Content')
    author = models.ForeignKey(settings.AUTH_USER_MODEL,
                               on_delete=models.CASCADE)

    def __str__(self):
        return self.content


class Release(models.Model):
    title = models.CharField(max_length=100)
    link = models.CharField(max_length=100)
    content = HTMLField('Content')
    author = models.ForeignKey(settings.AUTH_USER_MODEL,
                               on_delete=models.CASCADE)

    def __str__(self):
        return self.title


class Future(models.Model):
    title = models.CharField(max_length=100)
    link = models.CharField(max_length=100)
    content = HTMLField('Content')
    author = models.ForeignKey(settings.AUTH_USER_MODEL,
                               on_delete=models.CASCADE)

    def __str__(self):
        return self.title


class Installs(models.Model):
    content = HTMLField('Content')
    author = models.ForeignKey(settings.AUTH_USER_MODEL,
                               on_delete=models.CASCADE)

    def __str__(self):
        return self.content
