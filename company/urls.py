from django.urls import path
from . import views

app_name = 'company'

urlpatterns = [
  path('company-workspace/<int:pk>/',views.company_workspace, name='company-workspace'),
  path('create-company/',views.create_company, name='create-company'),
  path('update-company/<int:pk>/',views.update_company, name='update-company'),
  path('delete-company/<int:company_id>/',views.delete_company, name='delete-company'),
  path('confirm-delete-company/<int:company_id>/',views.confirm_delete_company, name='confirm-delete-company'),
  path('leave-company/<int:company_id>/',views.leave_company, name='leave-company'),
  path('confirm-leave-company/<int:company_id>/',views.confirm_leave_company, name='confirm-leave-company'),
  path('company-profile/<int:pk>/',views.company_profile, name='company-profile'),
  path('users-list/<int:company_id>/',views.show_users_list, name='show-users-list'),

  path('show-created-company-list/<int:user_id>/', views.show_created_company_list, name='show-created-company-list'),

  path('send-add-request-from-profile/<int:company_id>/<int:user_id>/',views.send_add_request_from_profile, name='send-add-request-from-profile'),
  path('send-add-request/<int:company_id>/<int:user_id>/',views.send_add_request, name='send-add-request'),
  path('cancel-add-request/<int:company_id>/<int:user_id>/',views.cancel_add_request, name='cancel-add-request'),
  path('accept-add-request/<int:company_id>/<int:user_id>/',views.accept_add_request, name='accept-add-request'),
  path('confirm-add-request-accept/<int:company_id>/<int:user_id>/',views.confirm_add_request_accept, name='confirm-add-request-accept'),

  path('notifications/', views.notifications, name='notifications'),

  path('company-settings/<int:pk>/', views.company_settings, name='company-settings'),
  path('show-task-list/<int:pk>/', views.show_task_list, name='show-task-list'),
  path('show-member-list/<int:pk>/', views.show_member_list, name='show-member-list'),
  path('remove-member/<int:company_id>/<int:user_id>/', views.remove_member, name='remove-member'),
  path('confirm-remove-member/<int:company_id>/<int:user_id>/', views.confirm_remove_member, name='confirm-remove-member'),
]
