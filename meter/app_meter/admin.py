from django.contrib import admin
from . import models

admin.site.register(models.Meter)
admin.site.register(models.Resource)
admin.site.register(models.Record)
admin.site.register(models.Unit)
