from django.urls import path
from . import views

urlpatterns = [
    path('', views.keyword_tool_view, name='keyword_tool_view'),
]

