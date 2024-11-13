from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import DetailView, ListView, UpdateView
from django.contrib import messages
from django.utils import timezone
from django.db.models.functions import ExtractYear, ExtractMonth, Cast, Coalesce
from django.db.models import (
    Count, Sum, F, Avg, Q, ExpressionWrapper, FloatField,
    Case, When, Value
)
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import AuthenticationForm
from .models import Customer, Product, Category, OrderDetail, Order
from .forms import CustomerForm, ProductForm
import calendar
import logging

logger = logging.getLogger(__name__)

def index(request):
    """Home page view"""
    return render(request, 'DjTraders/index.html')

# Check if the user is part of the "Employees" group
def is_employee(user):
    return user.groups.filter(name='Employees').exists()

@login_required
@user_passes_test(is_employee)
def SalesDashboard(request):
    """Sales analysis dashboard for annual, monthly, top/bottom, and category sales."""
    
    # Get years from database, default to latest year
    available_years = list(
        Order.objects
        .dates('order_date', 'year')
        .values_list('order_date__year', flat=True)
        .distinct()
        .order_by('-order_date__year')
    )
    
    # Default to latest year if not specified
    selected_year = int(request.GET.get('year', available_years[0]))
    
    # Annual Sales Overview
    annual_total = (
        OrderDetail.objects
        .filter(order__order_date__year=selected_year)
        .aggregate(
            orders_count=Count('order', distinct=True),
            products_sold=Sum('quantity'),
            revenue=Sum(F('quantity') * F('product__price'))
        )
    )

    # Monthly Sales Data
    monthly_sales = list(OrderDetail.objects
        .filter(order__order_date__year=selected_year)
        .annotate(month=ExtractMonth('order__order_date'))
        .values('month')
        .annotate(
            orders=Count('order', distinct=True),
            products=Sum('quantity'),
            revenue=Sum(F('quantity') * F('product__price'))
        )
        .order_by('month'))

    # Calculate average revenue
    avg_revenue_query = (
        OrderDetail.objects
        .filter(order__order_date__year=selected_year)
        .values('product')
        .annotate(
            total_revenue=Sum(F('quantity') * F('product__price'))
        )
        .aggregate(avg_revenue=Avg('total_revenue'))
    )
    avg_revenue = avg_revenue_query['avg_revenue'] or 0

    # Top 10 Products
    top_products = list(OrderDetail.objects
        .filter(order__order_date__year=selected_year)
        .values('product__product_name')
        .annotate(
            orders_count=Count('order', distinct=True),
            revenue=Sum(F('quantity') * F('product__price'))
        )
        .order_by('-revenue')[:10])

    # Add percentage vs average
    for product in top_products:
        product['vs_average'] = ((product['revenue'] - avg_revenue) / avg_revenue * 100) if avg_revenue else 0

    # Bottom 10 Products
    bottom_products = list(OrderDetail.objects
        .filter(order__order_date__year=selected_year)
        .values('product__product_name')
        .annotate(
            orders_count=Count('order', distinct=True),
            revenue=Sum(F('quantity') * F('product__price'))
        )
        .order_by('revenue')[:10])

    # Add percentage vs average
    for product in bottom_products:
        product['vs_average'] = ((product['revenue'] - avg_revenue) / avg_revenue * 100) if avg_revenue else 0

    # Category Analysis
    category_analysis = list(OrderDetail.objects
        .filter(order__order_date__year=selected_year)
        .values('product__category__category_name')
        .annotate(
            name=F('product__category__category_name'),
            product_count=Count('product', distinct=True),
            orders_count=Count('order', distinct=True),
            revenue=Sum(F('quantity') * F('product__price'))
        )
        .order_by('-revenue'))

    # Calculate average per product for each category
    for category in category_analysis:
        category['avg_per_product'] = category['revenue'] / category['product_count'] if category['product_count'] else 0

    # Get all categories for the filter
    categories = Category.objects.all().order_by('category_name')

    # Format data for charts
    monthly_labels = [calendar.month_name[m['month']] for m in monthly_sales]
    monthly_revenue = [float(m['revenue']) for m in monthly_sales]
    monthly_orders = [m['orders'] for m in monthly_sales]

    monthly_data = {
        'labels': monthly_labels,
        'datasets': [
            {
                'label': 'Revenue',
                'data': monthly_revenue,
                'borderColor': '#456545',
                'fill': False
            },
            {
                'label': 'Orders',
                'data': monthly_orders,
                'borderColor': '#B38F4A',
                'fill': False
            }
        ]
    }

    category_data = {
        'labels': [c['name'] for c in category_analysis],
        'datasets': [{
            'label': 'Revenue by Category',
            'data': [float(c['revenue']) for c in category_analysis],
            'backgroundColor': '#456545'
        }]
    }

    context = {
        'annual_total': annual_total,
        'top_products': top_products,
        'bottom_products': bottom_products,
        'category_analysis': category_analysis,
        'available_years': available_years,
        'selected_year': selected_year,
        'monthly_data': monthly_data,
        'category_data': category_data,
        'categories': categories,
    }

    return render(request, 'DjTraders/SalesDashboard.html', context)

@login_required
def CustomerDashboard(request, pk):
    """Customer dashboard with annual and monthly sales, top products, and top categories."""
    customer = get_object_or_404(Customer, pk=pk)
    
    yearly_orders = Order.objects.filter(customer_id=pk)\
        .annotate(year=ExtractYear('order_date'))\
        .values('year')\
        .annotate(
            order_count=Count('order_id'),
            total_products=Sum('orderdetails__quantity'),
            total_revenue=Sum(F('orderdetails__quantity') * F('orderdetails__product__price'))
        )\
        .order_by('-year')

    monthly_sales = Order.objects.filter(customer_id=pk)\
        .annotate(year=ExtractYear('order_date'), month=ExtractMonth('order_date'))\
        .values('year', 'month')\
        .annotate(
            order_count=Count('order_id'),
            total_products=Sum('orderdetails__quantity'),
            total_revenue=Sum(F('orderdetails__quantity') * F('orderdetails__product__price'))
        )\
        .order_by('-year', '-month')
    for sale in monthly_sales:
        sale['month_name'] = month_name[sale['month']]

    context = {
        'customer': customer,
        'yearly_orders': yearly_orders,
        'monthly_sales': monthly_sales,
    }
    
    return render(request, 'DjTraders/CustomerDashboard.html', context)

def custom_login_view(request):
    print("Login view called")  # Debug print
    if request.method == 'POST':
        print("POST request received")  # Debug print
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            
            print(f"User authenticated: {user.username}")  # Debug print
            print(f"User groups: {[group.name for group in user.groups.all()]}")  # Debug print
            
            if user.groups.filter(name='Employees').exists():
                print(f"Employee group found for {user.username}")  # Debug print
                messages.success(request, 'Successfully logged in as employee.')
                print("About to redirect to SalesDashboard")  # Debug print
                return redirect('DjTraders:SalesDashboard')
            else:
                print(f"No employee group for {user.username}")  # Debug print
                messages.success(request, 'Successfully logged in.')
                return redirect('DjTraders:Index')
        else:
            print(f"Form errors: {form.errors}")  # Debug print
    else:
        form = AuthenticationForm()
        
    return render(request, 'DjTraders/login.html', {'form': form})

# ============================
# Customer Views
# ============================

class DjTradersCustomersView(ListView):
    """Customer list view with search and filtering"""
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
    """Customer detail view"""
    model = Customer
    template_name = 'DjTraders/CustomerDetail.html'
    context_object_name = 'customer'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        customer = self.get_object()
        order_details = []
        for order in customer.orders.all().order_by('-order_date'):
            details = {
                'order_id': order.order_id,
                'order_date': order.order_date,
                'products': [{
                    'product': detail.product,
                    'quantity': detail.quantity,
                } for detail in order.orderdetails.all()]
            }
            order_details.append(details)
        
        sort_field = self.request.GET.get('sort')
        sort_direction = self.request.GET.get('direction', 'desc')
        if sort_field:
            order_details.sort(
                key=lambda x: x['order_id'],
                reverse=(sort_direction == 'desc')
            )
        
        context.update({
            'orders': order_details,
            'sort_field': sort_field,
            'sort_direction': sort_direction
        })
        return context

class CustomerArchiveView(UpdateView):
    """View for archiving customers"""
    model = Customer
    fields = []
    template_name = 'DjTraders/CustomerDetail.html'
    
    def form_valid(self, form):
        customer = self.get_object()
        customer.status = 'archived'
        customer.archived_date = timezone.now()
        customer.save()
        messages.success(self.request, f'Customer {customer.customer_name} has been archived.')
        return redirect('DjTraders:CustomerDetail', pk=customer.pk)

def create_customer(request):
    """Create new customer"""
    if request.method == 'POST':
        form = CustomerForm(request.POST)
        if form.is_valid():
            customer = form.save()
            messages.success(request, 'Customer created successfully.')
            return redirect('DjTraders:CustomerDetail', pk=customer.pk)
        else:
            messages.error(request, 'Please correct the errors below.')
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
            request.session['customer_updated'] = True
            return redirect('DjTraders:CustomerDetail', pk=customer.pk)
    else:
        form = CustomerForm(instance=customer)
    return render(request, 'DjTraders/CustomerForm.html', {'form': form, 'customer': customer})

def update_customer_status(request, pk):
    """Update customer status"""
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

# ============================
# Product Views
# ============================

class DjTradersProductsView(ListView):
    """Product list view with search and filtering"""
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

class DjTradersProductDetailView(DetailView):
    """Product detail view"""
    model = Product
    template_name = 'DjTraders/ProductDetail.html'
    context_object_name = 'product'

def create_product(request):
    """Create new product"""
    if request.method == 'POST':
        form = ProductForm(request.POST)
        if form.is_valid():
            product = form.save()
            messages.success(request, 'Product created successfully.')
            return redirect('DjTraders:ProductDetail', pk=product.pk)
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = ProductForm()
    return render(request, 'DjTraders/ProductForm.html', {'form': form})

def update_product(request, pk):
    """Update existing product"""
    product = get_object_or_404(Product, pk=pk)
    if request.method == 'POST':
        form = ProductForm(request.POST, instance=product)
        if form.is_valid():
            product = form.save()
            messages.success(request, 'Product updated successfully.')
            return redirect('DjTraders:ProductDetail', pk=product.pk)
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = ProductForm(instance=product)
    return render(request, 'DjTraders/ProductForm.html', {'form': form, 'product': product})

def update_product_status(request, pk):
    """Update product status"""
    if request.method == 'POST':
        product = get_object_or_404(Product, pk=pk)
        new_status = request.POST.get('status')
        if new_status in ['active', 'inactive', 'archived']:
            product.status = new_status
            if new_status == 'archived':
                product.archived_date = timezone.now()
            product.save()
            messages.success(request, f'Product status updated to {new_status}.')
    return redirect('DjTraders:Products')
