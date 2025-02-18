# Generated by Django 4.2.7 on 2024-02-05 00:35

from django.db import migrations, models
import django.db.models.deletion
import utils


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0008_alter_brand_image_name_alter_product_image_name_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='productfeature',
            name='feature_value',
        ),
        migrations.AddField(
            model_name='productfeature',
            name='filter_value',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='filter_values', to='product.featurevalue', verbose_name='مققدار ویژگی برای فیلتر'),
        ),
        migrations.AlterField(
            model_name='brand',
            name='image_name',
            field=models.ImageField(upload_to=utils.FileUpload.upload_to, verbose_name='تصویر کالا'),
        ),
        migrations.AlterField(
            model_name='product',
            name='image_name',
            field=models.ImageField(upload_to=utils.FileUpload.upload_to, verbose_name='نام تصویر'),
        ),
        migrations.AlterField(
            model_name='productgallery',
            name='image_name',
            field=models.ImageField(upload_to=utils.FileUpload.upload_to, verbose_name='تصویر کالا'),
        ),
        migrations.AlterField(
            model_name='productgroup',
            name='image_name',
            field=models.ImageField(upload_to=utils.FileUpload.upload_to, verbose_name='تصویر گروه'),
        ),
    ]
