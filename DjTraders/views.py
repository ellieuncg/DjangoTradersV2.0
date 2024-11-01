from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import DetailView, ListView, UpdateView
from django.db.models import Q
from django.contrib import messages
from django.utils import timezone
from .models import Customer, Product, Category, OrderDetail
from .forms import CustomerForm, ProductForm

def index(request):
    """Home page view"""
    return render(request, 'DjTraders/index.html')

class DjTradersCustomersView(ListView):
    """Customer list view with search and filtering"""
    model = Customer
    template_name = 'DjTraders/customers.html'
    context_object_name = 'customers'

    def get_queryset(self):
        queryset = Customer.objects.all()
        
        # Get search parameters
        customer_query = self.request.GET.get('customer', '')
        contact_query = self.request.GET.get('contact', '')
        city_query = self.request.GET.get('city', '')
        country_query = self.request.GET.get('country', '')
        letter = self.request.GET.get('letter', '')
        status = self.request.GET.get('status', 'active')  # Default to active

        # Apply filters
        if customer_query:
            queryset = queryset.filter(customer_name__icontains=customer_query)
        if contact_query:
            queryset = queryset.filter(contact_name__icontains=contact_query)
        if city_query:
            queryset = queryset.filter(city__icontains=city_query)
        if country_query:
            queryset = queryset.filter(country__icontains=country_query)
        if letter:
            queryset = queryset.filter(customer_name__istartswith=letter)
        
        # Status filter
        if status == 'active':
            queryset = queryset.filter(status='active')
        elif status == 'inactive':
            queryset = queryset.filter(status='inactive')
        elif status == 'archived':
            queryset = queryset.filter(status='archived')
        # 'all' shows everything, so no filter needed

        return queryset.order_by('customer_name')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Get unique countries from the database
        countries = Customer.objects.values_list('country', flat=True).distinct().order_by('country')
        context.update({
            'customer_query': self.request.GET.get('customer', ''),
            'contact_query': self.request.GET.get('contact', ''),
            'city_query': self.request.GET.get('city', ''),
            'country_query': self.request.GET.get('country', ''),
            'status_filter': self.request.GET.get('status', 'active'),
            'countries': countries  # Add this line to provide countries to template
        })
        return context

class DjTradersProductsView(ListView):
    """Product list view with search and filtering"""
    model = Product
    template_name = 'DjTraders/products.html'
    context_object_name = 'products'

    def get_queryset(self):
        queryset = Product.objects.all()
        
        # Get search parameters
        product_query = self.request.GET.get('product', '')
        supplier_query = self.request.GET.get('supplier', '')
        category = self.request.GET.get('category', '')
        min_price = self.request.GET.get('min_price', '')
        max_price = self.request.GET.get('max_price', '')
        status = self.request.GET.get('status', 'active')

        # Apply filters
        if product_query:
            queryset = queryset.filter(product_name__icontains=product_query)
        if supplier_query:
            queryset = queryset.filter(supplier__company_name__icontains=supplier_query)
        if category:
            queryset = queryset.filter(category__category_id=category)
        if min_price:
            try:
                queryset = queryset.filter(price__gte=float(min_price))
            except ValueError:
                pass
        if max_price:
            try:
                queryset = queryset.filter(price__lte=float(max_price))
            except ValueError:
                pass

        # Status filter
        if status != 'all':
            queryset = queryset.filter(status=status)

        return queryset.order_by('product_name')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Get categories for filter
        categories = Category.objects.all().order_by('category_name')
        context.update({
            'categories': categories,
            'product_query': self.request.GET.get('product', ''),
            'supplier_query': self.request.GET.get('supplier', ''),
            'min_price': self.request.GET.get('min_price', ''),
            'max_price': self.request.GET.get('max_price', ''),
            'selected_category': self.request.GET.get('category', ''),
            'status_filter': self.request.GET.get('status', 'active'),
        })
        return context

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
        context['orders'] = order_details
        return context

class DjTradersProductDetailView(DetailView):
    """Product detail view"""
    model = Product
    template_name = 'DjTraders/ProductDetail.html'
    context_object_name = 'product'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        product = self.get_object()
        order_details = OrderDetail.objects.filter(product=product).order_by('-order__order_date')
        context['order_details'] = [{
            'order': detail.order,
            'quantity': detail.quantity,
            'unit_price': detail.product.price,
            'total': detail.product.price * detail.quantity,
        } for detail in order_details]
        context['total_orders'] = len(order_details)
        context['total_units_sold'] = sum(detail.quantity for detail in order_details)
        context['total_revenue'] = sum(detail.product.price * detail.quantity for detail in order_details)
        return context

class CustomerArchiveView(UpdateView):
    """View for archiving customers"""
    model = Customer
    fields = []
    template_name = 'DjTraders/CustomerDetail.html'
    
    def form_valid(self, form):
        customer = self.get_object()
        customer.status = 'inactive'
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
        form = CustomerForm()
    return render(request, 'DjTraders/CustomerForm.html', {'form': form})

def update_customer(request, pk):
    """Update existing customer"""
    customer = get_object_or_404(Customer, pk=pk)
    if request.method == 'POST':
        form = CustomerForm(request.POST, instance=customer)
        if form.is_valid():
            customer = form.save()
            messages.success(request, 'Customer updated successfully.')
            return redirect('DjTraders:CustomerDetail', pk=customer.pk)
    else:
        form = CustomerForm(instance=customer)
    return render(request, 'DjTraders/CustomerForm.html', {
        'form': form,
        'customer': customer
    })

def update_customer_status(request, pk):
    """Update customer active/inactive status"""
    if request.method == 'POST':
        customer = get_object_or_404(Customer, pk=pk)
        new_status = request.POST.get('status')
        if new_status in ['active', 'inactive']:
            customer.status = new_status
            customer.save()
            messages.success(request, f'Customer status updated to {new_status}.')
    return redirect('DjTraders:Customers')

def create_product(request):
    """Create new product"""
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
    """Update existing product"""
    product = get_object_or_404(Product, pk=pk)
    if request.method == 'POST':
        form = ProductForm(request.POST, instance=product)
        if form.is_valid():
            product = form.save()
            messages.success(request, 'Product updated successfully.')
            return redirect('DjTraders:ProductDetail', pk=product.pk)
    else:
        form = ProductForm(instance=product)
    return render(request, 'DjTraders/ProductForm.html', {
        'form': form,
        'product': product
    })

def update_product_status(request, pk):
    """Update product active/inactive/archived status"""
    if request.method == 'POST':
        product = get_object_or_404(Product, pk=pk)
        new_status = request.POST.get('status')
        if new_status in ['active', 'inactive', 'archived']:
            product.status = new_status
            # Set archived date if status is changing to archived
            if new_status == 'archived':
                product.archived_date = timezone.now()
            product.save()
            messages.success(request, f'Product status updated to {new_status}.')
    return redirect('DjTraders:Products')