from django.db import models
from django.utils import timezone
from django.core.validators import RegexValidator, MinLengthValidator

# Custom validators
no_numbers_validator = RegexValidator(
    regex=r'^[^\d]+$',
    message="This field should not contain numbers."
)

class Category(models.Model):
    """
    Represents product categories in the system.
    Used to organize and classify products.
    """
    category_id = models.AutoField(primary_key=True)
    category_name = models.CharField(max_length=255)

    class Meta:
        db_table = 'categories'

    def __str__(self):
        return self.category_name

class Customer(models.Model):
    """
    Represents customer information and status.
    Includes contact details, location information, and activity tracking.
    """
    # Status choices for customer accounts
    STATUS_CHOICES = [
        ('active', 'Active'),
        ('inactive', 'Inactive'),
        ('archived', 'Archived')
    ]

    # Basic Information
    customer_id = models.AutoField(primary_key=True)
    customer_name = models.CharField(
        max_length=255,
        validators=[no_numbers_validator]
    )
    contact_name = models.CharField(
        max_length=255,
        validators=[no_numbers_validator]
    )

    # Address Information
    address = models.CharField(
        max_length=255, 
        default='',
        validators=[
            MinLengthValidator(3, "Address must be at least 3 characters long.")
        ]
    )
    city = models.CharField(
        max_length=100,
        validators=[no_numbers_validator],
        blank=True,
        null=True
    )
    postal_code = models.CharField(max_length=20)
    country = models.CharField(
        max_length=100,
        validators=[no_numbers_validator]
    )

    # Status and Activity Tracking
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='active')
    last_activity_date = models.DateTimeField(default=timezone.now)
    archived_date = models.DateTimeField(null=True, blank=True)

    class Meta:
        db_table = 'customers'

    def __str__(self):
        return self.customer_name

    @property
    def NumberOfOrders(self):
        """Returns the total number of orders placed by the customer."""
        return self.orders.count()

    def should_be_archived(self):
        """
        Determines if customer should be archived based on inactivity.
        Returns True if customer has been inactive for over a year.
        """
        if self.status != 'archived':
            days_inactive = (timezone.now() - self.last_activity_date).days
            return days_inactive > 365
        return False

    def archive(self):
        """
        Archives the customer record and sets archived date.
        """
        self.status = 'archived'
        self.archived_date = timezone.now()
        self.save()

    def unarchive(self):
        """
        Reactivates an archived customer and resets activity dates.
        """
        self.status = 'active'
        self.archived_date = None
        self.last_activity_date = timezone.now()
        self.save()

    @property
    def days_inactive(self):
        """Returns the number of days since last activity."""
        return (timezone.now() - self.last_activity_date).days

class Product(models.Model):
    """
    Represents products available in the system.
    Includes product details, pricing, and availability status.
    """
    # Status choices for product availability
    STATUS_CHOICES = [
        ('active', 'Active'),
        ('inactive', 'Inactive')
    ]

    # Product Information
    product_id = models.AutoField(primary_key=True)
    product_name = models.CharField(max_length=255)
    category = models.ForeignKey(
        Category, 
        on_delete=models.CASCADE, 
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
    """
    Represents customer orders.
    Links customers to their ordered products through OrderDetail.
    """
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
    """
    Represents individual line items in an order.
    Contains quantity and links to specific products in an order.
    """
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