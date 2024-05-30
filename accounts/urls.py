from django.urls import path
from . import views

urlpatterns = [
    path('/dashboard', views.Dashboard.as_view(), name='dashboard'),
    path('/login', views.UserLogin.as_view(), name='login'),
    path('/logout', views.UserLogout.as_view(), name='logout'),
    path('/reset-password', views.ResetPassword.as_view(), name='reset-password'),
    path('/', views.SignUp.as_view(), name='signup'),
]