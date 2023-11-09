from django import forms
from .models import Task
from account.models import User
from django.contrib.auth import get_user_model
from company.models import Company


class Task_creation_form(forms.ModelForm):

  def __init__(self, *args, **kwargs):
    user_id = kwargs.pop('user_id', None)
    company_id = kwargs.pop('company_id', None)
    super(Task_creation_form, self).__init__(*args, **kwargs)

    queryset = []

    user = User.objects.get(pk=user_id)
    users_company = Company.objects.filter(creator=user)

    queryset_non_distinct = user.company_members.all() | users_company #connecting two querysets
    queryset = queryset_non_distinct.distinct()

    company = Company.objects.get(pk=company_id)
    company_creator_id = company.creator.id
    company_creator = User.objects.filter(id=company_creator_id)
    print('company_creator', company_creator)
    assignee_qs_non_distinct = company.members.all() | company_creator
    assignee_qs = assignee_qs_non_distinct.distinct()

    self.fields['company'] = forms.ModelChoiceField(queryset=queryset) #don't touch
    self.initial['company'] = company_id
    self.fields['assignee'] = forms.ModelMultipleChoiceField(queryset=assignee_qs)

  class Meta:
    model = Task
    exclude = ["creator"]


# bug - only members of the company should be in the assignee,
# but this form bringing every user on bd, including Admin