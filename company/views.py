from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q
from .models import Company, Membership, Notification
from .forms import Company_creation_form
from account.models import User

@login_required(login_url='account:login')
def company_workspace(request, pk):
  company = Company.objects.get(pk=pk)
  members = company.members.all()[:3]
  tasks = company.task_set.all()
  print('company',company)
  print('member',members)
  print('tasks',tasks)

  ongoing_task_list = []
  unstarted_task_list = []
  unassigned_task_list = []
  finished_task_list = []

  for task in tasks:
    if task.status == 'ongoing':
      print('ong_task',task)
      ongoing_task_list.append(task)
    elif task.status == 'unstarted':
      print('unst_task',task)
      unstarted_task_list.append(task)
    elif task.status == 'unassigned':
      print('unass_task',task)
      unassigned_task_list.append(task)
    elif task.status == 'finished':
      print('fin_task',task)
      finished_task_list.append(task)

  context = {
    'company':company,
    'members':members,
    'ongoing_task_list':ongoing_task_list,
    'unstarted_task_list':unstarted_task_list,
    'unassigned_task_list':unassigned_task_list,
    'finished_task_list':finished_task_list,
  }
  return render(request, 'company/company-workspace.html', context)


@login_required(login_url='account:login')
def company_profile(request, pk):
  company= Company.objects.get(pk=pk)
  company_members = company.members.all()
  company_tasks = company.task_set.all()

  task_list = []

  for t in company_tasks:
    task_assignees =  t.assignee.all()[:3]
    task = {
      'id':t.id,
      'title':t.title,
      'date_created':t.date_created,
      'status':t.status,
      'priority':t.priority,
      'assignees':task_assignees,
    }
    task_list.append(task)


  members_list = []

  for m in company_members:
    member_joined_date = m.membership_set.filter(company=company).first()
    total_finished_task = company.task_set.filter(assignee=m, status='finished').count()
    joined_date = member_joined_date.joined_date

    member = {
      'member_id':m.id,
      'member_joined_date':joined_date,
      'member_name': m.username,
      'member_total_finished_task':total_finished_task,
    }
    members_list.append(member)

  context = {
    'company':company,
    'member_list':members_list,
    'task_list':task_list,
  }
  return render(request, 'company/company-profile-view.html', context)


@login_required(login_url='account:login')
def company_settings(request, pk):
  company = Company.objects.get(pk=pk)
  context = {
    'company':company
  }
  return render(request, 'company/company-settings.html',context)

@login_required(login_url='account:login')
def show_task_list(request, pk):
  company = Company.objects.get(pk=pk)
  task_list = company.task_set.all()
  print(task_list)
  context = {
    'company':company,
    'task_list':task_list,
  }
  return render(request, 'company/show-task-list.html', context)


@login_required(login_url='account:login')
def show_member_list(request, pk):
  company = Company.objects.get(pk=pk)
  company_members = company.members.all()
  print(company_members)

  members_list = []

  for m in company_members:
    member_joined_date = m.membership_set.filter(company=company).first()
    total_finished_task = company.task_set.filter(assignee=m, status='finished').count()
    joined_date = member_joined_date.joined_date

    member = {
      'id':m.id,
      'name': m.username,
      'profile_picture_url':m.profile_picture.url,
      'bio':m.bio,
      'joined_date':joined_date,
      'total_finished_task':total_finished_task,
    }
    members_list.append(member)

  print('members_list',members_list)
  context = {
    'company':company,
    'members_list':members_list,
  }
  return render(request, 'company/show-member-list.html', context)


@login_required(login_url='account:login')
def remove_member(request, company_id, user_id):
  user = User.objects.get(pk=user_id)
  company = Company.objects.get(pk=company_id)
  total_finished_task = company.task_set.filter(assignee=user, status='finished').count()
  try:
    membership= Membership.objects.get(user=user,company=company)
    data_joined = membership.joined_date
  except:
    data_joined = ''

  context = {
    'company_id':company_id,
    'user':user,
    'date_joined':data_joined,
    'total_finished_task':total_finished_task,
  }
  return render(request, 'company/confirm_member_removal.html', context)


@login_required(login_url='account:login')
def confirm_remove_member(request, company_id, user_id):
  user = User.objects.get(pk=user_id)
  company = Company.objects.get(pk=company_id)
  print('cmb',company.members.all())
  company.members.remove(user)
  print('cm',company.members.all())

  try:
    membership = Membership.objects.get(user=user, company=company)
    print('mm',membership)
    membership.delete()
  except:
    membership = None;

  print(membership)
  messages.warning(request, 'Member removed')
  return redirect('company:show-member-list', pk=company_id)


@login_required(login_url='account:login')
def create_company(request):
  form = Company_creation_form()

  if request.method == 'POST':
    form = Company_creation_form(request.POST, request.FILES)
    # form = Task_creation_form(user=user, data=request.POST, files=request.FILES)
    if form.is_valid():
      var = form.save(commit=False)
      var.creator = request.user
      var.save()
      company_email = form.cleaned_data['company_email']
      company = Company.objects.get(company_email = company_email)
      id = company.id
      messages.success(request, 'Company created successfully')
      return redirect('company:company-workspace', pk=id)

  context = {
    'form':form
  }
  return render(request,'company/create-company-form.html', context)

@login_required(login_url='account:login')
def update_company(request, pk):
  company = Company.objects.get(pk=pk)
  form = Company_creation_form(instance=company)

  if request.method == 'POST':
    form = Company_creation_form(request.POST, request.FILES, instance=company)

    if form.is_valid():
      var = form.save(commit=False)
      var.creator = request.user
      var.save()
      company_email = form.cleaned_data['company_email']
      company = Company.objects.get(company_email = company_email)
      id = company.id
      messages.success(request, 'Company updated successfully')
      return redirect('company:company-profile', pk=id)

  context = {
    'form':form
  }
  return render(request,'company/create-company-form.html', context)



@login_required(login_url='account:login')
def delete_company(request, company_id):
  company = Company.objects.get(pk=company_id)
  context = {
    'company':company,
  }
  return render(request, 'company/delete-company.html',context)

@login_required(login_url='account:login')
def confirm_delete_company(request, company_id):
  company = Company.objects.get(pk=company_id)
  company.delete()

  messages.warning(request, 'Company Deleted')
  return redirect('task:user-workspace')

@login_required(login_url='account:login')
def leave_company(request, company_id, user_id):
  company = Company.objects.get(pk=company_id)
  context = {
    'company':company,
    'user_id':user_id,
  }
  return render(request, 'company/leave-company.html',context)


@login_required(login_url='account:login')
def confirm_leave_company(request, company_id, user_id):
  company = Company.objects.get(pk=company_id)
  context = {
    'company':company,
    'user_id':user_id,
  }
  return redirect('task:user-workspace')


@login_required(login_url='account:login')
def show_users_list(request, company_id):
  logged_in_user_id =request.user.id
  user_list = User.objects.exclude(id=logged_in_user_id)
  company = Company.objects.get(pk=company_id)

  req_receivers_list = []
  company_members_list = []

  for user in user_list:
    add_req_exist = Notification.objects.filter(company_sender=company, receivers=user)
    if add_req_exist:
      req_receivers_list.append(user)

    if user in company.members.all():
      print('user in company')
      company_members_list.append(user)
    else:
      print('user is not in company')

  print(company_members_list)
  context = {
    'user_list':user_list,
    'company_id':company_id,
    'req_receivers_list':req_receivers_list,
    'company_members_list':company_members_list,
  }
  return render(request, 'company/show-users-list.html', context)


@login_required(login_url='account:login')
def show_created_company_list(request, user_id):
  user = request.user
  user_companies = Company.objects.filter(creator=user)

  context = {
    'user_companies':user_companies,
    'user_id':user_id,
  }
  return render(request, 'company/show-created-company-list.html', context)



@login_required(login_url='account:login')
def send_add_request(request, company_id, user_id):
  user_receiver = User.objects.get(pk=user_id)
  company_sender = Company.objects.get(pk=company_id)
  exist_notification = Notification.objects.filter(company_sender=company_sender, receivers=user_receiver)

  if not exist_notification:

    title =  "Add Request"
    subject = f"{company_sender.name} sent you add request"

    notification = Notification.objects.create(
      type = "addrequest",
      title = title,
      subject = subject,
      company_sender = company_sender,
    )
    notification.receivers.set([user_receiver])

    mgs = f"add request sent to {user_receiver.username}"

    messages.success(request, mgs)
    return redirect('company:show-users-list', company_id = company_id)
  else:
    messages.success(request, 'add request already sent')
    return redirect('company:show-users-list', company_id = company_id)


@login_required(login_url='account:login')
def send_add_request_from_profile(request, company_id, user_id):
  user_receiver = User.objects.get(pk=user_id)
  company_sender = Company.objects.get(pk=company_id)
  exist_notification = Notification.objects.filter(company_sender=company_sender, receivers=user_receiver)

  if not exist_notification:

    title =  "Add Request"
    subject = f"{company_sender.name} sent you add request"

    notification = Notification.objects.create(
      type = "addrequest",
      title = title,
      subject = subject,
      company_sender = company_sender,
    )
    notification.receivers.set([user_receiver])

    mgs = f"add request sent to {user_receiver.username}"

    messages.success(request, mgs)
    return redirect('account:user-profile', pk=user_id)
  else:
    messages.success(request, 'add request already sent')
    return redirect('account:user-profile', pk=user_id)


@login_required(login_url='account:login')
def cancel_add_request(request, company_id, user_id):
  user_receiver = User.objects.get(pk=user_id)
  company_sender = Company.objects.get(pk=company_id)
  notification = Notification.objects.filter(company_sender=company_sender, receivers=user_receiver)

  mgs = f"add request to {user_receiver.username} canceled"
  notification.delete()

  messages.warning(request, mgs)
  return redirect('company:show-users-list', company_id = company_id)

# accept a new ntf of accepting , delete sent
@login_required(login_url='account:login')
def accept_add_request(request, company_id, user_id):
  company = Company.objects.get(pk=company_id)
  print(company)
  context ={
    'company':company,
    'user_id':user_id,
  }
  return render(request, 'company/accept-add-req.html',context)

@login_required(login_url='account:login')
def confirm_add_request_accept(request, company_id, user_id):
  company = Company.objects.get(pk=company_id)
  user = User.objects.get(pk=user_id)
  ntf = Notification.objects.get(company_sender=company, receivers=user)

  company.members.add(user)
  ntf.delete()

  title = 'add request accepted'
  subject = f"{user.username} accepted {company.name} add request. User is now added to {company.name}"

  accept_ntf = Notification.objects.create(
    type = 'requestaccept',
    title = title,
    subject = subject,
    sender = user,
  )
  accept_ntf.company_receivers.set([company])

  messages.success(request, f"You are now member of {company.name}")
  return redirect('company:company-profile', pk=company_id)


@login_required(login_url='account:login')
def notifications(request):
  user = request.user
  users_company = Company.objects.filter(creator=user)
  notifications = Notification.objects.filter(receivers=user)

  ntf_of_company = Notification.objects.none()
  for company in users_company:
    ntf = Notification.objects.filter(company_receivers=company)
    ntf_of_company = ntf_of_company | ntf

  ntf_of_company = ntf_of_company | notifications

  for ntf in ntf_of_company:
    if ntf.seen == False:
      ntf.seen = True
      ntf.save()

  all_ntf_of_user = ntf_of_company.distinct() #include both com to user and user to com

  context = {
    'all_ntf_of_user':all_ntf_of_user,
  }
  return render(request, 'company/notifications.html', context)

