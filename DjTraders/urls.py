from django.urls import path
from . import views

app_name = 'DjTraders'

urlpatterns = [
    path('', views.index, name='index'),  # Home page view
    path('Products/', views.DjTradersProductsView.as_view(), name='Products'),
    path('Products/create/', views.create_product, name='ProductCreate'),
    path('Products/update/<int:pk>/', views.update_product, name='ProductUpdate'),
    path('Products/status/<int:pk>/', views.update_product_status, name='ProductStatus'),
    path('Products/<int:pk>/', views.DjTradersProductDetailView.as_view(), name='ProductDetail'),  # Add this line
    path('Customers/', views.DjTradersCustomersView.as_view(), name='Customers'),
    path('Customers/create/', views.create_customer, name='CustomerCreate'),
    path('Customers/update/<int:pk>/', views.update_customer, name='CustomerUpdate'),
    path('Customers/status/<int:pk>/', views.update_customer_status, name='CustomerStatus'),
    path('Customers/<int:pk>/', views.DjTradersCustomerDetailView.as_view(), name='CustomerDetail'),
    path('Customers/archive/<int:pk>/', views.archive_customer, name='CustomerArchive'),
]