from django.urls import path
from articles import views

urlpatterns = [
    path('', views.home, name='home'),
    path('search_results', views.search_results, name='search_results')
]
