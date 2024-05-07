from django import forms
from django.forms import ModelForm
from .models import CustomUser
from django.core.exceptions import ValidationError
from django.contrib.auth.forms import ReadOnlyPasswordHashField

class UserCreationForm(forms.ModelForm):#فرم ساخت کاربر درون پنل ادمین
    password1=forms.CharField(label='رمز',widget=forms.PasswordInput)
    password2=forms.CharField(label='تکرار رمز',widget=forms.PasswordInput)
    
    class Meta:
        model=CustomUser
        fields=['mobile_number','email','family','gender']
    def clean_password2(self):
        pass1 = self.cleaned_data["password1"]
        pass2 = self.cleaned_data["password2"]
        if pass1 and pass2 and pass1!=pass2:
            raise ValidationError('رمز و تکرار ان با هم مغایرت دارند')
        
        return pass2
        
    def save(self,commit=True):#تابع کامیت برای کنترل کردن فرایند ذخیره سازی .
                                #این تابع برای هش کردن پسورد بیشتر به کار رفته تا اول کار پسورد را هش کرده و به 
                                #درون دیتا بیس بفرستد
        user=super().save(commit=False)
        user.set_password(self.cleaned_data['password1'])
        if commit:
            user.save()
        return user
                
#_______________________________________________________________________________
class UserChangeForm(forms.ModelForm):#تابع ویرایش کاربر در پنل ادمین
    password=ReadOnlyPasswordHashField(help_text='برای تغییر رمز روی این <a href="../password">لینک</a> کلیک کنید')
    class Meta:
        model:CustomUser
        fields=['mobile_number','password','email','name','family','gender','is_active','is_admin']
        
#_______________________________________________________________________________
class RegisterForm(ModelForm): #فرم وارد کردن اطلاعاعات برای ثبت نام
    password1=forms.CharField(label='رمز عبور',
                              widget=forms.PasswordInput(attrs={'class':'form-control','placeholder':'رمز عبور را وارد کنید'}),)
    password2=forms.CharField(label='تکرار رمز عبور ',
                              widget=forms.PasswordInput(attrs={'class':'form-control','placeholder':'تکرار رمز عبور را وارد کنید'}),)
    class Meta:
        model=CustomUser
        fields=['mobile_number',]
        widgets={
            'mobile_number':forms.TextInput(attrs={'class':'form-control','placeholder':'موبایل را وارد کنید'},),
            }
        
    def clean_password2(self):
        password1 = self.cleaned_data["password1"]
        password2 = self.cleaned_data["password2"]
        if password1 and password2 and password1!=password2:
            raise ValidationError('رمز عبور و تکرار ان با یک دیگر مغایرت دارند')
        return password2
#________________________________________________________________________________
class VerifyForm(forms.Form):#فرم تایید کد کاربری
    active_code=forms.CharField(label='',
                                error_messages={'requierd':'این فیلد نمیتواند خالی باشد'},
                                widget=forms.TextInput(attrs={'class':'form-control','placeholder':'کد فعال سازی را وارد کنید'}))

#_______________________________________________________________________________
class LoginForm(forms.Form):#فرم لاگین یا ورود
    mobile_number=forms.CharField(label='شماره موبایل',
                                  error_messages={'requierd':'این فیلد نمیتواند خالی باشد'},
                                  widget=forms.TextInput(attrs={'class':'form-control','placeholder':'شماره موبایل را وارد کنید'}))
    
    password=forms.CharField(label='رمز عبور',
                                  error_messages={'requierd':'این فیلد نمیتواند خالی باشد'},
                                  widget=forms.PasswordInput(attrs={'class':'form-control','placeholder':'رمز عبور را وارد کنید'}))

#_______________________________________________________________________________
class ChangePasswordForm(forms.Form):#فرم عوض کردن پسورد
    password1=forms.CharField(label='رمز عبور جدید',error_messages={'requierd':'این فیلد نمیتواند خالی باشد'},
                              widget=forms.PasswordInput(attrs={'class':'form-control','placeholder':'رمز عبور جدید وارد کنید'}),)
    password2=forms.CharField(label='تکرار رمز عبور ',error_messages={'requierd':'این فیلد نمیتواند خالی باشد'},
                              widget=forms.PasswordInput(attrs={'class':'form-control','placeholder':'تکرار رمز عبور را وارد کنید'}),)
    def clean_password2(self):
        password1 = self.cleaned_data["password1"]
        password2 = self.cleaned_data["password2"]
        if password1 and password2 and password1!=password2:
            raise ValidationError('رمز عبور و تکرار ان با یک دیگر مغایرت دارند')
        return password2
#_______________________________________________________________________________
class GetMobileNumberForChangePasswordForm(forms.Form):#فرم گرفتن شماره موبایل برای تغییر رمز
    mobile_number=forms.CharField(label='شماره موبایل',
                                  error_messages={'requierd':'این فیلد نمیتواند خالی باشد'},
                                  widget=forms.TextInput(attrs={'class':'form-control','placeholder':'شماره موبایل را وارد کنید'}))
    
    
#_______________________________________________________________________________
class UpdateProfileForm(forms.Form):
    mobile_number=forms.CharField(label='', max_length=11,
                                  widget=forms.TextInput(attrs={'class':'form-control','placeholder':'شماره موبایل را وارد کنید','readonly':'readonly'}))
    
    name=forms.CharField(label='',error_messages={'required':'این فیلد نمیتواند خالی باشد'},
                                  widget=forms.TextInput(attrs={'class':'form-control','placeholder':' نام را وارد کنید'}))
    
    family=forms.CharField(label='',error_messages={'required':'این فیلد نمیتواند خالی باشد'},
                                  widget=forms.TextInput(attrs={'class':'form-control','placeholder':' نام خانوادگی را وارد کنید'}))
    
    email=forms.EmailField(label='',error_messages={'required':'این فیلد نمیتواند خالی باشد'},
                                  widget=forms.EmailInput(attrs={'class':'form-control','placeholder':' ایمیل را وارد کنید'}))

    phone_number=forms.CharField(label='',error_messages={'required':'این فیلد نمیتواند خالی باشد'},
                                  widget=forms.TextInput(attrs={'class':'form-control','placeholder':' تلفن ثابت خود را وارد کنید'}))

    address=forms.CharField(label='',error_messages={'required':'این فیلد نمیتواند خالی باشد'},
                                  widget=forms.Textarea(attrs={'class':'form-control','placeholder':'  ادرس خود را وارد کنید'}))
    
    image=forms.ImageField(required=False)