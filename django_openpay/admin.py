from django.contrib import admin
from . import models

# Register your models here.
admin.site.register(models.Address)
admin.site.register(models.Customer)
admin.site.register(models.Card)
admin.site.register(models.Plan)
admin.site.register(models.Subscription)
admin.site.register(models.Charge)
