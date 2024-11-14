from django.db import models
from django.utils import timezone
from django.core.validators import RegexValidator, MinLengthValidator
from django.db.models import Sum, F, ExpressionWrapper, DecimalField

# Custom validators
no_numbers_validator = RegexValidator(
    regex=r'^[^\d]+$',
    message="This field should not contain numbers."
)

class Category(models.Model):
    category_id = models.AutoField(primary_key=True)
    category_name = models.CharField(max_length=255)

    class Meta:
        db_table = 'categories'

    def __str__(self):
        return self.category_name

class Customer(models.Model):
    STATUS_CHOICES = [
        ('active', 'Active'),
        ('inactive', 'Inactive'),
        ('archived', 'Archived')
    ]

    GOLD = 'GOLD'
    DIAMOND = 'DIAMOND'
    PLATINUM = 'PLATINUM'
    
    LOYALTY_LEVELS = [
        (GOLD, 'Gold'),
        (DIAMOND, 'Diamond'),
        (PLATINUM, 'Platinum'),
    ]

    customer_id = models.AutoField(primary_key=True)
    customer_name = models.CharField(max_length=255, validators=[no_numbers_validator])
    contact_name = models.CharField(max_length=255, validators=[no_numbers_validator])
    address = models.CharField(
        max_length=255, 
        default='',
        validators=[MinLengthValidator(3, "Address must be at least 3 characters long.")]
    )
    city = models.CharField(max_length=100, validators=[no_numbers_validator], blank=True, null=True)
    postal_code = models.CharField(max_length=20)
    country = models.CharField(max_length=100, validators=[no_numbers_validator])
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='active')
    last_activity_date = models.DateTimeField(default=timezone.now)
    archived_date = models.DateTimeField(null=True, blank=True)
    
    # Loyalty fields
    loyalty_level = models.CharField(max_length=10, choices=LOYALTY_LEVELS, null=True, blank=True)
    annual_spend = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    last_spend_update = models.DateField(null=True, blank=True)

    class Meta:
        db_table = 'customers'

    def __str__(self):
        return self.customer_name

    @property
    def NumberOfOrders(self):
        return self.orders.count()

    def should_be_archived(self):
        if self.status != 'archived':
            days_inactive = (timezone.now() - self.last_activity_date).days
            return days_inactive > 365
        return False

    def archive(self):
        self.status = 'archived'
        self.archived_date = timezone.now()
        self.save()

    def unarchive(self):
        self.status = 'active'
        self.archived_date = None
        self.last_activity_date = timezone.now()
        self.save()

    @property
    def days_inactive(self):
        return (timezone.now() - self.last_activity_date).days

    def calculate_loyalty_level(self):
        if self.annual_spend >= 10000:
            return self.PLATINUM
        elif self.annual_spend >= 7500:
            return self.DIAMOND
        elif self.annual_spend >= 5000:
            return self.GOLD
        return None

    def get_discount_percentage(self):
        discounts = {
            self.PLATINUM: 7.5,
            self.DIAMOND: 5.0,
            self.GOLD: 2.5
        }
        return discounts.get(self.loyalty_level, 0)

    def update_annual_spend(self):
        one_year_ago = timezone.now().date() - timezone.timedelta(days=365)
        
        annual_total = OrderDetail.objects.filter(
            order__customer=self,
            order__order_date__gte=one_year_ago
        ).annotate(
            total=ExpressionWrapper(
                F('quantity') * F('product__price'),
                output_field=DecimalField()
            )
        ).aggregate(Sum('total'))['total__sum'] or 0

        self.annual_spend = annual_total
        self.loyalty_level = self.calculate_loyalty_level()
        self.last_spend_update = timezone.now().date()
        self.save()

    def get_spend_to_next_level(self):
        thresholds = {
            None: 5000,
            self.GOLD: 7500,
            self.DIAMOND: 10000,
            self.PLATINUM: None
        }
        
        next_threshold = thresholds.get(self.loyalty_level)
        if next_threshold:
            return max(0, next_threshold - self.annual_spend)
        return None
    
class Supplier(models.Model):
    supplier_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)
    contact_name = models.CharField(max_length=255, blank=True, null=True)
    phone = models.CharField(max_length=20, blank=True, null=True)
    email = models.EmailField(blank=True, null=True)
    address = models.CharField(max_length=255, blank=True, null=True)
    city = models.CharField(max_length=100, blank=True, null=True)
    country = models.CharField(max_length=100, blank=True, null=True)

    class Meta:
        db_table = 'suppliers'

    def __str__(self):
        return self.name

class Product(models.Model):
    STATUS_CHOICES = [
        ('active', 'Active'),
        ('inactive', 'Inactive')
    ]

    product_id = models.AutoField(primary_key=True)
    product_name = models.CharField(max_length=255)
    category = models.ForeignKey(
        Category, 
        on_delete=models.CASCADE, 
        related_name='products'
    )
    supplier = models.ForeignKey(
        Supplier,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='products'
    )
    unit = models.CharField(max_length=50)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=15, choices=STATUS_CHOICES, default='active')

    class Meta:
        db_table = 'products'

    def __str__(self):
        return self.product_name

class Order(models.Model):
    order_id = models.AutoField(primary_key=True)
    customer = models.ForeignKey(
        Customer, 
        on_delete=models.CASCADE, 
        related_name='orders'
    )
    order_date = models.DateField()

    class Meta:
        db_table = 'orders'

    def __str__(self):
        return f"Order {self.order_id} by {self.customer.customer_name}"

class OrderDetail(models.Model):
    order_detail_id = models.AutoField(primary_key=True)
    order = models.ForeignKey(
        Order, 
        on_delete=models.CASCADE, 
        related_name='orderdetails'
    )
    product = models.ForeignKey(
        Product, 
        on_delete=models.CASCADE, 
        related_name='orderdetails'
    )
    quantity = models.PositiveIntegerField()

    class Meta:
        db_table = 'order_details'

    def __str__(self):
        return f"{self.quantity} x {self.product.product_name} in Order {self.order.order_id}"
