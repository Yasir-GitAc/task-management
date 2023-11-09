from django.urls import path
from . import views

app_name = 'task'

urlpatterns = [
  path('user-workspace/', views.user_workspace, name='user-workspace'),
  path('get-task-info-based-on-status/<str:status>/',
    views.get_task_info_based_on_status,
    name='get-task-info-based-on-status'
  ),
  path('get-task-info-for-task-modal/<int:id>/',
    views.get_task_info_for_task_modal,
    name='get-task-info-for-task-modal'
  ),
  path('show-company-list/', views.show_company_list, name='show-company-list'),
  path('create-task/<int:c_id>/', views.create_task, name='create-task'),
  path('edit-task/<int:id>/', views.edit_task, name='edit-task'),
  path('delete-task/<int:id>/', views.delete_task, name='delete-task'),
  path('confirm-delete-task/<int:id>/', views.confirm_delete_task, name='confirm-delete-task'),
]

 # path('view-task/', views.view_task, name='view-task'),
 # path('get-task-information/', views.get_task_information, name='get-task-information'),