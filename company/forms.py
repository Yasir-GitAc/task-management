from django.forms import ModelForm
from .models import Company


class Company_creation_form(ModelForm):
  class Meta:
    model = Company
    fields = ['name', 'company_logo', 'company_email', 'address', 'company_bio']

  def __init__(self, *args, **kwargs):
    super(Company_creation_form, self).__init__(*args, **kwargs)

    placeholders = {
      'name': 'Company Name',
      'company_logo': 'Company Logo',
      'company_email': 'Company Email',
      'address': 'Address',
      'company_bio': 'Company Bio',
    }

    for field_name, placeholder_text in placeholders.items():
      self.fields[field_name].widget.attrs['placeholder'] = placeholder_text

