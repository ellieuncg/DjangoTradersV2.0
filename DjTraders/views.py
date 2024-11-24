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
    # First, check if user is already authenticated
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
    template_name = "DjTraders/products.html"
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

    return render(request, "DjTraders/SalesDashboard.html", context)


@login_required
def CustomerDashboard(request, pk):
    customer = get_object_or_404(Customer, pk=pk)

    # Define loyalty tiers
    loyalty_tiers = [
        {"name": "Bronze", "threshold": 5000, "discount": 5, "position": 20},
        {"name": "Silver", "threshold": 25000, "discount": 10, "position": 40},
        {"name": "Gold", "threshold": 50000, "discount": 15, "position": 60},
        {"name": "Platinum", "threshold": 100000, "discount": 20, "position": 80},
    ]

    # Calculate time remaining
    today = timezone.now().date()
    year_end = timezone.datetime(today.year, 12, 31).date()
    days_remaining = (year_end - today).days

    # Previous year's spend
    last_year_start = today - timezone.timedelta(days=730)
    last_year_end = today - timezone.timedelta(days=365)
    previous_year_spend = (
        OrderDetail.objects.filter(
            order__customer=customer,
            order__order_date__gte=last_year_start,
            order__order_date__lte=last_year_end,
        ).aggregate(total=Sum(F("quantity") * F("product__price")))["total"]
        or 0
    )

    # Monthly Sales Analysis
    monthly_sales = (
        Order.objects.filter(customer=customer)
        .annotate(month=ExtractMonth("order_date"), year=ExtractYear("order_date"))
        .values("year", "month")
        .annotate(
            total_revenue=Sum(
                F("orderdetails__quantity") * F("orderdetails__product__price")
            )
        )
        .order_by("-year", "-month")
    )

    monthly_sales_table_data = [
    (f"{sale['year']}-{sale['month']}", float(sale["total_revenue"]))
    for sale in monthly_sales
]


    # Annual Sales Analysis
    base_query = OrderDetail.objects.filter(order__customer=customer)

    annual_sales = (
        base_query.values("order__order_date__month")
        .annotate(
            revenue=Sum(F("quantity") * F("product__price")), 
            units=Sum("quantity")
        )
        .order_by("order__order_date__month")
    )

    annual_sales_labels = [
        "January", "February", "March", "April", "May", "June",
        "July", "August", "September", "October", "November", "December"
    ]
    annual_sales_data = [0] * 12

    for sale in annual_sales:
        month_index = sale["order__order_date__month"] - 1
        annual_sales_data[month_index] = float(sale["revenue"])

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

    # Top Products by Year
    top_products = (
        OrderDetail.objects.filter(order__customer=customer)
        .values("product__product_name")
        .annotate(
            total_quantity=Sum("quantity"),
            revenue=Sum(F("quantity") * F("product__price"))
        )
        .order_by("-revenue")[:10]
    )

    top_products_labels = [product["product__product_name"] for product in top_products]
    top_products_data = [float(product["revenue"]) for product in top_products]

    total_revenue = (
        OrderDetail.objects.filter(order__customer=customer)
        .aggregate(total=Sum(F("quantity") * F("product__price")))["total"]
        or 0
    )

    top_products_table_data = [
        {
            "name": product["product__product_name"],
            "revenue": product["revenue"],
            "units": product["total_quantity"],
            "percentage": (product["revenue"] / total_revenue * 100) if total_revenue else 0,
        }
        for product in top_products
    ]

    # Category Analysis
    category_sales = (
        OrderDetail.objects.filter(order__customer=customer)
        .values("product__category__category_name")
        .annotate(
            revenue=Sum(F("quantity") * F("product__price")),
            units=Sum("quantity")
        )
        .order_by("-revenue")
    )

    category_sales_table_data = [
    {
        "name": category["product__category__category_name"],
        "revenue": category["revenue"],
        "units": category["units"],
        "percentage": (category["revenue"] / total_revenue * 100) if total_revenue else 0,
    }
    for category in category_sales
]



    # Calculate loyalty program progress
    one_year_ago = timezone.now().date() - timezone.timedelta(days=365)
    annual_spend = (
        OrderDetail.objects.filter(
            order__customer=customer,
            order__order_date__gte=one_year_ago
        ).aggregate(total=Sum(F("quantity") * F("product__price")))["total"]
        or 0
    )

    loyalty_info = {
        "current_level": customer.loyalty_level or "Not Qualified",
        "annual_spend": float(annual_spend),
        "discount_percentage": customer.get_discount_percentage(),
        "spend_to_next": float(customer.get_spend_to_next_level() or 0),
    }

    next_level_spend = customer.get_spend_to_next_level()
    if next_level_spend and next_level_spend > 0:
        progress_percentage = min(
            (float(annual_spend) / (float(annual_spend) + float(next_level_spend))) * 100,
            100,
        )
    else:
        progress_percentage = 100

    # Context for rendering
    context = {
        # Basic Info
        "customer": customer,
        "company_name": customer.customer_name,
        "contact_name": customer.contact_name,
        
        # Loyalty Program Info
        "loyalty_info": loyalty_info,
        "loyalty_tiers": loyalty_tiers,
        "progress_percentage": round(progress_percentage, 1),
        "days_remaining": days_remaining,
        "previous_year_spend": float(previous_year_spend),
        
        # Monthly Sales Data
        "monthly_sales_labels": json.dumps([f"{sale['year']}-{sale['month']}" for sale in monthly_sales]),
        "monthly_sales_data": json.dumps([float(sale["total_revenue"]) for sale in monthly_sales]),
        "monthly_sales_table_data": monthly_sales_table_data,
        
        # Annual Sales Data
        "annual_sales_labels": json.dumps(annual_sales_labels),
        "annual_sales_data": json.dumps([float(value) for value in annual_sales_data]),
        "annual_sales_table_data": annual_sales_table_data,
        
        # Top Products Data
        "top_products_labels": json.dumps(top_products_labels),
        "top_products_data": json.dumps(top_products_data),
        "top_products_table_data": top_products_table_data,
        
        # Category Sales Data
        "category_sales_table_data": category_sales_table_data,
        "top_categories_labels": json.dumps([category["name"] for category in category_sales_table_data]),
        "top_categories_data": json.dumps([float(category["revenue"]) for category in category_sales_table_data]),
        
        # Chart Data
        "yearly_orders": json.dumps(annual_sales_labels),
        "yearly_revenue": json.dumps([float(value) for value in annual_sales_data])
    }

    return render(request, "DjTraders/CustomerDashboard.html", context)


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