from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('DjTraders.urls', namespace='DjTraders')),  # Root URL with namespace
    path('DjTraders/', include('DjTraders.urls', namespace='DjTraders_alt')),  # Alternative URL with different namespace
]