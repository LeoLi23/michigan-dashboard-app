from django.urls import path
from . import views

# URL patterns for the airQualityApp
urlpatterns = [
    path('', views.mapView, name='mapView'),  # map view
]

