import logging
from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import DetailView, ListView, UpdateView
from django.contrib import messages
from django.utils import timezone
from django.db.models.functions import ExtractYear, ExtractMonth
from django.db.models import (
    Count, Sum, F, Avg, Q, ExpressionWrapper, FloatField, DecimalField, Case, When, Value
)
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth import login
from django.contrib.auth.forms import AuthenticationForm
from django.http import JsonResponse
from .models import Customer, Product, Category, OrderDetail, Order, Supplier
from .forms import CustomerForm, ProductForm
from django.core.serializers.json import DjangoJSONEncoder
import json
from itertools import zip_longest

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
    # Get available years and selected year
    years_query = Order.objects.annotate(
        year=ExtractYear('order_date')
    ).values('year').distinct().order_by('-year')
    
    available_years = [entry['year'] for entry in years_query]
    selected_year = int(request.GET.get('year', available_years[0] if available_years else timezone.now().year))

    # Base query for the selected year
    base_query = OrderDetail.objects.filter(
        order__order_date__year=selected_year
    )

    # Calculate annual sales data
    annual_sales = base_query.values(
        'order__order_date__month'
    ).annotate(
        revenue=Sum(F('quantity') * F('product__price')),
        units=Sum('quantity')
    ).order_by('order__order_date__month')

    # Prepare annual sales data for charts and table
    annual_sales_list = list(annual_sales)
    annual_sales_labels = ['January', 'February', 'March', 'April', 'May', 'June', 
                          'July', 'August', 'September', 'October', 'November', 'December']
    annual_sales_data = [0] * 12  # Initialize with zeros
    
    # Fill in the actual data
    for sale in annual_sales_list:
        month_index = sale['order__order_date__month'] - 1  # Convert 1-based to 0-based index
        annual_sales_data[month_index] = float(sale['revenue'])

    # Calculate growth percentages for table
    annual_sales_table_data = []
    previous_revenue = None
    for i, revenue in enumerate(annual_sales_data):
        growth = 0
        if previous_revenue and previous_revenue != 0:
            growth = ((revenue - previous_revenue) / previous_revenue) * 100
        annual_sales_table_data.append({
            'name': annual_sales_labels[i],
            'revenue': revenue,
            'growth': growth
        })
        previous_revenue = revenue

    # Top 10 Products Analysis
    top_products = base_query.values(
        'product__product_name'
    ).annotate(
        revenue=Sum(F('quantity') * F('product__price')),
        units=Sum('quantity')
    ).order_by('-revenue')[:10]

    total_revenue = base_query.aggregate(
        total=Sum(F('quantity') * F('product__price'))
    )['total'] or 0

    # Prepare top products data
    top_products_labels = []
    top_products_data = []
    top_products_table_data = []

    for product in top_products:
        top_products_labels.append(product['product__product_name'])
        top_products_data.append(float(product['revenue']))
        top_products_table_data.append({
            'name': product['product__product_name'],
            'revenue': product['revenue'],
            'units': product['units'],
            'percentage': (product['revenue'] / total_revenue * 100) if total_revenue else 0
        })

    # Bottom 10 Products Analysis
    bottom_products = base_query.values(
        'product__product_name'
    ).annotate(
        revenue=Sum(F('quantity') * F('product__price')),
        units=Sum('quantity')
    ).order_by('revenue')[:10]

    # Prepare bottom products data
    bottom_products_labels = []
    bottom_products_data = []
    bottom_products_table_data = []

    for product in bottom_products:
        bottom_products_labels.append(product['product__product_name'])
        bottom_products_data.append(float(product['revenue']))
        bottom_products_table_data.append({
            'name': product['product__product_name'],
            'revenue': product['revenue'],
            'units': product['units'],
            'percentage': (product['revenue'] / total_revenue * 100) if total_revenue else 0
        })

    # Category Analysis
    category_sales = base_query.values(
        'product__category__category_name'
    ).annotate(
        revenue=Sum(F('quantity') * F('product__price')),
        units=Sum('quantity')
    ).order_by('-revenue')

    # Prepare category data
    category_sales_labels = []
    category_sales_data = []
    category_sales_table_data = []

    for category in category_sales:
        category_sales_labels.append(category['product__category__category_name'])
        category_sales_data.append(float(category['revenue']))
        category_sales_table_data.append({
            'name': category['product__category__category_name'],
            'revenue': category['revenue'],
            'units': category['units'],
            'percentage': (category['revenue'] / total_revenue * 100) if total_revenue else 0
        })

    context = {
        'available_years': available_years,
        'selected_year': selected_year,
        
        # Annual Sales Data
        'annual_sales_labels': json.dumps(annual_sales_labels),
        'annual_sales_data': json.dumps(annual_sales_data),
        'annual_sales_table_data': annual_sales_table_data,
        
        # Top Products Data
        'top_products_labels': json.dumps(top_products_labels),
        'top_products_data': json.dumps(top_products_data),
        'top_products_table_data': top_products_table_data,
        
        # Bottom Products Data
        'bottom_products_labels': json.dumps(bottom_products_labels),
        'bottom_products_data': json.dumps(bottom_products_data),
        'bottom_products_table_data': bottom_products_table_data,
        
        # Category Sales Data
        'category_sales_labels': json.dumps(category_sales_labels),
        'category_sales_data': json.dumps(category_sales_data),
        'category_sales_table_data': category_sales_table_data,
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
        contact_query = self.request.GET.get('contact', '')
        city_query = self.request.GET.get('city', '')
        country_query = self.request.GET.get('country', '')
        letter = self.request.GET.get('letter', '')
        status = self.request.GET.get('status', 'active')

        if customer_query:
            queryset = queryset.filter(customer_name__icontains=customer_query)
        if contact_query:
            queryset = queryset.filter(contact_name__icontains=contact_query)
        if city_query:
            queryset = queryset.filter(city__icontains=city_query)
        if country_query:
            queryset = queryset.filter(country__iexact=country_query)
        if letter:
            queryset = queryset.filter(customer_name__istartswith=letter)
        if status != 'all':
            queryset = queryset.filter(status=status)

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

def update_customer_status(request, pk):
    if request.method == 'POST':
        customer = get_object_or_404(Customer, pk=pk)
        new_status = request.POST.get('status')
        if new_status in ['active', 'inactive', 'archived']:
            customer.status = new_status
            if new_status == 'archived':
                customer.archived_date = timezone.now()
            customer.save()
            messages.success(request, f'Customer status updated to {new_status}.')
    return redirect('DjTraders:Customers')

# Customer Dashboard
def CustomerDashboard(request, pk):
    customer = get_object_or_404(Customer, pk=pk)

    # Yearly Orders and Revenue
    yearly_orders = Order.objects.filter(customer__customer_id=pk)\
        .annotate(year=ExtractYear('order_date'))\
        .values('year')\
        .annotate(
            order_count=Count('order_id'),
            total_revenue=Sum(F('orderdetails__quantity') * F('orderdetails__product__price'))
        ).order_by('-year')

    # Prepare annual data for template
    yearly_orders_list = list(yearly_orders)
    yearly_revenue = [order['total_revenue'] for order in yearly_orders_list]
    yearly_orders_labels = [order['year'] for order in yearly_orders_list]
    annual_data = list(zip(yearly_orders_labels, yearly_revenue))

    # Monthly Sales Analysis
    monthly_sales = Order.objects.filter(customer__customer_id=pk)\
        .annotate(
            month=ExtractMonth('order_date'),
            year=ExtractYear('order_date')
        ).values('year', 'month')\
        .annotate(
            total_revenue=Sum(F('orderdetails__quantity') * F('orderdetails__product__price'))
        ).order_by('-year', '-month')

    # Prepare monthly data
    monthly_sales_list = list(monthly_sales)
    monthly_sales_labels = [f"{sale['year']}-{sale['month']}" for sale in monthly_sales_list]
    monthly_sales_data = [float(sale['total_revenue']) for sale in monthly_sales_list]
    monthly_data = list(zip(monthly_sales_labels, monthly_sales_data))

    # Top Products
    top_products = OrderDetail.objects.filter(order__customer__customer_id=pk)\
        .values('product__product_name')\
        .annotate(total_quantity=Sum('quantity'))\
        .order_by('-total_quantity')[:10]

    top_products_labels = [item['product__product_name'] for item in top_products]
    top_products_data = [item['total_quantity'] for item in top_products]

    # Top Categories
    top_categories = OrderDetail.objects.filter(order__customer__customer_id=pk)\
        .values('product__category__category_name')\
        .annotate(total_quantity=Sum('quantity'))\
        .order_by('-total_quantity')[:10]

    top_categories_labels = [item['product__category__category_name'] for item in top_categories]
    top_categories_data = [item['total_quantity'] for item in top_categories]

    # Example loyalty info (replace with your actual loyalty logic)
    loyalty_info = {
        'current_level': 'Gold',
        'annual_spend': sum(yearly_revenue) if yearly_revenue else 0,
        'discount_percentage': 10,
        'spend_to_next': 300.00
    }

    context = {
        'customer': customer,
        'annual_data': annual_data,
        'monthly_data': monthly_data,
        'loyalty_info': loyalty_info,
        # Chart.js data
        'yearly_orders': json.dumps(yearly_orders_labels, cls=DjangoJSONEncoder),
        'yearly_revenue': json.dumps(yearly_revenue, cls=DjangoJSONEncoder),
        'monthly_sales_labels': json.dumps(monthly_sales_labels, cls=DjangoJSONEncoder),
        'monthly_sales_data': json.dumps(monthly_sales_data, cls=DjangoJSONEncoder),
        'top_products_labels': json.dumps(top_products_labels, cls=DjangoJSONEncoder),
        'top_products_data': json.dumps(top_products_data, cls=DjangoJSONEncoder),
        'top_categories_labels': json.dumps(top_categories_labels, cls=DjangoJSONEncoder),
        'top_categories_data': json.dumps(top_categories_data, cls=DjangoJSONEncoder),
    }

    return render(request, 'DjTraders/CustomerDashboard.html', context)
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

def update_product_status(request, pk):
    if request.method == 'POST':
        product = get_object_or_404(Product, pk=pk)
        new_status = request.POST.get('status')
        if new_status in ['active', 'inactive', 'archived']:
            product.status = new_status
            product.save()
            messages.success(request, f'Product status updated to {new_status}.')
    return redirect('DjTraders:Products')

class DjTradersProductsView(ListView):
    model = Product
    template_name = 'DjTraders/products.html'
    context_object_name = 'products'

    def get_queryset(self):
        queryset = Product.objects.all()
        product_query = self.request.GET.get('product', '')
        category = self.request.GET.get('category', '')
        min_price = self.request.GET.get('min_price', '')
        max_price = self.request.GET.get('max_price', '')
        status = self.request.GET.get('status', 'active')

        if product_query:
            queryset = queryset.filter(product_name__icontains=product_query)
        if category:
            queryset = queryset.filter(category__category_id=category)
        if min_price:
            try:
                min_price = float(min_price)
                queryset = queryset.filter(price__gte=min_price)
            except ValueError:
                pass
        if max_price:
            try:
                max_price = float(max_price)
                queryset = queryset.filter(price__lte=max_price)
            except ValueError:
                pass
        if status != 'all':
            queryset = queryset.filter(status=status)

        return queryset.order_by('product_name')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = Category.objects.all().order_by('category_name')
        context['selected_category'] = self.request.GET.get('category', '')
        context['status_filter'] = self.request.GET.get('status', 'active')
        return context
