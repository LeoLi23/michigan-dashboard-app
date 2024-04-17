from django.urls import path
from . import views

# URL patterns for homeApp
urlpatterns = [
    path('', views.homeView, name='homeView'),  # home view
]