from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

app_name = 'users'
urlpatterns = [
  path('log_in/', views.CustomLoginView.as_view(), name='login' ),
  path('sign_up/', views.SignUpView.as_view(), name='signup'),
  path('log_out/', auth_views.LogoutView.as_view(), name='logout'),
]