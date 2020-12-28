from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('resources/', include('resources.urls')),
    path('', include('articles.urls')),
]
