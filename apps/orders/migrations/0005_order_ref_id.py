# Generated by Django 4.2.7 on 2024-03-07 22:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0004_order_descrition'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='ref_id',
            field=models.CharField(blank=True, max_length=50, null=True, verbose_name='کد پیگیری سفارش'),
        ),
    ]
