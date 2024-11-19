from django.urls import path
from . import views

app_name = "DjTraders"

urlpatterns = [
    path("", views.index, name="Home"),
    path("Customers/", views.DjTradersCustomersView.as_view(), name="Customers"),
    path(
        "CustomerDetail/<int:pk>/",
        views.DjTradersCustomerDetailView.as_view(),
        name="CustomerDetail",
    ),
    path("Products/", views.DjTradersProductsView.as_view(), name="Products"),
    path(
        "ProductDetail/<int:pk>/",
        views.DjTradersProductDetailView.as_view(),
        name="ProductDetail",
    ),
    path("CustomerCreate/", views.CustomerCreateView.as_view(), name="CustomerCreate"),
    path(
        "CustomerUpdate/<int:pk>/",
        views.CustomerEditView.as_view(),
        name="CustomerEditView",
    ),
]
