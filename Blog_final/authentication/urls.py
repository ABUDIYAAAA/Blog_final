from django.contrib import admin
from django.urls import path
from . import views
from .views import PasswordsChangeView, ProfileUpdateView
from django.contrib.auth import views as auth_views

app_name = 'authentication'

urlpatterns = [
    path('', views.home, name='home'),
    path('signup', views.signup, name='signup'),
    path('signin', views.signin, name='signin'),
    path('signout', views.signout, name='signout'),
    path('userprofile',views.ProfileView, name='profile'),
    #path('passwordchange/', auth_views.PasswordChangeView.as_view(template_name='authentication/password_change.html'), name='password_change'),
    path('passwordchange/', views.PasswordsChangeView.as_view(template_name='authentication/password_change.html'), name='password_change'),
    path('profilechange/<int:pk>', views.ProfileUpdateView.as_view(), name='profilechange'),
    # path('biochange/', views.profilebioupdate, name='biochange')
]
