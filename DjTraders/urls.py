from django.urls import path
from . import views

app_name = 'DjTraders'  # This should match the primary namespace

urlpatterns = [
    path('', views.index, name='Index'),
    
    # Customer URLs
    path('customers/', views.DjTradersCustomersView.as_view(), name='Customers'),
    path('customers/<int:pk>/', views.DjTradersCustomerDetailView.as_view(), name='CustomerDetail'),
    path('customers/create/', views.create_customer, name='CustomerCreate'),
    path('customers/<int:pk>/update/', views.update_customer, name='CustomerUpdate'),
    path('customers/<int:pk>/status/', views.update_customer_status, name='CustomerStatus'),
    path('customers/<int:pk>/archive/', views.CustomerArchiveView.as_view(), name='CustomerArchive'),
    
    # Product URLs
    path('products/', views.DjTradersProductsView.as_view(), name='Products'),
    path('products/<int:pk>/', views.DjTradersProductDetailView.as_view(), name='ProductDetail'),
    path('products/create/', views.create_product, name='ProductCreate'),
    path('products/<int:pk>/update/', views.update_product, name='ProductUpdate'),
    path('products/<int:pk>/status/', views.update_product_status, name='ProductStatus'),
]