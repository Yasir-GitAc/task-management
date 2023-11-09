import json
from django.shortcuts import render,redirect
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.contrib import messages
from django.http import JsonResponse
from datetime import datetime
from .models import Task, Assignment
from .forms import Task_creation_form
from company.models import Company,Notification


@login_required(login_url='account:login')
def get_task_info_based_on_status(request, status):
  user = request.user
  status = status
  task_query = Task.objects.filter(assignee=user, status=status)

  task_list = []
  for t in task_query:
    task = {
      'finishing_expected': t.finishing_expected.strftime("%b %d, %Y, %I:%M %p"),
      'title':t.title,
      'task_id':t.id,
      'priority':t.priority,
      'company':t.company.name,
      'company_id':t.company.id
    }
    task_list.append(task)

  return JsonResponse({'data':task_list}, safe=False)


@login_required(login_url='account:login')
def get_task_info_for_task_modal(request, id):
  task = Task.objects.get(pk=id)

  assignee_list = []
  for a in task.assignee.all():
    assignee = {
      'assignee_id':a.id,
      'assignee_name':a.username,
      'assignee_img_url':a.profile_picture.url,
    }
    assignee_list.append(assignee)

  if task.finishing_date:
    finishing_date = task.finishing_date.strftime("%b %d, %Y, %I:%M %p"),
  else:
    finishing_date = None,

  data = [{
    'title':task.title,
    'status':task.status,
    'drescription':task.drescription,
    'priority':task.priority,
    'checklist':task.checklist,
    'company':task.company.name,
    'company_id':task.company.id,
    'company_logo_url':task.company.company_logo.url,
    'assignees':assignee_list,
    'finishing_expected':task.finishing_expected.strftime("%b %d, %Y, %I:%M %p"),
    'date_created':task.date_created.strftime("%b %d, %Y, %I:%M %p"),
    'finishing_date':finishing_date,
  },]
  return JsonResponse({'data':data}, safe=False )

#  cancelling their implementation to shortend dev time,
# use if to check null or not, then use below code, or response won't be ok
# 'last_updated':task.last_updated.strftime("%b %d, %Y, %I:%M %p"),
# 'finishing_date':task.finishing_date.strftime("%b %d, %Y, %I:%M %p"),

def user_workspace(request):
  tasks = Task.objects.filter(assignee=request.user, status='ongoing')
  context = {
    'tasks':tasks,
  }
  return render(request, 'task/user-workspace.html', context)


@login_required(login_url='account:login')
def show_company_list(request):
  user = request.user
  companies = Company.objects.filter(members=user)
  users_companies = Company.objects.filter(creator=user)

  context = {
    'companies':companies,
    'user_companies':users_companies,
  }
  return render(request, 'task/show-company-list.html', context)


@login_required(login_url='account:login')
def create_task(request, c_id):
  company_id = c_id
  form = Task_creation_form(user_id=request.user.id, company_id=company_id)

  if request.method == 'POST':
    form = Task_creation_form(user_id=request.user.id,company_id=company_id,data=request.POST)
    if form.is_valid():
      task = form.save(commit=False)
      task.creator = request.user

      if task.status == 'finished':
        task.finishing_date = datetime.today()

      task.save()

      company = form.cleaned_data['company']
      for user in form.cleaned_data['assignee']:
        Assignment.objects.create(user=user, task=task)
        title = 'Task Assignment'
        subject = f"{company.name} assigned you new Task."
        notification = Notification.objects.create(
          type = "assignment",
          title = title,
          subject = subject,
          company_sender = company,
        )
        notification.receivers.set([user])

      messages.success(request, 'Task Created Successfully')
      return redirect('task:user-workspace')

  context = {
    'form':form
  }
  return render(request, 'task/create-task-form.html', context)


@login_required(login_url='account:login')
def edit_task(request, id):
  task = Task.objects.get(pk=id)
  user_id = request.user.id
  company_id =task.company.id
  form = Task_creation_form(user_id=user_id,company_id=company_id,instance=task)

  if request.method == "POST":
    form = Task_creation_form(user_id=user_id,company_id=company_id,data=request.POST, instance=task)

    if form.is_valid():
      task = form.save(commit=False)

      if task.status == 'finished':
        task.finishing_date = datetime.today()

      task.save()
      company = form.cleaned_data['company']
      for user in form.cleaned_data['assignee']:
        try:
          assignment = Assignment.objects.get(user=user, task=task)
        except:
          assignment = None

        if assignment is None:
          Assignment.objects.create(user=user, task=task)
          title = 'Task Assignment'
          subject = f"{company.name} assigned you new Task."
          notification = Notification.objects.create(
            type = "assignment",
            title = title,
            subject = subject,
            company_sender = company,
          )
          notification.receivers.set([user])

      messages.success(request, 'Task Updated')
      return redirect('task:user-workspace')

  context = {
    'form':form,
  }
  return render(request, 'task/create-task-form.html', context)


@login_required(login_url='account:login')
def delete_task(request, id):
  task = Task.objects.get(pk=id)

  context = {
    'task':task,
  }
  return render(request, 'task/delete-task.html', context)

@login_required(login_url='account:login')
def confirm_delete_task(request, id):
  task= Task.objects.get(pk=id)
  task.delete()
  messages.warning(request, 'Task deleted')
  return redirect(request.GET['next'] if 'next' in request.GET else 'task:user-workspace')


