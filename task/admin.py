from django.contrib import admin
from .models import Task, Assignment
from django.contrib import admin

class TaskAdmin(admin.ModelAdmin):
  list_display = ('title', 'priority', 'status', 'creator', 'date_created', 'finishing_expected')
  list_filter = ('priority', 'status', 'creator', 'company')

  search_fields = ('title', 'creator__username', 'company__name')  # Add fields to search
  list_per_page = 20  # Number of items to display per page

admin.site.register(Task, TaskAdmin)
admin.site.register(Assignment)
