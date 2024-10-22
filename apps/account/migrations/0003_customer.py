# Generated by Django 4.2.7 on 2024-02-15 04:38

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import utils


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0002_alter_customuser_options'),
    ]

    operations = [
        migrations.CreateModel(
            name='Customer',
            fields=[
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to=settings.AUTH_USER_MODEL, verbose_name='کاربر')),
                ('phone_number', models.CharField(blank=True, max_length=11, null=True, verbose_name='شماره تلفن')),
                ('address', models.TextField(blank=True, null=True, verbose_name='ادرس')),
                ('image_name', models.ImageField(upload_to=utils.FileUpload.upload_to, verbose_name='تصویر پروفایل')),
            ],
        ),
    ]
