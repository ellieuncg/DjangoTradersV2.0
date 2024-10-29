# DjangoTraders/urls.py
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('DjTraders.urls')),  # Root URL points to DjTraders app
    path('DjTraders/', include('DjTraders.urls', namespace='DjTraders_alt')),  # Add unique namespace
]