from django.contrib import admin
from django.urls import path, include

app_name = "DjTraders"


urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include("DjTraders.urls", namespace="DjTraders")),  # Main app
]
