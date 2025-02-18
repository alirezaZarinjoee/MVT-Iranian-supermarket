# Generated by Django 4.2.7 on 2024-02-19 05:46

import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('product', '0016_alter_brand_image_name_alter_product_image_name_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='Coupon',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('coupon_code', models.CharField(max_length=10, unique=True, verbose_name='کد کوپن')),
                ('start_date', models.DateTimeField(verbose_name='تاریخ شروع')),
                ('end_date', models.DateTimeField(verbose_name='تاریخ پایان')),
                ('discount', models.IntegerField(validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(100)], verbose_name='درصد تخفیف')),
                ('is_active', models.BooleanField(default=False, verbose_name='فعال/غیرفعال')),
            ],
            options={
                'verbose_name': 'کد تخفیف',
                'verbose_name_plural': 'کد های تخفیف',
            },
        ),
        migrations.CreateModel(
            name='DiscountBasket',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('discount_title', models.CharField(max_length=10, unique=True, verbose_name='عنوان سبد خرید')),
                ('start_date', models.DateTimeField(verbose_name='تاریخ شروع')),
                ('end_date', models.DateTimeField(verbose_name='تاریخ پایان')),
                ('discount', models.IntegerField(validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(100)], verbose_name='درصد تخفیف')),
                ('is_active', models.BooleanField(default=False, verbose_name='فعال/غیرفعال')),
            ],
            options={
                'verbose_name': 'سبد خرید',
                'verbose_name_plural': 'سبد های خرید',
            },
        ),
        migrations.CreateModel(
            name='DiscountBasketDetails',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('discount_basket', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='discount_basket_details2', to='product.product', verbose_name='کالا')),
            ],
        ),
    ]
