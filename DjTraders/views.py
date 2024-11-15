import logging
from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import DetailView, ListView, UpdateView
from django.contrib import messages
from django.utils import timezone
from django.db.models.functions import ExtractYear
from django.db.models import (
    Count, Sum, F, Avg, ExpressionWrapper, DecimalField, FloatField
)
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth import login
from django.contrib.auth.forms import AuthenticationForm
from django.http import JsonResponse
from .models import Customer, Product, Category, OrderDetail, Order, Supplier
from .forms import CustomerForm, ProductForm
from django.core.serializers.json import DjangoJSONEncoder
import json

logger = logging.getLogger(__name__)

# Home Page View
def index(request):
    return render(request, 'DjTraders/index.html')

# Check if User is Employee
def is_employee(user):
    return user.groups.filter(name='Employees').exists()

# Sales Dashboard View
@login_required
@user_passes_test(is_employee)
def SalesDashboard(request):
    years_query = Order.objects.annotate(
        year=ExtractYear('order_date')
    ).values('year').distinct().order_by('-year')

    available_years = [entry['year'] for entry in years_query]
    selected_year = int(request.GET.get('year', available_years[0] if available_years else timezone.now().year))
    selected_category = request.GET.get('category')
    selected_supplier = request.GET.get('supplier')

    base_query = OrderDetail.objects.filter(order__order_date__year=selected_year)
    if selected_category:
        base_query = base_query.filter(product__category_id=selected_category)
    if selected_supplier:
        base_query = base_query.filter(product__supplier_id=selected_supplier)

    annual_total = base_query.aggregate(
        orders_count=Count('order', distinct=True),
        products_sold=Sum('quantity'),
        revenue=Sum(ExpressionWrapper(F('quantity') * F('product__price'), output_field=DecimalField(max_digits=10, decimal_places=2))),
    )

    top_products = base_query.values('product__product_name').annotate(
        revenue=Sum(F('quantity') * F('product__price'))
    ).order_by('-revenue')[:10]

    bottom_products = base_query.values('product__product_name').annotate(
        revenue=Sum(F('quantity') * F('product__price'))
    ).order_by('revenue')[:10]

    category_analysis = base_query.values('product__category__category_name').annotate(
        name=F('product__category__category_name'),
        product_count=Count('product', distinct=True),
        revenue=Sum(F('quantity') * F('product__price'))
    ).order_by('-revenue')

    context = {
        'annual_total': annual_total,
        'top_products': top_products,
        'bottom_products': bottom_products,
        'category_analysis': category_analysis,
        'available_years': available_years,
        'selected_year': selected_year,
        'selected_category': selected_category,
        'selected_supplier': selected_supplier,
        'categories': Category.objects.all().order_by('category_name'),
        'suppliers': Supplier.objects.all().order_by('name'),
        'annual_sales_labels': json.dumps([entry['name'] for entry in category_analysis], cls=DjangoJSONEncoder),
        'annual_sales_data': json.dumps([entry['revenue'] for entry in category_analysis], cls=DjangoJSONEncoder),
    }

    return render(request, 'DjTraders/SalesDashboard.html', context)

# Custom Login View
def custom_login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            if user.groups.filter(name='Employees').exists():
                return redirect('DjTraders:SalesDashboard')
            return redirect('DjTraders:Index')
    else:
        form = AuthenticationForm()
    return render(request, 'DjTraders/login.html', {'form': form})

# Customer Views
class DjTradersCustomersView(ListView):
    model = Customer
    template_name = 'DjTraders/customers.html'
    context_object_name = 'customers'

    def get_queryset(self):
        queryset = Customer.objects.all()
        customer_query = self.request.GET.get('customer', '')
        if customer_query:
            queryset = queryset.filter(customer_name__icontains=customer_query)
        return queryset.order_by('customer_name')

class DjTradersCustomerDetailView(DetailView):
    model = Customer
    template_name = 'DjTraders/CustomerDetail.html'
    context_object_name = 'customer'

def create_customer(request):
    if request.method == 'POST':
        form = CustomerForm(request.POST)
        if form.is_valid():
            customer = form.save()
            messages.success(request, 'Customer created successfully.')
            return redirect('DjTraders:CustomerDetail', pk=customer.pk)
    else:
        form = CustomerForm()
    return render(request, 'DjTraders/CustomerForm.html', {'form': form})

def update_customer(request, pk):
    customer = get_object_or_404(Customer, pk=pk)
    if request.method == 'POST':
        form = CustomerForm(request.POST, instance=customer)
        if form.is_valid():
            form.save()
            messages.success(request, 'Customer updated successfully.')
            return redirect('DjTraders:CustomerDetail', pk=customer.pk)
    else:
        form = CustomerForm(instance=customer)
    return render(request, 'DjTraders/CustomerForm.html', {'form': form})

@login_required
def archive_customer(request, pk):
    customer = get_object_or_404(Customer, pk=pk)
    customer.status = 'archived'
    customer.archived_date = timezone.now()
    customer.save()
    return JsonResponse({'status': 'archived', 'message': f'{customer.customer_name} archived successfully.'})

# Product Views
class DjTradersProductsView(ListView):
    model = Product
    template_name = 'DjTraders/products.html'
    context_object_name = 'products'

    def get_queryset(self):
        queryset = Product.objects.all()
        product_query = self.request.GET.get('product', '')
        if product_query:
            queryset = queryset.filter(product_name__icontains=product_query)
        return queryset.order_by('product_name')

class DjTradersProductDetailView(DetailView):
    model = Product
    template_name = 'DjTraders/ProductDetail.html'
    context_object_name = 'product'

def create_product(request):
    if request.method == 'POST':
        form = ProductForm(request.POST)
        if form.is_valid():
            product = form.save()
            messages.success(request, 'Product created successfully.')
            return redirect('DjTraders:ProductDetail', pk=product.pk)
    else:
        form = ProductForm()
    return render(request, 'DjTraders/ProductForm.html', {'form': form})

def update_product(request, pk):
    product = get_object_or_404(Product, pk=pk)
    if request.method == 'POST':
        form = ProductForm(request.POST, instance=product)
        if form.is_valid():
            form.save()
            messages.success(request, 'Product updated successfully.')
            return redirect('DjTraders:Products')
    else:
        form = ProductForm(instance=product)
    return render(request, 'DjTraders/ProductForm.html', {'form': form})

@login_required
def archive_product(request, pk):
    product = get_object_or_404(Product, pk=pk)
    product.status = 'archived'
    product.save()
    return JsonResponse({'status': 'archived', 'message': f'{product.product_name} archived successfully.'})



