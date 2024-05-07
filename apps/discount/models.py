from django.db import models
from django.core.validators import MinValueValidator,MaxValueValidator
from apps.product.models import Product


class Coupon(models.Model):
    coupon_code=models.CharField(unique=True, max_length=10,verbose_name='کد کوپن')
    start_date=models.DateTimeField(verbose_name='تاریخ شروع')
    end_date=models.DateTimeField(verbose_name='تاریخ پایان')
    discount=models.IntegerField(verbose_name='درصد تخفیف',validators=[MinValueValidator(0),MaxValueValidator(100)])
    is_active=models.BooleanField(verbose_name='فعال/غیرفعال',default=False)
    def __str__(self):
        return self.coupon_code
    class Meta:
        verbose_name='کد تخفیف'
        verbose_name_plural='کد های تخفیف'
        
        
#--------------------------------------------------------------------------------------------

class DiscountBasket(models.Model):
    discount_title=models.CharField(unique=True, max_length=10,verbose_name='عنوان سبد خرید')
    start_date1=models.DateTimeField(verbose_name='تاریخ شروع')
    end_date1=models.DateTimeField(verbose_name='تاریخ پایان')
    discount=models.IntegerField(verbose_name='درصد تخفیف',validators=[MinValueValidator(0),MaxValueValidator(100)])
    is_active=models.BooleanField(verbose_name='فعال/غیرفعال',default=False)
    def __str__(self):
        return self.discount_title
    class Meta:
        verbose_name='سبد خرید'
        verbose_name_plural='سبد های خرید'
        
#--------------------------------------------------------------------------------------------

class DiscountBasketDetails(models.Model):
    discount_basket=models.ForeignKey(DiscountBasket, verbose_name='سبد خرید', on_delete=models.CASCADE,related_name='discount_basket_details1')
    product=models.ForeignKey(Product, verbose_name='کالا', on_delete=models.CASCADE,null=True,blank=True,related_name='discount_basket_details2')