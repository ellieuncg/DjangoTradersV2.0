from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import DetailView, ListView, UpdateView
from django.contrib import messages
from django.utils import timezone
from django.db.models import Count, Sum, F, Avg, ExpressionWrapper, FloatField, DecimalField
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth import login
from django.contrib.auth.forms import AuthenticationForm
from django.core.exceptions import PermissionDenied
from django.contrib.auth.decorators import login_required

from .models import Customer, Product, Category, OrderDetail, Order, Supplier
from .forms import CustomerForm, ProductForm
import json
from django.core.serializers.json import DjangoJSONEncoder


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
    # Get available years
    years_query = Order.objects.annotate(
        year=ExtractYear('order_date')
    ).values('year').distinct().order_by('-year')
    
    available_years = [entry['year'] for entry in years_query]
    
    # Get selected filters
    selected_year = int(request.GET.get('year', available_years[0] if available_years else timezone.now().year))
    selected_category = request.GET.get('category')
    selected_supplier = request.GET.get('supplier')
    
    # Base query
    base_query = OrderDetail.objects.filter(
        order__order_date__year=selected_year
    )
    
    # Apply filters
    if selected_category:
        base_query = base_query.filter(product__category_id=selected_category)
    
    if selected_supplier:
        base_query = base_query.filter(product__supplier_id=selected_supplier)
    
    # Calculate annual totals
    annual_total = base_query.aggregate(
        orders_count=Count('order', distinct=True),
        products_sold=Sum('quantity'),
        revenue=Sum(
            ExpressionWrapper(
                F('quantity') * F('product__price'),
                output_field=DecimalField(max_digits=10, decimal_places=2)
            )
        )
    )
    
    # Calculate average revenue per product
    product_revenues = base_query.values('product').annotate(
        revenue=Sum(
            ExpressionWrapper(
                F('quantity') * F('product__price'),
                output_field=DecimalField(max_digits=10, decimal_places=2)
            )
        )
    )
    
    avg_revenue = product_revenues.aggregate(
        avg_revenue=Avg('revenue')
    )['avg_revenue'] or 0
    
    # Top Products
    top_products = base_query.values(
        'product__product_name'
    ).annotate(
        orders_count=Count('order', distinct=True),
        revenue=Sum(
            ExpressionWrapper(
                F('quantity') * F('product__price'),
                output_field=DecimalField(max_digits=10, decimal_places=2)
            )
        ),
        vs_average=ExpressionWrapper(
            (Sum(F('quantity') * F('product__price')) - avg_revenue) / avg_revenue * 100,
            output_field=FloatField()
        )
    ).order_by('-revenue')[:10]
    
    # Bottom Products
    bottom_products = base_query.values(
        'product__product_name'
    ).annotate(
        orders_count=Count('order', distinct=True),
        revenue=Sum(
            ExpressionWrapper(
                F('quantity') * F('product__price'),
                output_field=DecimalField(max_digits=10, decimal_places=2)
            )
        ),
        vs_average=ExpressionWrapper(
            (Sum(F('quantity') * F('product__price')) - avg_revenue) / avg_revenue * 100,
            output_field=FloatField()
        )
    ).order_by('revenue')[:10]
    
    # Category Analysis
    category_analysis = base_query.values(
        'product__category__category_name'
    ).annotate(
        name=F('product__category__category_name'),
        product_count=Count('product', distinct=True),
        orders_count=Count('order', distinct=True),
        revenue=Sum(
            ExpressionWrapper(
                F('quantity') * F('product__price'),
                output_field=DecimalField(max_digits=10, decimal_places=2)
            )
        )
    ).order_by('-revenue')
    
    # Calculate average per product for categories
    for category in category_analysis:
        category['avg_per_product'] = (
            category['revenue'] / category['product_count']
            if category['product_count'] else 0
        )
    
    # Prepare data for charts
    annual_sales_labels = [category['name'] for category in category_analysis]
    annual_sales_data = [category['revenue'] for category in category_analysis]
    top_products_labels = [product['product__product_name'] for product in top_products]
    top_products_data = [product['revenue'] for product in top_products]
    bottom_products_labels = [product['product__product_name'] for product in bottom_products]
    bottom_products_data = [product['revenue'] for product in bottom_products]
    category_sales_labels = [category['name'] for category in category_analysis]
    category_sales_data = [category['product_count'] for category in category_analysis]

    # Context data
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
        
        # Additional data for visualizations
        'annual_sales_labels': json.dumps(annual_sales_labels, cls=DjangoJSONEncoder),
        'annual_sales_data': json.dumps(annual_sales_data, cls=DjangoJSONEncoder),
        'top_products_labels': json.dumps(top_products_labels, cls=DjangoJSONEncoder),
        'top_products_data': json.dumps(top_products_data, cls=DjangoJSONEncoder),
        'bottom_products_labels': json.dumps(bottom_products_labels, cls=DjangoJSONEncoder),
        'bottom_products_data': json.dumps(bottom_products_data, cls=DjangoJSONEncoder),
        'category_sales_labels': json.dumps(category_sales_labels, cls=DjangoJSONEncoder),
        'category_sales_data': json.dumps(category_sales_data, cls=DjangoJSONEncoder),
    }
    
    # Prepare table data for each tab
    annual_sales_table_data = []
    for category in category_analysis:
        annual_sales_table_data.append({
            'name': category['name'],
            'revenue': category['revenue'],
            'growth': ((category['revenue'] - category.get('prev_revenue', 0)) / category.get('prev_revenue', 1) * 100 
                      if category.get('prev_revenue', 0) else 0)
        })

    top_products_table_data = []
    for product in top_products:
        top_products_table_data.append({
            'name': product['product__product_name'],
            'revenue': product['revenue'],
            'units': product['orders_count'],
            'percentage': (product['revenue'] / annual_total['revenue'] * 100 if annual_total['revenue'] else 0)
        })

    bottom_products_table_data = []
    for product in bottom_products:
        bottom_products_table_data.append({
            'name': product['product__product_name'],
            'revenue': product['revenue'],
            'units': product['orders_count'],
            'percentage': (product['revenue'] / annual_total['revenue'] * 100 if annual_total['revenue'] else 0)
        })

    category_sales_table_data = []
    for category in category_analysis:
        category_sales_table_data.append({
            'name': category['name'],
            'revenue': category['revenue'],
            'units': category['orders_count'],
            'percentage': (category['revenue'] / annual_total['revenue'] * 100 if annual_total['revenue'] else 0)
        })

    context.update({
        'annual_sales_table_data': annual_sales_table_data,
        'top_products_table_data': top_products_table_data,
        'bottom_products_table_data': bottom_products_table_data,
        'category_sales_table_data': category_sales_table_data,
    })
    
    return render(request, 'DjTraders/SalesDashboard.html', context)


# Custom Login View with Employee Group Check
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

# Customer List View with Search and Filtering
class DjTradersCustomersView(ListView):
    model = Customer
    template_name = 'DjTraders/customers.html'
    context_object_name = 'customers'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['countries'] = Customer.objects.values_list('country', flat=True).distinct().order_by('country')
        return context

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

# Customer Dashboard View
@login_required
def CustomerDashboard(request, pk):
    customer = get_object_or_404(Customer, pk=pk)
    
    # Check if user is a customer and viewing their own dashboard
    if hasattr(request.user, 'customer'):
        if request.user.customer.pk != pk:
            raise PermissionDenied("You can only view your own dashboard.")
    else:
        raise PermissionDenied("Only customers can access dashboards.")
    
    yearly_orders = list(Order.objects.filter(customer__customer_id=pk)
        .annotate(year=ExtractYear('order_date'))
        .values('year')
        .annotate(
            order_count=Count('order_id'),
            total_products=Sum('orderdetails__quantity'),
            total_revenue=Sum(F('orderdetails__quantity') * F('orderdetails__product__price'))
        ).order_by('-year'))
    yearly_revenue = [item['total_revenue'] for item in yearly_orders]
    yearly_orders_labels = [item['year'] for item in yearly_orders]

    monthly_sales = list(Order.objects.filter(customer__customer_id=pk)
        .annotate(year=ExtractYear('order_date'))
        .values('year')
        .annotate(
            order_count=Count('order_id'),
            total_products=Sum('orderdetails__quantity'),
            total_revenue=Sum(F('orderdetails__quantity') * F('orderdetails__product__price'))
        ).order_by('-year'))
    monthly_sales_labels = [f"{sale['year']}" for sale in monthly_sales]
    monthly_sales_data = [sale['total_revenue'] for sale in monthly_sales]

    top_products_by_year = OrderDetail.objects.filter(order__customer__customer_id=pk)\
        .annotate(year=ExtractYear('order__order_date'))\
        .values('product__product_name')\
        .annotate(total_quantity=Sum('quantity'))\
        .order_by('-total_quantity')[:10]
    top_products_labels = [item['product__product_name'] for item in top_products_by_year]
    top_products_data = [item['total_quantity'] for item in top_products_by_year]

    top_categories_by_year = OrderDetail.objects.filter(order__customer__customer_id=pk)\
        .annotate(year=ExtractYear('order__order_date'))\
        .values('product__category__category_name')\
        .annotate(total_quantity=Sum('quantity'))\
        .order_by('-total_quantity')[:10]
    top_categories_labels = [item['product__category__category_name'] for item in top_categories_by_year]
    top_categories_data = [item['total_quantity'] for item in top_categories_by_year]

    context = {
        'customer': customer,
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


# Customer Detail View
class DjTradersCustomerDetailView(DetailView):
    model = Customer
    template_name = 'DjTraders/CustomerDetail.html'
    context_object_name = 'customer'

# Archive Customer View
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

# Create Customer View
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

# Update Customer View
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

# Update Customer Status View
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

# Product Views
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

# Product Detail View
class DjTradersProductDetailView(DetailView):
    model = Product
    template_name = 'DjTraders/ProductDetail.html'
    context_object_name = 'product'

# Create Product View
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

# Update Product View
def update_product(request, pk):
    product = get_object_or_404(Product, pk=pk)
    if request.method == 'POST':
        form = ProductForm(request.POST, instance=product)
        if form.is_valid():
            form.save()
            messages.success(request, 'Product updated successfully.')
            return redirect('DjTraders:Products')
        else:
            messages.error(request, 'Error saving product.')
    else:
        form = ProductForm(instance=product)
    return render(request, 'DjTraders/ProductForm.html', {'form': form})

# Update Product Status View
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
