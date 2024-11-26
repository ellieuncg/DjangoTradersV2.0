
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
from .models import Customer, Product, Category, OrderDetail, Order, Supplier, Company
from .forms import CustomerForm, ProductForm
from django.core.serializers.json import DjangoJSONEncoder
import json
from itertools import zip_longest
from django.db.models import Sum, Count
from django.http import JsonResponse
from django.shortcuts import render
import json
from .models import Order, Product, Category

from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required, user_passes_test
from django.db.models import Sum, F, Count
from django.utils import timezone
from django.db.models.functions import ExtractYear
from .models import Order, Product, OrderDetail, Category
from django.utils.timezone import now
from django.contrib.auth import authenticate

from django.http import JsonResponse
from django.db.models import Sum, F
from .models import OrderDetail, Product, Category

from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.db.models import Sum, F
from django.db.models.functions import ExtractMonth, ExtractYear
from django.utils.timezone import now
import json
from django.core.serializers.json import DjangoJSONEncoder
from DjTraders.models import OrderDetail  

from django.shortcuts import render
from .models import Order, Product
from django.contrib.auth.decorators import login_required

from django.views.generic import ListView
from .models import Customer

from django.views.generic import ListView
from .models import Customer


from django.views.generic import TemplateView

from django.utils.decorators import method_decorator


from django.urls import clear_url_caches
clear_url_caches()

logger = logging.getLogger(__name__)


# Home Page View
def index(request):
    return render(request, "DjTraders/index.html")


# Check if User is Employee
def is_employee(user):
    result = user.groups.filter(name="Employees").exists()
    print(f"\nDEBUG IS_EMPLOYEE CHECK")
    print(f"User: {user.username}")
    print(f"Result: {result}")
    print(f"Groups: {[g.name for g in user.groups.all()]}")
    return result

def custom_login_view(request):
    print("\nDEBUG LOGIN VIEW")
    print(f"User is authenticated: {request.user.is_authenticated}")
    if request.user.is_authenticated:
        print(f"Current user: {request.user.username}")
        print(f"Groups: {[g.name for g in request.user.groups.all()]}")
        print(f"Is superuser: {request.user.is_superuser}")

    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            next_url = request.GET.get('next')
            print(f"Login successful for {username}")
            print(f"Next URL: {next_url}")
            print(f"Groups: {[g.name for g in user.groups.all()]}")
            print(f"Is superuser: {user.is_superuser}")
            
            if next_url and next_url.startswith('/sales/dashboard/'):
                return redirect('DjTraders:SalesDashboard')
            elif user.groups.filter(name='Employees').exists():
                return redirect('DjTraders:SalesDashboard')
            return redirect('DjTraders:Index')
        else:
            messages.error(request, "Invalid username or password.")
    
    return render(request, "DjTraders/login.html")

class DjTradersProductsView(ListView):
    model = Product
    template_name = "DjTraders/Products.html"
    context_object_name = "products"

    def get_queryset(self):
        queryset = Product.objects.all()
        product_query = self.request.GET.get("product", "").strip()
        category = self.request.GET.get("category", "").strip()
        min_price = self.request.GET.get("min_price", "").strip()
        max_price = self.request.GET.get("max_price", "").strip()
        status = self.request.GET.get("status", "active").strip()

        # Debug prints
        print("\nDEBUG INFORMATION:")
        print(f"Category from request: '{category}'")
        print(f"Initial queryset count: {queryset.count()}")

        # Apply filters based on user input
        if product_query:
            queryset = queryset.filter(product_name__icontains=product_query)
        if category:
            print(f"Filtering by category: '{category}'")
            queryset = queryset.filter(category__category_name=category)
            print(f"After category filter count: {queryset.count()}")
            # Print the SQL query
            print(f"SQL Query: {queryset.query}")
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
        if status and status != "all":
            queryset = queryset.filter(status=status)

        return queryset.order_by("product_name")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Get all categories and print them for debugging
        categories = Category.objects.all().order_by("category_name")
        print("\nAvailable Categories:")
        for cat in categories:
            print(f"- {cat.category_name}")

        context["categories"] = categories
        context["selected_category"] = self.request.GET.get("category", "")
        print(f"Selected category in context: '{context['selected_category']}'")
        
        context["status_filter"] = self.request.GET.get("status", "active")
        context["product_query"] = self.request.GET.get("product", "")
        context["min_price"] = self.request.GET.get("min_price", "")
        context["max_price"] = self.request.GET.get("max_price", "")
        return context

class DjTradersProductDetailView(DetailView):
    model = Product
    template_name = "DjTraders/ProductDetail.html"
    context_object_name = "product"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # Get order details for this product and annotate with total
        order_details = (
            OrderDetail.objects.filter(product=self.object)
            .select_related("order", "order__customer")
            .annotate(total=F("quantity") * F("product__price"))
            .order_by("-order__order_date")
        )

        context["order_details"] = order_details
        return context


def create_product(request):
    if request.method == "POST":
        form = ProductForm(request.POST)
        if form.is_valid():
            product = form.save()
            messages.success(request, "Product created successfully.")
            return redirect("DjTraders:ProductDetail", pk=product.pk)
    else:
        form = ProductForm()
    return render(request, "DjTraders/ProductForm.html", {"form": form})


def update_product(request, pk):
    product = get_object_or_404(Product, pk=pk)
    if request.method == "POST":
        form = ProductForm(request.POST, instance=product)
        if form.is_valid():
            form.save()
            messages.success(request, "Product updated successfully.")
            return redirect("DjTraders:Products")
    else:
        form = ProductForm(instance=product)
    return render(request, "DjTraders/ProductForm.html", {"form": form})


@login_required
def archive_product(request, pk):
    product = get_object_or_404(Product, pk=pk)
    product.status = "archived"
    product.save()
    return JsonResponse(
        {
            "status": "archived",
            "message": f"{product.product_name} archived successfully.",
        }
    )


def update_product_status(request, pk):
    if request.method == "POST":
        product = get_object_or_404(Product, pk=pk)
        new_status = request.POST.get("status")
        if new_status in ["active", "inactive", "archived"]:
            product.status = new_status
            product.save()
            messages.success(request, f"Product status updated to {new_status}.")
    return redirect("DjTraders:Products")


# Customer Views
class DjTradersCustomersView(ListView):
    model = Customer
    template_name = "DjTraders/customers.html"
    context_object_name = "customers"

    def get_queryset(self):
        queryset = Customer.objects.all()
        customer_query = self.request.GET.get("customer", "")
        contact_query = self.request.GET.get("contact", "")
        city_query = self.request.GET.get("city", "")
        country_query = self.request.GET.get("country", "")
        letter = self.request.GET.get("letter", "")
        status = self.request.GET.get("status", "active")

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
        if status != "all":
            queryset = queryset.filter(status=status)

        return queryset.order_by("customer_name")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["status_filter"] = self.request.GET.get("status", "active")
        context["countries"] = (
            Customer.objects.values_list("country", flat=True)
            .distinct()
            .exclude(country__isnull=True)
            .exclude(country__exact="")
            .order_by("country")  # Add this line to order countries alphabetically
        )
        return context

class DjTradersCustomerDetailView(DetailView):
    model = Customer 
    template_name = "DjTraders/CustomerDetail.html"
    context_object_name = "customer"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['orders'] = Order.objects.filter(
            customer=self.object
        ).annotate(
            total_amount=Sum(F('orderdetails__quantity') * F('orderdetails__product__price'))
        ).values(
            'order_id',
            'order_date',
            'total_amount'
        ).order_by('-order_date')
        return context

def create_customer(request):
    if request.method == "POST":
        form = CustomerForm(request.POST)
        if form.is_valid():
            customer = form.save()
            messages.success(request, "Customer created successfully.")
            return redirect("DjTraders:CustomerDetail", pk=customer.pk)
    else:
        form = CustomerForm()
    return render(request, "DjTraders/CustomerForm.html", {"form": form})


def update_customer(request, pk):
    customer = get_object_or_404(Customer, pk=pk)
    if request.method == "POST":
        form = CustomerForm(request.POST, instance=customer)
        if form.is_valid():
            form.save()
            messages.success(request, "Customer updated successfully.")
            return redirect("DjTraders:CustomerDetail", pk=customer.pk)
    else:
        form = CustomerForm(instance=customer)
    return render(request, "DjTraders/CustomerForm.html", {"form": form})


@login_required
def archive_customer(request, pk):
    customer = get_object_or_404(Customer, pk=pk)
    customer.status = "archived"
    customer.archived_date = timezone.now()
    customer.save()
    return JsonResponse(
        {
            "status": "archived",
            "message": f"{customer.customer_name} archived successfully.",
        }
    )


def update_customer_status(request, pk):
    if request.method == "POST":
        customer = get_object_or_404(Customer, pk=pk)
        new_status = request.POST.get("status")
        if new_status in ["active", "inactive", "archived"]:
            customer.status = new_status
            if new_status == "archived":
                customer.archived_date = timezone.now()
            customer.save()
            messages.success(request, f"Customer status updated to {new_status}.")
    return redirect("DjTraders:Customers")


# Sales Dashboard View


# Helper functions
def is_employee(user):
    return user.groups.filter(name="Employees").exists()  

# Sales Dashboard View
@login_required(login_url='DjTraders:login')  # Specify the login URL
@user_passes_test(is_employee, login_url='DjTraders:login')
def SalesDashboard(request):
    # Add debug prints
    print("\nDEBUG SALES DASHBOARD ACCESS")
    print(f"User: {request.user.username}")
    print(f"Authenticated: {request.user.is_authenticated}")
    print(f"Groups: {[g.name for g in request.user.groups.all()]}")
    print(f"Is employee check: {is_employee(request.user)}")
    
    # Rest of your code...
    # Get available years and selected year
    years_query = (
        Order.objects.annotate(year=ExtractYear("order_date"))
        .values("year")
        .distinct()
        .order_by("-year")
    )

    available_years = [entry["year"] for entry in years_query]
    selected_year = int(
        request.GET.get(
            "year", available_years[0] if available_years else timezone.now().year
        )
    )

    # Get all products and selected product
    products = Product.objects.all().values("product_id", "product_name")
    selected_product = request.GET.get("product")

    # Base query for the selected year
    base_query = OrderDetail.objects.filter(order__order_date__year=selected_year)

    # Filter by product if one is selected
    if (
        selected_product and selected_product != ""
    ):  # Check if there's a valid selection
        try:
            selected_product_id = int(selected_product)  # Convert string to integer
            base_query = base_query.filter(product__product_id=selected_product_id)
            product_name = Product.objects.get(
                product_id=selected_product_id
            ).product_name
        except (ValueError, Product.DoesNotExist):
            product_name = "All Products"
    else:
        top_product = (
            base_query.values("product__product_name")
            .annotate(total_revenue=Sum(F("quantity") * F("product__price")))
            .order_by("-total_revenue")
            .first()
        )
        product_name = (
            "All Products"
            if not selected_product
            else (
                top_product["product__product_name"]
                if top_product
                else "No Product Data"
            )
        )

    # Calculate annual sales data
    annual_sales = (
        base_query.values("order__order_date__month")
        .annotate(
            revenue=Sum(F("quantity") * F("product__price")), units=Sum("quantity")
        )
        .order_by("order__order_date__month")
    )

    # Prepare annual sales data for charts and table
    annual_sales_list = list(annual_sales)
    annual_sales_labels = [
        "January",
        "February",
        "March",
        "April",
        "May",
        "June",
        "July",
        "August",
        "September",
        "October",
        "November",
        "December",
    ]
    annual_sales_data = [0] * 12  # Initialize with zeros

    # Fill in the actual data
    for sale in annual_sales_list:
        month_index = (
            sale["order__order_date__month"] - 1
        )  # Convert 1-based to 0-based index
        annual_sales_data[month_index] = float(sale["revenue"])

    # Calculate growth percentages for table
    annual_sales_table_data = []
    previous_revenue = None
    for i, revenue in enumerate(annual_sales_data):
        growth = 0
        if previous_revenue and previous_revenue != 0:
            growth = ((revenue - previous_revenue) / previous_revenue) * 100
        annual_sales_table_data.append(
            {"name": annual_sales_labels[i], "revenue": revenue, "growth": growth}
        )
        previous_revenue = revenue

    # Top 10 Products Analysis
    top_products = (
        base_query.values("product__product_name")
        .annotate(
            revenue=Sum(F("quantity") * F("product__price")), units=Sum("quantity")
        )
        .order_by("-revenue")[:10]
    )

    total_revenue = (
        base_query.aggregate(total=Sum(F("quantity") * F("product__price")))["total"]
        or 0
    )

    # Prepare top products data
    top_products_labels = []
    top_products_data = []
    top_products_table_data = []

    for product in top_products:
        top_products_labels.append(product["product__product_name"])
        top_products_data.append(float(product["revenue"]))
        top_products_table_data.append(
            {
                "name": product["product__product_name"],
                "revenue": product["revenue"],
                "units": product["units"],
                "percentage": (
                    (product["revenue"] / total_revenue * 100) if total_revenue else 0
                ),
            }
        )

    # Bottom 10 Products Analysis
    bottom_products = (
        base_query.values("product__product_name")
        .annotate(
            revenue=Sum(F("quantity") * F("product__price")), units=Sum("quantity")
        )
        .order_by("revenue")[:10]
    )

    # Prepare bottom products data
    bottom_products_labels = []
    bottom_products_data = []
    bottom_products_table_data = []

    for product in bottom_products:
        bottom_products_labels.append(product["product__product_name"])
        bottom_products_data.append(float(product["revenue"]))
        bottom_products_table_data.append(
            {
                "name": product["product__product_name"],
                "revenue": product["revenue"],
                "units": product["units"],
                "percentage": (
                    (product["revenue"] / total_revenue * 100) if total_revenue else 0
                ),
            }
        )

    # Category Analysis
    category_sales = (
        base_query.values("product__category__category_name")
        .annotate(
            revenue=Sum(F("quantity") * F("product__price")), units=Sum("quantity")
        )
        .order_by("-revenue")
    )

    # Prepare category data
    category_sales_labels = []
    category_sales_data = []
    category_sales_table_data = []

    for category in category_sales:
        category_sales_labels.append(category["product__category__category_name"])
        category_sales_data.append(float(category["revenue"]))
        category_sales_table_data.append(
            {
                "name": category["product__category__category_name"],
                "revenue": category["revenue"],
                "units": category["units"],
                "percentage": (
                    (category["revenue"] / total_revenue * 100) if total_revenue else 0
                ),
            }
        )

    context = {
        # Basic Info
        "available_years": available_years,
        "selected_year": selected_year,
        "products": products,
        "selected_product": selected_product,
        "product_name": product_name,
        
        # Annual Sales Data
        "annual_sales_labels": json.dumps(annual_sales_labels),
        "annual_sales_data": json.dumps(annual_sales_data),
        "annual_sales_table_data": annual_sales_table_data,
        
        # Top Products Data
        "top_products_labels": json.dumps(top_products_labels),
        "top_products_data": json.dumps(top_products_data),
        "top_products_table_data": top_products_table_data,
        
        # Bottom Products Data
        "bottom_products_labels": json.dumps(bottom_products_labels),
        "bottom_products_data": json.dumps(bottom_products_data),
        "bottom_products_table_data": bottom_products_table_data,
        
        # Category Sales Data
        "category_sales_labels": json.dumps(category_sales_labels),
        "category_sales_data": json.dumps(category_sales_data),
        "category_sales_table_data": category_sales_table_data,
    }

    return render(request, "DjTraders/SalesDash.html", context)



@login_required
def CustomerTransactions(request, pk):
    customer = get_object_or_404(Customer, pk=pk)

    print("\nDEBUG TRANSACTION DATA CHECK:")
    print(f"Customer ID: {customer.customer_id}")
    print(f"Company Name: {customer.customer_name}")
    print(f"Contact Name: {customer.contact_name}")

    # Get all orders with their details
    transactions = (
        Order.objects.filter(customer=customer)
        .prefetch_related("orderdetails", "orderdetails__product")
        .annotate(
            total_amount=Sum(
                F("orderdetails__quantity") * F("orderdetails__product__price")
            )
        )
        .order_by("-order_date")
    )

    for transaction in transactions:
        print(f"\nOrder ID: {transaction.order_id}")
        print(f"Order Date: {transaction.order_date}")
        print("Order Details:")
        for detail in transaction.orderdetails.all():
            print(f"  - Product: {detail.product.product_name}")
            print(f"  - Quantity: {detail.quantity}")            
            print(f"  - Price: {detail.product.price}")
            print(f"  - Total: {detail.quantity * detail.product.price}")
        print("---")

    context = {
        "customer": customer,
        "transactions": transactions,
        "company_name": customer.customer_name,
        "contact_name": customer.contact_name,
    }

    return render(request, "DjTraders/CustomerTransactions.html", context)



def get_customer_dashboard_data(request):
    # Check if a customer ID is provided
    customer_id = request.GET.get("customer_id")
    if not customer_id:
        return JsonResponse({"error": "Missing 'customer_id' parameter."}, status=400)
    
    try:
        customer = Customer.objects.get(pk=customer_id)
    except Customer.DoesNotExist:
        return JsonResponse({"error": "Customer not found."}, status=404)

    # Annual Sales Revenue
    annual_sales = (
        OrderDetail.objects.filter(order__customer=customer)
        .annotate(year=F("order__order_date__year"))
        .values("year")
        .annotate(revenue=Sum(F("quantity") * F("product__price")))
        .order_by("-year")
    )
    annual_sales_data = list(annual_sales)

    # Top Products Purchased
    top_products = (
        OrderDetail.objects.filter(order__customer=customer)
        .values("product__product_name")
        .annotate(
            revenue=Sum(F("quantity") * F("product__price")),
            units=Sum("quantity")
        )
        .order_by("-revenue")[:5]
    )
    top_products_data = list(top_products)

    # Category Revenue Breakdown
    category_sales = (
        OrderDetail.objects.filter(order__customer=customer)
        .values("product__category__category_name")
        .annotate(
            revenue=Sum(F("quantity") * F("product__price")),
            units=Sum("quantity")
        )
        .order_by("-revenue")
    )
    category_sales_data = list(category_sales)

    # Prepare the response data
    data = {
        "customer_name": customer.customer_name,
        "annual_sales": annual_sales_data,
        "top_products": top_products_data,
        "category_sales": category_sales_data,
    }

    return JsonResponse(data)



@login_required
def CustomerDash(request, pk):
    """
    Customer Dashboard view showing sales analysis and loyalty program status.
    Provides detailed analytics for customer's purchase history and trends.
    """
    customer = get_object_or_404(Customer, pk=pk)

    # Ensure user has access to this customer dashboard
    if not request.user.is_staff and request.user != customer.user:
        return redirect('DjTraders:login')

    # Define loyalty tiers with visualization positions
    loyalty_tiers = [
        {"name": "Bronze", "threshold": 5000, "discount": 2.5, "position": 20},
        {"name": "Silver", "threshold": 7500, "discount": 5.0, "position": 40},
        {"name": "Gold", "threshold": 10000, "discount": 7.5, "position": 60},
        {"name": "Platinum", "threshold": 15000, "discount": 10.0, "position": 80}
    ]

    # Calculate time remaining in current period
    today = timezone.now().date()
    year_end = timezone.datetime(today.year, 12, 31).date()
    days_remaining = (year_end - today).days

    # Get available years for filtering
    available_years = (
        Order.objects.filter(customer=customer)
        .dates('order_date', 'year')
        .values_list('order_date__year', flat=True)
        .distinct()
        .order_by('-order_date__year')
    )

    # Get selected year from query params or use current year
    selected_year = request.GET.get('year', today.year)

    # Calculate previous year's spend
    previous_year_start = today.replace(year=today.year - 1, month=1, day=1)
    previous_year_end = today.replace(year=today.year - 1, month=12, day=31)
    previous_year_spend = (
        OrderDetail.objects.filter(
            order__customer=customer,
            order__order_date__gte=previous_year_start,
            order__order_date__lte=previous_year_end
        ).aggregate(
            total=Sum(F('quantity') * F('product__price'))
        )['total'] or 0
    )

    # Calculate annual sales analysis
    annual_sales = (
        OrderDetail.objects.filter(
            order__customer=customer,
            order__order_date__year=selected_year
        ).values(
            'order__order_date__month'
        ).annotate(
            revenue=Sum(F('quantity') * F('product__price')),
            units=Sum('quantity')
        ).order_by('order__order_date__month')
    )

    # Prepare annual sales data
    months = ['January', 'February', 'March', 'April', 'May', 'June',
             'July', 'August', 'September', 'October', 'November', 'December']
    annual_data = [0] * 12
    for sale in annual_sales:
        month_index = sale['order__order_date__month'] - 1
        annual_data[month_index] = float(sale['revenue'])

    # Calculate growth rates for annual data
    annual_sales_table_data = []
    previous_revenue = None
    for i, revenue in enumerate(annual_data):
        growth = 0
        if previous_revenue and previous_revenue != 0:
            growth = ((revenue - previous_revenue) / previous_revenue) * 100
        annual_sales_table_data.append({
            'name': months[i],
            'revenue': revenue,
            'growth': growth
        })
        previous_revenue = revenue

    # Calculate monthly sales analysis
    monthly_sales = (
        OrderDetail.objects.filter(
            order__customer=customer
        ).annotate(
            month=ExtractMonth('order__order_date'),
            year=ExtractYear('order__order_date')
        ).values(
            'year', 'month'
        ).annotate(
            revenue=Sum(F('quantity') * F('product__price'))
        ).order_by('-year', '-month')
    )

    monthly_sales_table_data = [
        (f"{sale['year']}-{sale['month']}", float(sale['revenue']))
        for sale in monthly_sales
    ]

    # Calculate top products
    top_products = (
        OrderDetail.objects.filter(
            order__customer=customer
        ).values(
            'product__product_name'
        ).annotate(
            revenue=Sum(F('quantity') * F('product__price')),
            units=Sum('quantity')
        ).order_by('-revenue')[:10]
    )

    # Calculate total revenue for percentages
    total_revenue = sum(float(product['revenue']) for product in top_products)

    top_products_table_data = [
        {
            'name': product['product__product_name'],
            'revenue': float(product['revenue']),
            'units': product['units'],
            'percentage': (float(product['revenue']) / total_revenue * 100) if total_revenue else 0
        }
        for product in top_products
    ]

    # Calculate category analysis
    category_sales = (
        OrderDetail.objects.filter(
            order__customer=customer
        ).values(
            'product__category__category_name'
        ).annotate(
            revenue=Sum(F('quantity') * F('product__price')),
            units=Sum('quantity')
        ).order_by('-revenue')
    )

    category_sales_table_data = [
        {
            'name': category['product__category__category_name'],
            'revenue': float(category['revenue']),
            'units': category['units'],
            'percentage': (float(category['revenue']) / total_revenue * 100) if total_revenue else 0
        }
        for category in category_sales
    ]

    # Calculate loyalty program status
    one_year_ago = today - timezone.timedelta(days=365)
    annual_spend = (
        OrderDetail.objects.filter(
            order__customer=customer,
            order__order_date__gte=one_year_ago
        ).aggregate(
            total=Sum(F('quantity') * F('product__price'))
        )['total'] or 0
    )

    loyalty_info = {
        'current_level': customer.loyalty_level or "Not Qualified",
        'annual_spend': float(annual_spend),
        'discount_percentage': customer.get_discount_percentage(),
        'spend_to_next': float(customer.get_spend_to_next_level() or 0)
    }

    # Calculate progress percentage for loyalty program
    next_level_spend = customer.get_spend_to_next_level()
    if next_level_spend and next_level_spend > 0:
        progress_percentage = min(
            (float(annual_spend) / (float(annual_spend) + float(next_level_spend))) * 100,
            100
        )
    else:
        progress_percentage = 100

    # Prepare chart data for JavaScript
    chart_data = {
        'yearly_orders': months,
        'yearly_revenue': [float(value) for value in annual_data],
        'monthly_sales_labels': [f"{sale['year']}-{sale['month']}" for sale in monthly_sales],
        'monthly_sales_data': [float(sale['revenue']) for sale in monthly_sales],
        'top_products_labels': [product['name'] for product in top_products_table_data],
        'top_products_data': [product['revenue'] for product in top_products_table_data],
        'top_categories_labels': [category['name'] for category in category_sales_table_data],
        'top_categories_data': [category['revenue'] for category in category_sales_table_data]
    }

    context = {
        'customer': customer,
        'loyalty_info': loyalty_info,
        'loyalty_tiers': loyalty_tiers,
        'progress_percentage': round(progress_percentage, 1),
        'days_remaining': days_remaining,
        'previous_year_spend': float(previous_year_spend),
        'available_years': available_years,
        'selected_year': selected_year,
        'annual_sales_table_data': annual_sales_table_data,
        'monthly_sales_table_data': monthly_sales_table_data,
        'top_products_table_data': top_products_table_data,
        'category_sales_table_data': category_sales_table_data,
        'dashboard_data': json.dumps(chart_data)
    }

    return render(request, 'DjTraders/CustomerDash.html', context)

from django.http import JsonResponse
from django.db.models import Sum, F
from .models import OrderDetail, Product, Category

def get_sales_dashboard_data(request):
    # Annual Sales Revenue
    annual_sales = (
        OrderDetail.objects.annotate(year=F("order__order_date__year"))
        .values("year")
        .annotate(revenue=Sum(F("quantity") * F("product__price")))
        .order_by("-year")
    )
    annual_sales_data = list(annual_sales)

    # Top 10 Products
    top_products = (
        OrderDetail.objects.values("product__product_name")
        .annotate(
            revenue=Sum(F("quantity") * F("product__price")),
            units=Sum("quantity")
        )
        .order_by("-revenue")[:10]
    )
    top_products_data = list(top_products)

    # Revenue by Category
    category_sales = (
        OrderDetail.objects.values("product__category__category_name")
        .annotate(
            revenue=Sum(F("quantity") * F("product__price")),
            units=Sum("quantity")
        )
        .order_by("-revenue")
    )
    category_sales_data = list(category_sales)

    # Prepare the response data
    data = {
        "annual_sales": annual_sales_data,
        "top_products": top_products_data,
        "category_sales": category_sales_data,
    }

    return JsonResponse(data)



@login_required
@user_passes_test(is_employee)
def SalesDash(request):
    """Independent Sales Dashboard for viewing sales analytics"""
    # Get the current year or the year selected via the filter
    today = now().date()
    selected_year = int(request.GET.get("year", today.year))

    # Query: Annual Sales Data
    annual_sales = (
        OrderDetail.objects.annotate(year=ExtractYear("order__order_date"))
        .values("year")
        .annotate(revenue=Sum(F("quantity") * F("product__price")))
        .order_by("year")
    )
    annual_labels = [str(sale["year"]) for sale in annual_sales]
    annual_data = [sale["revenue"] for sale in annual_sales]

    # Query: Monthly Revenue for Selected Year
    monthly_sales = (
        OrderDetail.objects.filter(order__order_date__year=selected_year)
        .annotate(month=ExtractMonth("order__order_date"))
        .values("month")
        .annotate(revenue=Sum(F("quantity") * F("product__price")))
        .order_by("month")
    )
    months = [
        "January", "February", "March", "April", "May",
        "June", "July", "August", "September", "October", "November", "December"
    ]
    monthly_revenue = [0] * 12
    for sale in monthly_sales:
        monthly_revenue[sale["month"] - 1] = sale["revenue"]

    # Query: Top Products
    top_products = (
        OrderDetail.objects.filter(order__order_date__year=selected_year)
        .values("product__name")
        .annotate(revenue=Sum(F("quantity") * F("product__price")))
        .order_by("-revenue")[:5]
    )
    top_products_labels = [product["product__name"] for product in top_products]
    top_products_data = [product["revenue"] for product in top_products]

    # Query: Bottom Products
    bottom_products = (
        OrderDetail.objects.filter(order__order_date__year=selected_year)
        .values("product__name")
        .annotate(revenue=Sum(F("quantity") * F("product__price")))
        .order_by("revenue")[:5]
    )
    bottom_products_labels = [product["product__name"] for product in bottom_products]
    bottom_products_data = [product["revenue"] for product in bottom_products]

    # Query: Category Sales
    category_sales = (
        OrderDetail.objects.filter(order__order_date__year=selected_year)
        .values("product__category__name")
        .annotate(revenue=Sum(F("quantity") * F("product__price")))
        .order_by("-revenue")
    )
    category_labels = [category["product__category__name"] for category in category_sales]
    category_data = [category["revenue"] for category in category_sales]

    # Prepare chart data
    chart_data = {
        "annual_sales_labels": annual_labels,
        "annual_sales_data": annual_data,
        "monthly_labels": months,
        "monthly_revenue": monthly_revenue,
        "top_products_labels": top_products_labels,
        "top_products_data": top_products_data,
        "bottom_products_labels": bottom_products_labels,
        "bottom_products_data": bottom_products_data,
        "category_labels": category_labels,
        "category_data": category_data,
    }

    # Render context
    context = {
        "available_years": list(range(today.year - 5, today.year + 1)),  # Example: Last 5 years
        "selected_year": selected_year,
        "dashboard_data": json.dumps(chart_data, cls=DjangoJSONEncoder),
    }
    return render(request, "DjTraders/SalesDash.html", context)


@login_required
def client_dashboard(request):
    return render(request, 'DjTraders/client_dashboard.html')
    # Ensure the user is a customer, not an admin or manager
    if not request.user.is_staff:
        # Fetch sales data for the logged-in customer
        customer_orders = Order.objects.filter(customer=request.user)

        # Calculate annual sales, top products, and categories
        annual_sales = customer_orders.values('order_date__year').annotate(
            total_orders=Count('id'),
            total_products=Sum('product__quantity'),
            total_revenue=Sum('total_price')
        )

        top_products = customer_orders.values('product__name').annotate(
            total_quantity=Sum('product__quantity')
        ).order_by('-total_quantity')[:10]

        top_categories = customer_orders.values('product__category__name').annotate(
            total_quantity=Sum('product__quantity')
        ).order_by('-total_quantity')[:10]

        # Prepare data for the template
        context = {
            'annual_sales': annual_sales,
            'top_products': top_products,
            'top_categories': top_categories,
        }
        return render(request, 'DjTraders/client_dashboard.html', context)
    else:
        return redirect('DjTraders:index')




class CustomersListView(ListView):
    model = Customer
    template_name = 'DjTraders/customers.html'  # Points to your uploaded template
    context_object_name = 'customers'

    def get_queryset(self):
        queryset = super().get_queryset()
        status = self.request.GET.get('status')
        letter = self.request.GET.get('letter')

        if status:
            queryset = queryset.filter(status=status)
        if letter:
            queryset = queryset.filter(customer_name__istartswith=letter)

        return queryset

@method_decorator(login_required, name='dispatch')
class TransactionDashboardView(TemplateView):
    template_name = "DjTraders/transaction_dashboard.html"