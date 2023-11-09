from django.urls import path
from . import views

app_name = 'account'

urlpatterns = [
  path('login/',views.login_user, name='login'),
  path('logout/',views.logout_user, name='logout'),
  path('sign-up/', views.signup, name='signup'),
  path('user-profile/<int:pk>/', views.user_profile, name='user-profile'),
  path('update-user-profile/<int:pk>/', views.update_user_profile, name='update-user-profile'),
]
