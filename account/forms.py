from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm
from .models import User

class custom_user_creation_form(UserCreationForm):
    class Meta:
      model = User
      fields = ['email', 'username', 'phone', 'occupation', 'company', 'bio', 'profile_picture', 'password1', 'password2']
      labels = {
        'email': '',
        'username': '',
        'phone': '',
        'occupation': '',
        'company': '',
        'bio': '',
        'profile_picture': 'Profile Picture',
        'password1': '',
        'password2': '',
      }

    def __init__(self, *args, **kwargs):
      super(custom_user_creation_form, self).__init__(*args, **kwargs)

      placeholders = {
        'email': 'Email',
        'username': 'Username',
        'phone': 'Phone Number',
        'occupation': 'Occupation',
        'company': 'Company',
        'bio': 'Bio',
        'password1': 'Password',
        'password2': 'Confirm Password',
      }

      for field_name, placeholder_text in placeholders.items():
        self.fields[field_name].widget.attrs['placeholder'] = placeholder_text







# class custom_user_creation_form(UserCreationForm):

#   class Meta:
#     model = User
#     fields = ['email', 'username', 'phone', 'occupation', 'company', 'bio',
#                'profile_picture','password1', 'password2']

#     labels = {
#       'email': '',
#       'username':'',
#       'phone': '',
#       'occupation':'',
#       'company':'',
#       'bio':'',
#       'profile_picture': 'profile picture',
#       'password1':'',
#       'password2':'',
#     }

#     def __init__(self, *args, **kwargs):
#       super(custom_user_creation_form, self).__init__(*args, **kwargs)






