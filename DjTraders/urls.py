from django.urls import path
from . import views
from .views import CustomerArchiveView  # Add this import

app_name = 'DjTraders'

urlpatterns = [
    path('', views.index, name='index'),
    path('Customers/', views.DjTradersCustomersView.as_view(), name='Customers'),
    path('Customers/create/', views.create_customer, name='CustomerCreate'),
    path('Customers/<int:pk>/', views.DjTradersCustomerDetailView.as_view(), name='CustomerDetail'),
    path('Customers/<int:pk>/update/', views.update_customer, name='CustomerUpdate'),
    path('Customers/<int:pk>/status/', views.update_customer_status, name='CustomerStatus'),
    path('Customers/<int:pk>/archive/', views.CustomerArchiveView.as_view(), name='CustomerArchive'),  # Use views.CustomerArchiveView
    
    path('Products/', views.DjTradersProductsView.as_view(), name='Products'),
    path('Products/create/', views.create_product, name='ProductCreate'),
    path('Products/<int:pk>/', views.DjTradersProductDetailView.as_view(), name='ProductDetail'),
    path('Products/<int:pk>/update/', views.update_product, name='ProductUpdate'),
    path('Products/<int:pk>/status/', views.update_product_status, name='ProductStatus'),
]