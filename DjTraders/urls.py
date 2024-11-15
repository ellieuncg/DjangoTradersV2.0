from django.urls import path
from django.contrib.auth import views as auth_views
from . import views  # Import the views module
import logging

logger = logging.getLogger(__name__)
logger.info("Views imported: %s", dir(views))

app_name = 'DjTraders'

urlpatterns = [
    # Authentication URLs
    path('accounts/login/', views.custom_login_view, name='login'),
    path('accounts/logout/', auth_views.LogoutView.as_view(next_page='DjTraders:Index'), name='logout'),

    # Sales Dashboard
    path('sales/dashboard/', views.SalesDashboard, name='SalesDashboard'),

    # Main application view
    path('', views.index, name='Index'),

    # Customer Management URLs
    path('customers/', views.DjTradersCustomersView.as_view(), name='Customers'),
    path('customers/<int:pk>/', views.DjTradersCustomerDetailView.as_view(), name='CustomerDetail'),
    path('customers/create/', views.create_customer, name='CustomerCreate'),
    path('customers/<int:pk>/update/', views.update_customer, name='CustomerUpdate'),
    path('customers/<int:pk>/archive/', views.archive_customer, name='CustomerArchive'),

    # Customer Dashboard URL
    path('customers/<int:pk>/dashboard/', views.CustomerDashboard, name='CustomerDashboard'),

    # Product Management URLs
    path('products/', views.DjTradersProductsView.as_view(), name='Products'),
    path('products/<int:pk>/', views.DjTradersProductDetailView.as_view(), name='ProductDetail'),
    path('products/create/', views.create_product, name='ProductCreate'),
    path('products/<int:pk>/update/', views.update_product, name='ProductUpdate'),
    path('products/<int:pk>/archive/', views.archive_product, name='ProductArchive'),
]
