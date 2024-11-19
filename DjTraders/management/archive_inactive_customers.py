from django.core.management.base import BaseCommand
from django.utils import timezone
from django.db.models import Q
from DjTraders.models import Customer, Order


class Command(BaseCommand):
    help = "Archives customers who have been inactive for more than 365 days"

    def handle(self, *args, **kwargs):
        customers = Customer.objects.filter(
            ~Q(status="archived")  # Exclude already archived customers
        )

        archived_count = 0
        for customer in customers:
            # Get the last order date for this customer
            last_order = (
                Order.objects.filter(customer=customer).order_by("-order_date").first()
            )

            # Update last_activity_date if there's an order
            if last_order:
                customer.last_activity_date = last_order.order_date
                customer.save()

            # Check if customer should be archived
            if customer.should_be_archived():
                customer.archive()
                archived_count += 1
                self.stdout.write(
                    self.style.SUCCESS(
                        f'Archived customer "{customer.customer_name}" - Last activity: {customer.last_activity_date}'
                    )
                )

        self.stdout.write(
            self.style.SUCCESS(f"Successfully archived {archived_count} customers")
        )
