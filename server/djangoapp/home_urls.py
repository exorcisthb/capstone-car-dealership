"""Home page URLs (root path)"""
from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='root_home'),
]
