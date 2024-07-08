from django.contrib.auth import views as auth_views
from django.urls import path

from . import views

urlpatterns = [
    path('', views.frontpage, name='frontpage'),
    path('signup/', views.signUp, name='signup'),
    # In Django, the LoginView and LogoutView are class-based views provided by Django's authentication system.Django's authentication framework includes built-in class-based views for common authentication tasks like login and logout.
    path('login/', auth_views.LoginView.as_view(template_name='core/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name="logout"),
]
