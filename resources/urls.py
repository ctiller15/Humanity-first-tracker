from django.urls import path
from resources import views

urlpatterns = [
    path('', views.resources, name='resources')
]
