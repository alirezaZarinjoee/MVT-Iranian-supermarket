from django.db import models
from apps.account.models import Customer
from django.utils import timezone
import uuid
from apps.product.models import Product
import utils



class OrderState(models.Model):
    order_state_title=models.CharField(verbose_name='عنوان وضعیت سفارش', max_length=50)
    
    def __str__(self):
        return self.order_state_title
    
    class Meta:
        verbose_name='وضعیت سفارش'
        verbose_name_plural='انواع وضعیت سفارش'


class PaymentType(models.Model):
    payment_title=models.CharField(verbose_name='نوع پرداخت', max_length=50)
    
    def __str__(self):
        return self.payment_title
    
    class Meta:
        verbose_name='نوع پرداخت'
        verbose_name_plural='انواع پرداخت'



class Order(models.Model):
    customer=models.ForeignKey(Customer, verbose_name='مشتری', on_delete=models.CASCADE,related_name='orders')
    register_date=models.DateField(default=timezone.now,verbose_name='تاریخ درج سفارش')
    update_date=models.DateField(auto_now=True,verbose_name='تاریخ ویرایش سفارش')
    is_finaly=models.BooleanField(default=False,verbose_name='نهایی شده/نهایی نشده')
    order_code=models.UUIDField(unique=True,default=uuid.uuid4,editable=False,verbose_name='کد تولید برای سفارش')
    discount=models.IntegerField(blank=True,null=True,default=0,verbose_name='تخفیف روی فاکتور')
    descrition=models.TextField(verbose_name='توضیحات',null=True,blank=True)
    ref_id=models.CharField(verbose_name='کد پیگیری سفارش', max_length=30,null=True,blank=True,editable=False, unique=True)
    payment_type=models.ForeignKey(PaymentType, verbose_name='نوع پرداخت', on_delete=models.CASCADE,null=True,blank=True,related_name='payment_types')
    order_state=models.ForeignKey(OrderState, verbose_name='وضعیت سفارش', on_delete=models.CASCADE,related_name='orders_states',null=True,blank=True)    
    
    def get_order_total_price(self):
        sum=0
        for item in self.orders_details1.all():
            sum+=item.product.get_price_by_discount()*item.qty
        
        order_final_price,delivery,tax=utils.price_by_delivery_tax(sum,self.discount)
        
        return int(order_final_price*10)
    
    
    def __str__(self):
        return f'{self.customer}\t{self.id}\t{self.is_finaly}'
    
    class Meta:
        verbose_name='سفارش'
        verbose_name_plural='سفارشات'
        

class OrderDetails(models.Model):
    order=models.ForeignKey(Order, verbose_name='سفارش', on_delete=models.CASCADE,related_name='orders_details1')
    product=models.ForeignKey(Product, verbose_name='کالا', on_delete=models.CASCADE,related_name='orders_details2')
    qty=models.PositiveIntegerField(verbose_name='تعداد کالا',default=1)
    price=models.IntegerField(verbose_name='قیمت کالا در فاکتور')
    
    def __str__(self):
        return f'{self.order}\t{self.product}\t{self.qty}\t{self.price}'


