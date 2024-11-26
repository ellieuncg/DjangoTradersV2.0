from django.contrib import admin
from django.urls import path
from DjTraders import views
from django.contrib.auth.views import LogoutView
from django.contrib.auth.views import LoginView



app_name = 'DjTraders'

urlpatterns = [
    # Admin route
    path('admin/', admin.site.urls),

    # Home route
    path('', views.index, name='index'),

    # SalesDashboard (old) route
    path('salesdashboard/', views.SalesDashboard, name='SalesDashboard'),

    # SalesDash (new) route
    path('salesdash/', views.SalesDash, name='SalesDash'),

    # Additional routes
    path('customers/', views.CustomersListView.as_view(), name='Customers'),
    path('customer/<int:pk>/', views.DjTradersCustomerDetailView.as_view(), name='CustomerDetail'),
    path('customer/<int:pk>/update/', views.update_customer, name='UpdateCustomer'),
    path('customer/<int:pk>/archive/', views.archive_customer, name='ArchiveCustomer'),

    # API endpoints for dashboard data
    path('api/sales-dashboard-data/', views.get_sales_dashboard_data, name='SalesDashboardData'),

    # Client dashboard route
    path('client_dashboard/', views.client_dashboard, name='client_dashboard'),

    
     path("products/", views.DjTradersProductsView.as_view(), name="Products"),
    path(
        "products/<int:pk>/",
        views.DjTradersProductDetailView.as_view(),
        name="ProductDetail",
    ),
    path("products/create/", views.create_product, name="ProductCreate"),
    path("products/<int:pk>/update/", views.update_product, name="ProductUpdate"),
    path("products/<int:pk>/archive/", views.archive_product, name="ProductArchive"),
    path(
        "products/<int:pk>/status/", views.update_product_status, name="ProductStatus"
    ),
    
    path('login/', LoginView.as_view(template_name='DjTraders/login.html'), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    
    path('transaction_dashboard/', views.TransactionDashboardView.as_view(), name='transaction_dashboard'),

]
