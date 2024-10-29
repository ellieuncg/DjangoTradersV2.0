from django.db import models
from django.utils import timezone

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
    
    customer_id = models.AutoField(primary_key=True)
    customer_name = models.CharField(max_length=255)
    contact_name = models.CharField(max_length=255)
    address = models.CharField(max_length=255, default='')
    city = models.CharField(max_length=100)
    postal_code = models.CharField(max_length=20)
    country = models.CharField(max_length=100)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='active')
    last_activity_date = models.DateTimeField(default=timezone.now)
    archived_date = models.DateTimeField(null=True, blank=True)

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
        
    @property
    def days_inactive(self):
        return (timezone.now() - self.last_activity_date).days

class Product(models.Model):
    STATUS_CHOICES = [
        ('active', 'Active'),
        ('discontinued', 'Discontinued')
    ]
    
    product_id = models.AutoField(primary_key=True)
    product_name = models.CharField(max_length=255)
    category = models.ForeignKey(
        Category, on_delete=models.CASCADE, related_name='products'
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
        Customer, on_delete=models.CASCADE, related_name='orders'
    )
    order_date = models.DateField()

    class Meta:
        db_table = 'orders'

    def __str__(self):
        return f"Order {self.order_id} by {self.customer.customer_name}"

class OrderDetail(models.Model):
    order_detail_id = models.AutoField(primary_key=True)
    order = models.ForeignKey(
        Order, on_delete=models.CASCADE, related_name='orderdetails'
    )
    product = models.ForeignKey(
        Product, on_delete=models.CASCADE, related_name='orderdetails'
    )
    quantity = models.PositiveIntegerField()

    class Meta:
        db_table = 'order_details'

    def __str__(self):
        return f"{self.quantity} x {self.product.product_name} in Order {self.order.order_id}"