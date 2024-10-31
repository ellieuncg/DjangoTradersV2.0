from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import DetailView, ListView, UpdateView
from django.db.models import Q
from django.contrib import messages
from django.utils import timezone
from .models import Customer, Product, Category, OrderDetail
from .forms import CustomerForm, ProductForm

def index(request):
    return render(request, 'DjTraders/index.html')

class DjTradersCustomersView(ListView):
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

        # Apply search filters
        if customer_query:
            queryset = queryset.filter(customer_name__icontains=customer_query)
        if contact_query:
            queryset = queryset.filter(contact_name__icontains=contact_query)
        if city_query:
            queryset = queryset.filter(city__icontains=city_query)
        if country_query:
            queryset = queryset.filter(country__icontains=country_query)

        # Apply letter filter
        if letter:
            queryset = queryset.filter(customer_name__istartswith=letter)
        
        # Apply status filter
        if status == 'inactive':
            queryset = queryset.filter(status='inactive')
        elif status == 'all':
            pass  # Show all customers
        else:  # Default to showing only active
            queryset = queryset.filter(status='active')
        
        return queryset.order_by('customer_name')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Add search queries to context for form repopulation
        context.update({
            'customer_query': self.request.GET.get('customer', ''),
            'contact_query': self.request.GET.get('contact', ''),
            'city_query': self.request.GET.get('city', ''),
            'country_query': self.request.GET.get('country', ''),
            'status_filter': self.request.GET.get('status', 'active'),  # Pass current status to context
        })
        return context

class DjTradersProductsView(ListView):
    model = Product
    template_name = 'DjTraders/Products.html'
    context_object_name = 'products'

    def get_queryset(self):
        queryset = Product.objects.all()
        query = self.request.GET.get('q', '')
        category = self.request.GET.get('category', '')
        min_price = self.request.GET.get('min_price', '')
        max_price = self.request.GET.get('max_price', '')
        status = self.request.GET.get('status', 'active')  # Default to active

        if query:
            queryset = queryset.filter(
                Q(product_name__icontains=query) |
                Q(category__category_name__icontains=query)
            )
        
        if category:
            queryset = queryset.filter(category_id=category)
            
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
            
        if status == 'inactive':
            queryset = queryset.filter(Q(status='inactive') | Q(status='discontinued'))
        elif status == 'all':
            pass  # Show all products
        else:
            queryset = queryset.filter(status='active')  # Default
        
        return queryset.order_by('product_name')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        categories = Category.objects.all().order_by('category_name')
        context['categories'] = [
            {'category_id': cat.category_id, 'category_name': cat.category_name}
            for cat in categories
        ]
        context['search_query'] = self.request.GET.get('q', '')
        context['selected_category'] = self.request.GET.get('category', '')
        context['min_price'] = self.request.GET.get('min_price', '')
        context['max_price'] = self.request.GET.get('max_price', '')
        context['status_filter'] = self.request.GET.get('status', 'active')  # Pass current status to context
        return context

class DjTradersCustomerDetailView(DetailView):
    model = Customer
    template_name = 'DjTraders/CustomerDetail.html'
    context_object_name = 'customer'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        customer = self.get_object()
        context['customer_orders'] = self.get_customer_orders(customer)
        return context

    def get_customer_orders(self, customer):
        orders = customer.orders.all()
        return [{
            'order_id': order.order_id,
            'order_date': order.order_date,
            'order_details': [{
                'product_name': detail.product.product_name,
                'quantity': detail.quantity,
                'price': detail.product.price,
                'total': detail.quantity * detail.product.price,
            } for detail in order.orderdetails.all()],
            'order_total': sum(
                detail.quantity * detail.product.price 
                for detail in order.orderdetails.all()
            )
        } for order in orders]

class DjTradersProductDetailView(DetailView):
    model = Product
    template_name = 'DjTraders/ProductDetail.html'
    context_object_name = 'product'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        product = self.get_object()
        order_details = OrderDetail.objects.filter(product=product).order_by('-order__order_date')
        
        order_details_with_total = []
        for detail in order_details:
            order_details_with_total.append({
                'order': detail.order,
                'quantity': detail.quantity,
                'total': detail.quantity * product.price
            })
        
        context['order_details'] = order_details_with_total
        context['orders_count'] = len(order_details_with_total)
        return context

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
    if request.method == 'POST':
        customer = get_object_or_404(Customer, pk=pk)
        new_status = request.POST.get('status')
        if new_status in ['active', 'inactive']:
            customer.status = new_status
            customer.save()
            messages.success(request, f'Customer status updated to {new_status}.')
    return redirect('DjTraders:Customers')

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
    if request.method == 'POST':
        product = get_object_or_404(Product, pk=pk)
        new_status = request.POST.get('status')
        if new_status in ['active', 'inactive', 'discontinued']:
            product.status = new_status
            product.save()
            messages.success(request, f'Product status updated to {new_status}.')
    return redirect('DjTraders:Products')

class CustomerArchiveView(UpdateView):
    model = Customer
    fields = []
    template_name = 'DjTraders/customer_detail.html'
    
    def form_valid(self, form):
        customer = self.get_object()
        customer.status = 'archived'
        customer.archived_date = timezone.now()
        customer.save()
        messages.success(self.request, f'Customer {customer.customer_name} has been archived.')
        return redirect('DjTraders:CustomerDetail', pk=customer.pk)