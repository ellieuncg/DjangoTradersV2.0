from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import DetailView, ListView
from django.db.models import Q
from django.http import JsonResponse
from django.contrib import messages
from django.utils import timezone
from .models import Customer, Product, Order, OrderDetail, Category
from .forms import CustomerForm, ProductForm

def index(request):
    return render(request, 'DjTraders/index.html')

class DjTradersCustomersView(ListView):
    model = Customer
    template_name = 'DjTraders/customers.html'
    context_object_name = 'customers'

    def get_queryset(self):
        queryset = Customer.objects.all()
        query = self.request.GET.get('q', '')
        letter = self.request.GET.get('letter', '')
        status = self.request.GET.get('status', '')

        if query:
            queryset = queryset.filter(
                Q(customer_name__icontains=query) |
                Q(contact_name__icontains=query) |
                Q(city__icontains=query) |
                Q(country__icontains=query)
            )
        
        if letter:
            queryset = queryset.filter(customer_name__istartswith=letter)
            
        if status == 'inactive':
            queryset = queryset.filter(status='inactive')
        elif status == 'all':
            pass  # Show all customers
        else:
            queryset = queryset.filter(status='active')  # Default: show only active
        
        return queryset.order_by('customer_name')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['search_query'] = self.request.GET.get('q', '')
        context['active_letter'] = self.request.GET.get('letter', '')
        context['status_filter'] = self.request.GET.get('status', '')
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
        status = self.request.GET.get('status', '')

        if query:
            queryset = queryset.filter(
                Q(product_name__icontains=query) |
                Q(category__category_name__icontains=query)
            )
        
        if category:
            queryset = queryset.filter(category_id=category)
            
        if min_price:
            queryset = queryset.filter(price__gte=min_price)
        
        if max_price:
            queryset = queryset.filter(price__lte=max_price)
            
        if status == 'inactive':
            queryset = queryset.filter(status='discontinued')
        elif status == 'all':
            pass  # Show all products
        else:
            queryset = queryset.filter(status='active')  # Default: show only active
        
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
        context['status_filter'] = self.request.GET.get('status', '')
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

def archive_customer(request, pk):
    customer = get_object_or_404(Customer, pk=pk)
    if customer.should_be_archived():
        customer.archive()
        messages.success(request, f'Customer "{customer.customer_name}" has been archived.')
    else:
        messages.warning(request, 
            f'Customer cannot be archived yet. Only {customer.days_inactive} days inactive out of required 365.')
    return redirect('DjTraders:CustomerDetail', pk=pk)

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
    if request.method == 'POST' or request.method == 'GET':
        product = get_object_or_404(Product, pk=pk)
        if product.status != 'discontinued':
            product.status = 'discontinued'
            product.save()
            messages.success(request, f'Product "{product.product_name}" has been discontinued.')
        else:
            messages.warning(request, f'Product "{product.product_name}" is already discontinued.')
    return redirect('DjTraders:Products')