from django.urls import path
from . import views
from django.contrib.auth.views import LoginView
from django.contrib.auth.views import LogoutView

urlpatterns = [
    path('api/register/player/', views.RegisterPlayerView.as_view(), name='register-player'),
    path('api/register/manager/', views.RegisterManagerView.as_view(), name='register-manager'),
    path('', views.home_view, name='home'),
    path('fixtures/', views.fixture_view, name='fixtures'),
    path('register/', views.registration_view, name='register'),
]
