from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.utils.translation import gettext_lazy as _
from .models import User


class UserAdmin(BaseUserAdmin):
  ordering = ['-joined']
  list_display = ['username', 'email']
  fieldsets = (
    (None, {'fields':('email', 'username', 'password')}),
    (_('Personal information'), {
      'fields':(
        'phone',
        'occupation',
        'company',
        'bio',
        'profile_picture',
      )
    }),
    (_('Permissions'),
     {
       'fields':(
         'is_active',
         'is_staff',
         'is_superuser',
       )
     }),
     (_('Important dates'), {'fields':('last_login',)}),
  )
  readonly_fields = ['last_login']
  add_fieldsets = (
    (None, {
      'classes':('wide',),
      'fields': (
        'email',
        'username',
        'phone',
        'occupation',
        'company',
        'bio',
        'profile_picture',
        'password1',
        'password2',
        'is_active',
        'is_staff',
        'is_superuser',
      )
    }),
  )


admin.site.register(User, UserAdmin)