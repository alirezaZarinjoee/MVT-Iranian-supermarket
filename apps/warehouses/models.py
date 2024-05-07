from django.db import models
from apps.product.models import Product
from apps.account.models import CustomUser

class WarehouseType(models.Model):
    warehouse_type_title=models.CharField(verbose_name='نوع انبار', max_length=50)
    
    def __str__(self):
        return self.warehouse_type_title
    
    class Meta:
        verbose_name='نوع انبار'
        verbose_name_plural='انواع انبار'
        
class Warehouse(models.Model):
    warehouse_type=models.ForeignKey(WarehouseType, verbose_name='نوع انبار', on_delete=models.CASCADE)
    user_register=models.ForeignKey(CustomUser, verbose_name='کاربر انبار دار', on_delete=models.CASCADE,related_name='warehouseuser_registered')
    product=models.ForeignKey(Product, verbose_name='کالا', on_delete=models.CASCADE,related_name='warehouse_products')
    qty=models.IntegerField(verbose_name='تعداد کالا')
    price=models.IntegerField(verbose_name='قیمت',null=True,blank=True)
    register_date=models.DateTimeField(verbose_name='تاریخ ثبت', auto_now_add=True)
    
    def __str__(self):
        return f'{self.warehouse_type} {self.product}'
    
    class Meta:
        verbose_name='انبار'
        verbose_name_plural='انبار ها'
        
