from django.shortcuts import render,redirect
from account.models import User
from company.models import Company
from task.models import Task
from django.db.models import Q

# Create your views here.

def index(request):
  if request.user.is_authenticated:
    return redirect('task:user-workspace')
  else:
    return render(request, 'index.html')


def search_result(request):
  search_query = ''

  if request.GET.get('search_query'):
    search_query = request.GET.get('search_query')

    companies = Company.objects.filter(
      Q(name__icontains = search_query)|
      Q(company_bio__icontains = search_query)
    )
    user_list = User.objects.filter(
      Q(username__icontains=search_query)|
      Q(bio__icontains = search_query)|
      Q(occupation__icontains = search_query)
    )

  context = {
    'companies':companies,
    'user_list':user_list,
  }

  return render(request, 'search-results.html', context)