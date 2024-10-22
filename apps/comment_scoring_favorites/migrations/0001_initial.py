# Generated by Django 4.2.7 on 2024-03-08 07:28

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('product', '0025_alter_brand_image_name_alter_product_image_name_and_more'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('comment_text', models.TextField(verbose_name='متن نظر')),
                ('register_date', models.DateTimeField(auto_now_add=True, verbose_name='تاریخ ثبت نظر')),
                ('is_active', models.BooleanField(default=False, verbose_name='وضعیت فعال/غیرفعال')),
                ('approving_user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='comments_user2', to=settings.AUTH_USER_MODEL, verbose_name='کاربر تایید کننده نظر')),
                ('comment_parent', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='comments_child', to='comment_scoring_favorites.comment', verbose_name='والد نظر')),
                ('commenting_user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='comments_user1', to=settings.AUTH_USER_MODEL, verbose_name='کاربر نظر دهنده')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='comments_product', to='product.product', verbose_name='کالا')),
            ],
            options={
                'verbose_name': 'نظر',
                'verbose_name_plural': 'نظرات',
            },
        ),
    ]
