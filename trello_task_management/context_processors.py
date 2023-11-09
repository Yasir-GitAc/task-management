from company.models import Company, Notification

def custom_context(request):
  user = request.user
  if request.user.is_authenticated:

    users_company = Company.objects.filter(creator=user)
    notifications = Notification.objects.filter(receivers=user)

    ntf_of_company = Notification.objects.none()
    for company in users_company:
      ntf = Notification.objects.filter(company_receivers=company)
      ntf_of_company = ntf_of_company | ntf

    ntf_of_company = ntf_of_company | notifications
    all_ntf_of_user = ntf_of_company.distinct()

    ntf_list = []
    for ntf in all_ntf_of_user:
      if ntf.seen == False:
        ntf_list.append(ntf)

    unseen_ntf = len(ntf_list)
  else:
    unseen_ntf = ''

  return {
    'my_custom_variable': unseen_ntf,
  }
