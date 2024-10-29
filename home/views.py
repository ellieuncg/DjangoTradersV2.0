from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import DetailView, ListView, UpdateView, CreateView
from django.urls import reverse_lazy
from .forms import CustomerForm
from .models import Customer, Product, Order, OrderDetail, Category

# Home view
def index(request):
    return render(request, 'DjTraders/index.html')

# Customers view
class DjTradersCustomersView(ListView):
    model = Customer
    template_name = 'DjTraders/customers.html'
    context_object_name = 'customers'

# Customer detail view
class DjTradersCustomerDetailView(DetailView):
    model = Customer
    template_name = 'DjTraders/CustomerDetail.html'
    context_object_name = 'customer'

# Products view
class DjTradersProductsView(ListView):
    model = Product
    template_name = 'DjTraders/Products.html'
    context_object_name = 'products'

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = Category.objects.all()
        return context

# Product detail view
class DjTradersProductDetailView(DetailView):
    model = Product
    template_name = 'DjTraders/ProductDetail.html'
    context_object_name = 'product'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        product = self.get_object()

        # Get all orders that include this product via OrderDetail
        orders = Order.objects.filter(orderdetails__product=product).distinct()

        # Get customers from these orders
        customers = Customer.objects.filter(orders__in=orders).distinct()

        context['customers'] = customers
        return context

# Create a new customer (class-based view)
class CustomerCreateView(CreateView):
    model = Customer
    template_name = 'DjTraders/CustomerForm.html'
    form_class = CustomerForm
    success_url = reverse_lazy('DjTraders:Customers')  # Redirect to customer list after saving

# Update an existing customer (class-based view)
class CustomerEditView(UpdateView):
    model = Customer
    template_name = 'DjTraders/CustomerForm.html'
    form_class = CustomerForm
    success_url = reverse_lazy('DjTraders:Customers')  # Redirect to customer list after saving
