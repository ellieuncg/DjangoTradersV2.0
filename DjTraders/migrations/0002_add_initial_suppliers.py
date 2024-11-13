from django.db import migrations

def add_suppliers(apps, schema_editor):
    Supplier = apps.get_model('DjTraders', 'Supplier')
    suppliers = [
        {"name": "QuickSource Inc.", "contact_name": "Jane Smith", "phone": "+1 555-2345678", "email": "janesmith@quicksource.com", "address": "45 Quick Ave.", "city": "San Francisco", "country": "USA"},
        {"name": "FreshFields Corp.", "contact_name": "Alice Johnson", "phone": "+1 555-3456789", "email": "ajohnson@freshfields.com", "address": "89 Green Blvd.", "city": "Seattle", "country": "USA"},
        {"name": "Prime Wholesale", "contact_name": "Bob Brown", "phone": "+1 555-4567890", "email": "bbrown@primewholesale.com", "address": "250 Market Lane", "city": "Austin", "country": "USA"},
        {"name": "BrightMart Co.", "contact_name": "Susan Taylor", "phone": "+1 555-5678901", "email": "staylor@brightmart.com", "address": "102 Retail Rd.", "city": "Chicago", "country": "USA"},
        {"name": "NextGen Supplies", "contact_name": "Tom White", "phone": "+1 555-6789012", "email": "twhite@nextgen.com", "address": "58 Future St.", "city": "Miami", "country": "USA"},
        {"name": "ValueChain Partners", "contact_name": "Lisa Green", "phone": "+1 555-7890123", "email": "lgreen@valuechain.com", "address": "77 Chain Drive", "city": "Boston", "country": "USA"},
        {"name": "UltraSource Ltd.", "contact_name": "Paul Black", "phone": "+1 555-8901234", "email": "pblack@ultrasource.com", "address": "39 Ultra Plaza", "city": "Los Angeles", "country": "USA"},
        {"name": "Efficient Exports", "contact_name": "Karen Hill", "phone": "+1 555-9012345", "email": "khill@efficientexports.com", "address": "143 Export Blvd.", "city": "Portland", "country": "USA"},
        {"name": "MegaMart Wholesale", "contact_name": "Frank King", "phone": "+1 555-0123456", "email": "fking@megamart.com", "address": "85 Mega Ave.", "city": "Houston", "country": "USA"},
        {"name": "OmniTrade Inc.", "contact_name": "Diane White", "phone": "+1 555-1234567", "email": "dwhite@omnitrade.com", "address": "101 Trade Plaza", "city": "New York", "country": "USA"},
    ]
    Supplier.objects.bulk_create([Supplier(**supplier) for supplier in suppliers])

class Migration(migrations.Migration):

    dependencies = [
        ('DjTraders', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(add_suppliers),
    ]
