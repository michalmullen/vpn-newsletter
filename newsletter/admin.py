from django.contrib import admin
from .models import Future, News, Release, Installs


admin.site.register(News)
admin.site.register(Future)
admin.site.register(Release)
admin.site.register(Installs)
