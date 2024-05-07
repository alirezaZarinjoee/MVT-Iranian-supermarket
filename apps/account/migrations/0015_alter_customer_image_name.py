# Generated by Django 4.2.7 on 2024-03-07 22:40

from django.db import migrations, models
import utils


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0014_alter_customer_image_name'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customer',
            name='image_name',
            field=models.ImageField(blank=True, null=True, upload_to=utils.FileUpload.upload_to, verbose_name='تصویر پروفایل'),
        ),
    ]
