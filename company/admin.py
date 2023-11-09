from django.contrib import admin
from .models import Company, Membership,Notification

admin.site.register(Company)
admin.site.register(Membership)
admin.site.register(Notification)
