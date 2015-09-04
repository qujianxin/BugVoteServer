from django.contrib import admin

# Register your models here.
from api import models

admin.site.register(models.Administration)
admin.site.register(models.BugRecord)
admin.site.register(models.Config)
admin.site.register(models.News)
admin.site.register(models.User)
admin.site.register(models.ImageItem)
admin.site.register(models.BugType)
