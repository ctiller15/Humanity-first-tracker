from django.urls import path
from articles import views

urlpatterns = [
    path('', views.home, name='home')
]
