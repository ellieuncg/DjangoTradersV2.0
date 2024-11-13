from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import DetailView, ListView, UpdateView
from django.contrib import messages
from django.utils import timezone
from django.db.models.functions import ExtractYear, ExtractMonth, Cast, Coalesce
from django.db.models import Count, Sum, F, Avg, Q, ExpressionWrapper, FloatField, Case, When, Value
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth import login
from django.contrib.auth.forms import AuthenticationForm
from django.http import JsonResponse
from django.utils.decorators import method_decorator
from .models import Customer, Product, Category, OrderDetail, Order, Supplier
from .forms import CustomerForm, ProductForm
import calendar
import logging

logger = logging.getLogger(__name__)

# Home page view
def index(request):
    """Home page view"""
    return render(request, 'DjTraders/index.html')

# Check if the user is part of the "Employees" group
def is_employee(user):
    return user.groups.filter(name='Employees').exists()

# Sales analysis dashboard for annual, monthly, top/bottom, and category sales
@login_required
@user_passes_test(is_employee)
def SalesDashboard(request):
    available_years = Order.objects.dates('order_date', 'year').values_list('order_date__year', flat=True).distinct().order_by('-order_date__year')
    selected_year = int(request.GET.get('year', available_years[0])) if available_years else None
    selected_category = request.GET.get('category')
    selected_supplier = request.GET.get('supplier')
    
    query_filters = {'order__order_date__year': selected_year}
    if selected_category:
        query_filters['product__category_id'] = selected_category
    if selected_supplier:
        query_filters['product__supplier_id'] = selected_supplier

    # Annual Sales Overview
    annual_total = OrderDetail.objects.filter(**query_filters).aggregate(
        orders_count=Count('order', distinct=True),
        products_sold=Sum('quantity'),
        revenue=Sum(F('quantity') * F('product__price'))
    )

    avg_revenue = OrderDetail.objects.filter(**query_filters).aggregate(avg_revenue=Avg(F('quantity') * F('product__price')))['avg_revenue'] or 0
    top_products = OrderDetail.objects.filter(**query_filters).values('product__product_name').annotate(
        orders_count=Count('order', distinct=True),
        revenue=Sum(F('quantity') * F('product__price')),
        vs_average=ExpressionWrapper(
            Case(
                When(revenue__isnull=False, then=((Sum(F('quantity') * F('product__price')) - avg_revenue) / avg_revenue * 100)),
                default=0,
                output_field=FloatField()
            ),
            output_field=FloatField()
        )
    ).order_by('-revenue')[:10]
    
    bottom_products = OrderDetail.objects.filter(**query_filters).values('product__product_name').annotate(
    orders_count=Count('order', distinct=True),
    revenue=Sum(F('quantity') * F('product__price')),
    vs_average=ExpressionWrapper(
        Case(
            When(revenue__isnull=False, then=((Sum(F('quantity') * F('product__price')) - avg_revenue) / avg_revenue * 100)),
            default=0,
            output_field=FloatField()
        ),
        output_field=FloatField()
    )
).order_by('revenue')[:10]

    category_analysis = OrderDetail.objects.filter(**query_filters).values('product__category__category_name').annotate(
        name=F('product__category__category_name'),
        product_count=Count('product', distinct=True),
        orders_count=Count('order', distinct=True),
        revenue=Sum(F('quantity') * F('product__price'))
    ).order_by('-revenue')

    for category in category_analysis:
        category['avg_per_product'] = category['revenue'] / category['product_count'] if category['product_count'] else 0

    categories = Category.objects.all().order_by('category_name')
    suppliers = Supplier.objects.all().order_by('name')

    context = {
        'annual_total': annual_total,
        'top_products': top_products,
        'bottom_products': bottom_products,
        'category_analysis': category_analysis,
        'available_years': available_years,
        'selected_year': selected_year,
        'selected_category': selected_category,
        'selected_supplier': selected_supplier,
        'categories': categories,
        'suppliers': suppliers,
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
        sale['month_name'] = calendar.month_name[sale['month']]

    context = {
        'customer': customer,
        'yearly_orders': yearly_orders,
        'monthly_sales': monthly_sales,
    }
    
    return render(request, 'DjTraders/CustomerDashboard.html', context)

# Custom login view
def custom_login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            if user.groups.filter(name='Employees').exists():
                messages.success(request, 'Successfully logged in as employee.')
                return redirect('DjTraders:SalesDashboard')
            else:
                messages.success(request, 'Successfully logged in.')
                return redirect('DjTraders:Index')
    else:
        form = AuthenticationForm()
    return render(request, 'DjTraders/login.html', {'form': form})

# Customer list view with search and filtering
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
            return redirect('DjTraders:CustomerDetail', pk=customer.pk)
    else:
        form = CustomerForm(instance=customer)
    return render(request, 'DjTraders/CustomerForm.html', {'form': form, 'customer': customer})

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

# Product list view with search and filtering
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
            messages.error(request, 'Please correct the errors below.')
    else:
        form = ProductForm()
    return render(request, 'DjTraders/ProductForm.html', {'form': form})

def update_product(request, pk):
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
