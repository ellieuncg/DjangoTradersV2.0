# Generated by Django 5.1.2 on 2024-10-31 23:38

import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('DjTraders', '0003_customer_archived_date_customer_last_activity_date_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='archived_date',
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='product',
            name='last_activity_date',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
        migrations.AlterField(
            model_name='product',
            name='status',
            field=models.CharField(choices=[('active', 'Active'), ('inactive', 'Inactive'), ('archived', 'Archived')], default='active', max_length=15),
        ),
    ]
