from django.db import models
from utils import FileUpload,reaplace_dash_to_space
from django.utils import timezone
from django.utils.text import slugify
from unidecode import unidecode
from ckeditor_uploader.fields import RichTextUploadingField
from django.urls import reverse
from datetime import datetime
from django.db.models import Sum,Avg
from middlewares.middlewares import RequestMiddleware
# Create your models here.
#________________________________________________________________________________

class Brand(models.Model):
    brand_title=models.CharField(verbose_name='برند', max_length=100)
    file_upload=FileUpload('images','brand')
    image_name=models.ImageField(upload_to=file_upload.upload_to,verbose_name='تصویر کالا')
    slug=models.SlugField(unique=True,max_length=200,null=True,blank=True)
    
    def __str__(self):
        return self.brand_title
    
    def save(self, *args, **kwargs):
        if not self.slug:
            new_slug = reaplace_dash_to_space(self.brand_title)
            self.slug = slugify(unidecode(new_slug))
        super().save(*args, **kwargs)
    
    class Meta:
        verbose_name='برند'
        verbose_name_plural='برندها'
    


#________________________________________________________________________________

class ProductGroup(models.Model):
    group_title=models.CharField(max_length=100,verbose_name='عنوان گروه کالا')
    file_upload=FileUpload('images','product_group')
    image_name=models.ImageField(upload_to=file_upload.upload_to,verbose_name='تصویر گروه')
    description=models.TextField(verbose_name='توضیحات',null=True,blank=True)
    is_active=models.BooleanField(verbose_name='وضعیت فعال/غیرفعال',default=True,blank=True)
    group_parent=models.ForeignKey('ProductGroup', verbose_name='والد گروه کالا', on_delete=models.CASCADE,related_name='groups',null=True,blank=True)
    slug=models.SlugField(unique=True,max_length=200,null=True,blank=True)
    register_date=models.DateTimeField(verbose_name='تاریخ ثبت', auto_now_add=True)
    update_date=models.DateTimeField(verbose_name='تاریخ اخرین بروزرسانی', auto_now=True)
    published_date=models.DateTimeField(verbose_name='تاریخ انتشار',default=timezone.now)
    
    def __str__(self):
        return self.group_title
    
    def save(self, *args, **kwargs):
        if not self.slug:
            new_slug = reaplace_dash_to_space(self.group_title)
            self.slug = slugify(unidecode(new_slug))
        super().save(*args, **kwargs)
    
    class Meta:
        verbose_name = 'گروه کالا'
        verbose_name_plural = 'گروه های کالا'
        
#________________________________________________________________________________

class Feature(models.Model):
    feature_name=models.CharField(verbose_name='نام ویژگی', max_length=100)
    product_group=models.ManyToManyField(ProductGroup, verbose_name='گروه کالا',related_name='features_of_groups')
    
    def __str__(self):
        return self.feature_name

    class Meta:
        verbose_name = 'ویژگی'
        verbose_name_plural = 'ویژگی ها'    
        
#________________________________________________________________________________

class Product(models.Model):
    product_name=models.CharField(verbose_name='نام کالا', max_length=500)
    # description=models.TextField(verbose_name='توضیحات',null=True,blank=True)
    summery_description=models.TextField(default='',null=True,blank=True,verbose_name='خلاصه توضیحات')
    description=RichTextUploadingField(verbose_name='توضیحات',null=True,blank=True)
    file_upload=FileUpload('images','product')
    image_name=models.ImageField(verbose_name='نام تصویر', upload_to=file_upload.upload_to)
    price=models.PositiveIntegerField(default=0,verbose_name='قیمت کالا')
    product_group=models.ManyToManyField(ProductGroup, verbose_name='گروه های کالا',related_name='products_of_groups')
    brand=models.ForeignKey(Brand, verbose_name='برند کالا', on_delete=models.CASCADE,related_name='brands')
    is_active=models.BooleanField(verbose_name='وضعیت فعال/غیرفعال',default=True,blank=True)
    slug=models.SlugField(unique=True,max_length=200,null=True,blank=True)
    register_date=models.DateTimeField(verbose_name='تاریخ ثبت', auto_now_add=True)
    update_date=models.DateTimeField(verbose_name='تاریخ اخرین بروزرسانی', auto_now=True)
    published_date=models.DateTimeField(verbose_name='تاریخ انتشار',default=timezone.now)
    feature=models.ManyToManyField(Feature, verbose_name='ویژگی کالا',through='ProductFeature')
    @property
    def groupid(self):
        return self.product_group.id
    
    def __str__(self):
        return self.product_name
    
    def get_absolute_url(self):
        return reverse("product:product_details", kwargs={"slug": self.slug})
    
    #محسابه قیمت با تخفیف اگر براش وجود داشت
    def get_price_by_discount(self):
        list1=[]
        current_time=datetime.now()
        for dbd in self.discount_basket_details2.all():
            if (dbd.discount_basket.is_active==True and 
                dbd.discount_basket.start_date1 <= current_time and 
                current_time <= dbd.discount_basket.end_date1):
                list1.append(dbd.discount_basket.discount)

        discount=0
        if (len(list1)>0):
            discount=max(list1)
        return self.price-(self.price*discount/100)
    
    #گرفتن تعداد کالای موجود در انبار
    def get_number_in_warehose(self):
        sum1=self.warehouse_products.filter(warehouse_type_id=1).aggregate(Sum('qty'))
        sum2=self.warehouse_products.filter(warehouse_type_id=2).aggregate(Sum('qty'))
    
        input=0
        if sum1['qty__sum']!=None:
            input=sum1['qty__sum']
        output=0
        if sum2['qty__sum']!=None:
            output=sum2['qty__sum']
            
        return input-output
        
        
    #میانگین امتیازات یک کالا   
    def get_avrage_score(self):
        avgScore=self.scoring_product.all().aggregate(Avg('score'))['score__avg']
        if avgScore==None:
            avgScore=0
        return avgScore

    #میزان امتیازی که کاربر به کالای ما داده
    def get_user_score(self):
        request=RequestMiddleware(get_response=None)
        request=request.thread_local.current_request
        
        score=0
        
        user_score=self.scoring_product.filter(scoring_user=request.user)
        if user_score.count()>0:
            score=user_score[0].score
        return score
    
    #ایا این کالا مورد علاقه کاربر جاری بوده یا نه
    def get_user_favorite(self):
        request=RequestMiddleware(get_response=None)
        request=request.thread_local.current_request
        flag=self.favorite_product.filter(favorite_user=request.user).exists()
        return flag
    
    def getMainProductGroup(self):
        return self.product_group.all()[0].id
        
    def save(self, *args, **kwargs):
        if not self.slug:
            new_slug = reaplace_dash_to_space(self.product_name)
            self.slug = slugify(unidecode(new_slug))
        super().save(*args, **kwargs)
    
    class Meta:
        verbose_name = 'کالا'
        verbose_name_plural = 'کالا ها'
#________________________________________________________________________________
class FeatureValue(models.Model):
    value_title=models.CharField(verbose_name='عنوان مقدار ویژگی', max_length=123)
    feature=models.ForeignKey(Feature, verbose_name='ویژگی', on_delete=models.CASCADE,related_name='feature_value')
    
    def __str__(self):
        return f'{self.value_title}'
    
    class Meta:
        verbose_name='مقدار ویژگی'
        verbose_name_plural='مقادیر ویژگی ها'

#________________________________________________________________________________

class ProductFeature(models.Model):
    product=models.ForeignKey(Product, verbose_name='کالا', on_delete=models.CASCADE,related_name='product_features')
    feature=models.ForeignKey(Feature, verbose_name='ویژگی', on_delete=models.CASCADE)
    value=models.CharField(verbose_name='مقدار ویژگی', max_length=100)
    filter_value=models.ForeignKey(FeatureValue, verbose_name='مققدار ویژگی برای فیلتر',null=True,blank=True, on_delete=models.CASCADE,related_name='filter_values')
    
    
    @property
    def productid(self):
        return self.product.id

    
    def __str__(self):
        return f'{self.product}-{self.feature} : {self.value}'
    
    class Meta:

        verbose_name = 'ویژگی محصول'
        verbose_name_plural = 'ویژگی محصولات'
        
#________________________________________________________________________________

class ProductGallery(models.Model):
    product=models.ForeignKey(Product, verbose_name='نام کالا', on_delete=models.CASCADE,related_name='gallery_images')
    file_upload=FileUpload('images','product_gallery')
    image_name=models.ImageField(verbose_name='تصویر کالا', upload_to=file_upload.upload_to)
    
    class Meta:
        db_table = ''
        managed = True
        verbose_name = 'تصویر'
        verbose_name_plural = 'تصاویر'
        
        
        
        
        
        
        
        



