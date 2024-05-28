from django.urls import path
from . import views

app_name = 'accounts'

urlpatterns = [
    path('', views.login_signup, name='login_signup'),
]
