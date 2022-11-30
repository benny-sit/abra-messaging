from django.urls import path
from . import views
from rest_framework.authtoken import views as auth_views

urlpatterns = [
    path('', views.get_users, name="all-users"),
    path('register', views.create_user, name="api-register"),
    path('get-token', auth_views.obtain_auth_token, name="api-auth-token")
]