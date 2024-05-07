from django.db import models
from apps.product.models import Product
from apps.account.models import CustomUser
from django.core.validators import MinValueValidator,MaxValueValidator

# Create your models here.

class Comment(models.Model):
    product=models.ForeignKey(Product, verbose_name='کالا', on_delete=models.CASCADE,related_name='comments_product')
    commenting_user=models.ForeignKey(CustomUser, verbose_name='کاربر نظر دهنده', on_delete=models.CASCADE,related_name='comments_user1')
    approving_user=models.ForeignKey(CustomUser, verbose_name='کاربر تایید کننده نظر', on_delete=models.CASCADE,related_name='comments_user2',null=True,blank=True)
    comment_text=models.TextField(verbose_name='متن نظر')
    register_date=models.DateTimeField(verbose_name='تاریخ ثبت نظر', auto_now_add=True)
    is_active=models.BooleanField(verbose_name='وضعیت فعال/غیرفعال',default=False)
    comment_parent=models.ForeignKey('Comment', verbose_name='والد نظر', on_delete=models.CASCADE,null=True,blank=True,related_name='comments_child')
    
    def __str__(self):
        return f'{self.product} {self.commenting_user}'
    
    class Meta:
        verbose_name='نظر'
        verbose_name_plural='نظرات'
        
        
        
class scoring(models.Model):
    product=models.ForeignKey(Product, verbose_name='کالا', on_delete=models.CASCADE,related_name='scoring_product')
    scoring_user=models.ForeignKey(CustomUser, verbose_name='کاربر امتیاز دهنده', on_delete=models.CASCADE,related_name='scoring_user1')
    register_date=models.DateTimeField(verbose_name='تاریخ درج امتیاز',auto_now_add=True)
    score=models.PositiveSmallIntegerField(validators=[MinValueValidator(0),MaxValueValidator(5)],verbose_name='امتیاز')
    
    def __str__(self):
        return f'{self.product} {self.scoring_user}'
    
    class Meta:
        verbose_name='امتیاز'
        verbose_name_plural='امتیازات'



class Favorite(models.Model):
    product=models.ForeignKey(Product, verbose_name='کالا', on_delete=models.CASCADE,related_name='favorite_product')
    favorite_user=models.ForeignKey(CustomUser, verbose_name='کاربر علاقه مند', on_delete=models.CASCADE,related_name='favorite_user1')
    register_date=models.DateTimeField(auto_now_add=True,verbose_name='تاریخ درج')
    
    def __str__(self):
        return f'{self.product} {self.favorite_user}'
    
    class Meta:
        verbose_name='علاقه مندی'
        verbose_name_plural='علاقه مندی ها'
        
    