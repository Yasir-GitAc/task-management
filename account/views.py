from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from .models import User
from company.models import Company
from .forms import custom_user_creation_form

# Create your views here.

def take_a_tour(request):
  if request.method == 'POST':
    email = request.POST['email']
    password = request.POST['password']

    user = authenticate(request, email=email, password=password)
    if user is not None:
      login(request, user)
      messages.success(request, 'LogIn Successful'+ ' ' + user.username)
      # return redirect('account:index')
      return redirect('task:user-workspace')
    else:
      print('Credentials is not matching, please try again.')
      messages.error(request, 'Credentials do not match, please try again.')
      return redirect('account:login')

  return render(request, 'account/take_a_tour.html')


def login_user(request):
  if request.user.is_authenticated:
    messages.info(request, 'your are already logged in')
    return redirect('index')

  if request.method == 'POST':
    email = request.POST['email']
    password = request.POST['password']

    user = authenticate(request, email=email, password=password)
    if user is not None:
      login(request, user)
      messages.success(request, 'LogIn Successful'+ ' ' + user.username)
      # return redirect('account:index')
      return redirect('task:user-workspace')
    else:
      print('Credentials is not matching, please try again.')
      messages.error(request, 'Credentials do not match, please try again.')
      return redirect('account:login')

  return render(request, 'account/login.html')


@login_required(login_url='account:login')
def logout_user(request):
  logout(request)
  return redirect('index')


def signup(request):
  form = custom_user_creation_form()

  if request.user.is_authenticated:
    return redirect('index')

  if request.method == 'POST':
    form = custom_user_creation_form(request.POST, request.FILES)
    print('form-received')
    if form.is_valid():
      print('form-valid')
      form.save()
      print('form-saved')
      email = form.cleaned_data['email']
      password = form.cleaned_data['password1']
      user = authenticate(request, email=email, password=password)

      if user is not None:
        login(request, user)
        print('successful-login')
        messages.success(request, 'SignUp Successful')
        # return redirect('account:edit_profile', pk=user.profile_set.id)
        return redirect('task:user-workspace')
      else:
        messages.error(request, 'An error occured during signup, please try again')
        print('failed')
        return redirect('account:signup')

  context = {
    'form':form
  }
  return render(request, 'account/signup.html', context)


@login_required(login_url='account:login')
def user_profile(request, pk):
  user = User.objects.get(pk=pk)

  users_companies = user.created_companies.all()

  #companies user is a member
  companies_user_in = Company.objects.filter(members = user)

  context = {
    'user':user,
    'users_companies': users_companies,
    'companies_user_in': companies_user_in,
  }
  return render(request, 'account/user-profile-view.html', context)


@login_required(login_url='account:login')
def update_user_profile(request, pk):
  user = User.objects.get(pk=pk)
  form = custom_user_creation_form(instance=user)

  if request.method == "POST":
    form = custom_user_creation_form(request.POST, request.FILES, instance=user)

    if form.is_valid():
      form.save()

      email = form.cleaned_data['email']
      password = form.cleaned_data['password1']
      user = authenticate(request, email=email, password=password)
      if user is not None:
        login(request, user)
        print('successful-login')
        messages.success(request, 'Profile Updated')
        return redirect('account:user-profile', pk=pk)

  context = {
    'form':form,
  }
  return render(request, 'account/update-user-profile.html', context)
