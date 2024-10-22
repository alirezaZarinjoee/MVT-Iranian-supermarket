# Generated by Django 4.2.7 on 2024-03-16 04:44

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0007_alter_order_ref_id'),
    ]

    operations = [
        migrations.CreateModel(
            name='OrderState',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('order_state_title', models.CharField(max_length=50, verbose_name='عنوان وضعیت سفارش')),
            ],
            options={
                'verbose_name': 'وضعیت سفارش',
                'verbose_name_plural': 'انواع وضعیت سفارش',
            },
        ),
        migrations.AddField(
            model_name='order',
            name='order_state',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='orders_states', to='orders.orderstate', verbose_name='وضعیت سفارش'),
        ),
    ]
