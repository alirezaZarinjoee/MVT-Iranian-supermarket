from django.db import models
from django.contrib.auth.models import AbstractBaseUser,PermissionsMixin,BaseUserManager
from django.utils import timezone
from utils import FileUpload

#_____________________________________________________________________________________________________
class CustomUserManager(BaseUserManager):
    
    def creat_user(self,mobile_number,email='',name='',family='',active_code=None,gender=None,password=None):
        if not mobile_number:
            raise ValueError('شماره موبایل باید وارد شود')
        user=self.model(
            mobile_number=mobile_number,
            email=self.normalize_email(email),
            name=name,
            family=family,
            active_code=active_code,
            gender=gender
        )
        user.set_password(password)
        user.save(using=self._db)
        return user
    #-------------------
    def create_superuser(self,mobile_number,email,name,family,password=None,active_code=None,gender=None):
        user=self.creat_user(
            mobile_number=mobile_number,
            email=email,
            name=name,
            family=family,
            active_code=active_code,
            gender=gender,
            password=password
            
        )
        user.is_active=True
        user.is_admin=True
        user.is_superuser=True
        user.save(using=self._db)
        return user
    


#_____________________________________________________________________________________________________
class CustomUser(AbstractBaseUser,PermissionsMixin):
    mobile_number=models.CharField(verbose_name='شماره تماس', max_length=11,unique=True)
    email=models.EmailField(verbose_name='ایمیل', max_length=254,blank=True)
    name=models.CharField(verbose_name='نام', max_length=50,blank=True)
    family=models.CharField(verbose_name='نام خانوادگی', max_length=50,blank=True)
    GENDER_CHOICES=(('True','مرد'),('False','زن'))
    gender=models.CharField(verbose_name='جنسیت', max_length=50,choices=GENDER_CHOICES,default='True',null=True,blank=True)
    register_date=models.DateTimeField(verbose_name='تاریخ اضافه شدن',default=timezone.now)
    is_active=models.BooleanField(verbose_name='فعال/غیرفعال',default=False)
    active_code=models.CharField(verbose_name='کد فعال سازی',max_length=100,null=True,blank=True)
    is_admin=models.BooleanField(verbose_name='ادمین',default=False)
    USERNAME_FIELD='mobile_number'
    REQUIRED_FIELDS=['email','name','family']
    
    objects=CustomUserManager()
    
    def __str__(self):
        return self.name+' '+self.family
    
    @property
    def is_staff(self):
        return self.is_admin
    
    class Meta:
        verbose_name = 'کاربر'
        verbose_name_plural = 'کاربران'
        
#_____________________________________________________________________________________________________
class Customer(models.Model):
    user=models.OneToOneField(CustomUser, verbose_name='کاربر', on_delete=models.CASCADE,primary_key=True)
    phone_number=models.CharField(verbose_name='شماره تلفن', max_length=11,null=True,blank=True)
    address=models.TextField(verbose_name='ادرس',null=True,blank=True)
    file_upload=FileUpload('images','customer')
    image_name=models.ImageField(upload_to=file_upload.upload_to,verbose_name='تصویر پروفایل',null=True,blank=True)
    
    def __str__(self):
        return f'{self.user}'
    