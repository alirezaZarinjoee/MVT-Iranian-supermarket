from django.shortcuts import render,redirect
from .forms import RegisterForm,VerifyForm,LoginForm,ChangePasswordForm,GetMobileNumberForChangePasswordForm,UpdateProfileForm
from django.views import View
from . models import CustomUser,Customer
from utils import crete_random,send_sms1
from django.contrib import messages
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.mixins import LoginRequiredMixin
from apps.orders.models import Order
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.decorators import login_required
#نکته:اول فایل توضیحات اپلیکیشن اکانتینگ را بخوانید سپس کد ها را ببینید

class RegisterView(View):   #تابع ثبت نام
    template_name='account/register.html'
    
    def dispatch(self,request,*args,**kwargs):
        if request.user.is_authenticated:  # اگر کاربر لاگین کرده باشد و قصد ورود به این صفحه را داشته باشد توسط این تابع از ورود ان جلوگیری میشود
            messages.warning(request,'برای ثبت نام کاربر دیگر باید از بخش حساب کاربری دکمه خروج را زده و سپس امتحان کنید','warning')
            return redirect('main:main')   
        return super().dispatch(request, *args, **kwargs)
    
    
    def get(self,request,*args,**kwargs):
        form=RegisterForm()
        return render(request,self.template_name,{'form':form})
    
    
    def post(self,request,*args,**kwargs):
            form=RegisterForm(request.POST)
            if form.is_valid():
                data=form.cleaned_data
                active_code=crete_random(5) #تولید کد رندوم برای فعال سازی کاربر
                print('+++++++++++++++++++++++++++++++++')
                print(active_code) # نمایش کد در ترمینال
                print('*********************************')
                send_sms1(data['mobile_number'],str(active_code))# تابع ارسال کد فعالسازی به کاربر
                request.session['session_user']={      #ذخیره اطلاعات فرم ثبت نام درون سشن برای استفاده در کلاس وریفای
                    'active_code':str(active_code),
                    'mobile_number':data['mobile_number'],
                    'password':data['password1'],
                    'remember_password':False #برای علامت گذاری میباشد که با سشن تغییر رمز قاطی نشود
                }
                messages.success(request,'کد فعال سازی با موفقیت ارسال شد','success')
                return redirect('account:verify_view')
            messages.error(request,'این حساب کاربری از قبل وجود دارد','danger')
            return render(request,self.template_name,{'form':form})
            



            
#_______________________________________________________________________
class VerifyView(View):#تابع بررسی صحت کد فعال سازی
    template_name='account/verify.html'
    
    def dispatch(self,request,*args,**kwargs):
        if request.user.is_authenticated: # اگر کاربر لاگین کرده باشد و قصد ورود به این صفحه را داشته باشد توسط این تابع از ورود ان جلوگیری میشود
            return redirect('main:main')
        return super().dispatch(request, *args, **kwargs)
        
    def get(self,request,*args,**kwargs):
        form=VerifyForm()
        return render(request,self.template_name,{'form':form})
    
    def post(self,request,*args,**kwargs):
        form=VerifyForm(request.POST)
        session_user=request.session['session_user'] #واکشی سشن
        if form.is_valid():
            data=form.cleaned_data
            if session_user['active_code']==data['active_code']: 
                if session_user['remember_password']==False:#گفتیم اگر سشن از طرف فرم رجیستر اومده فعالیت های زیر را انجام بده
                    CustomUser.objects.creat_user(
                    mobile_number=session_user['mobile_number'],
                    active_code=session_user['active_code'],
                    password=session_user['password']
                    )
                    #بعد از اینکه کاربر ثبت نام شد ، ان را پیدا میکنیم تا هم فعالش کنیم و هم کد فعال سازیش رو تغییر بدیم
                    user=CustomUser.objects.get(mobile_number=session_user['mobile_number'])
                    user.is_active=True
                    user.active_code=crete_random(5)
                    user.save()
                    
                    user_athen=authenticate(username=session_user['mobile_number'],password=session_user['password']) #برای پیدا کردن کاربر میباشد
                    if user_athen is not None:
                        login(request,user) #در اینجا کاربر لاگین میشود
                        
                    
                    messages.success(request,'ثبت نام با موفقیت انجام شد','success')
                
                    if 'next_url' in request.session: #  را درون سشن قرار میدهیم تا در اینجا ازش استفادده کنیمnext_urlما چون هنگام ثبت نام کاربر رو هم لاگین میکنیم ، میخواهیم به همان صفحه ایی برگردد که از انجا به فرم لاگین هدایت شده برای همین ما 
                        nextUrl=request.session['next_url']
                        #در اینجا چون مرحله اخر است هر دو سشن را حذف میکنیم
                        del session_user 
                        del request.session['next_url']
                        
                        return redirect(nextUrl)
                    else:
                        del session_user
                        return redirect('main:main')
                else:
                    return redirect('account:changepassword_view')
            else:
                messages.error(request,'کد وارد شده اشتباه می باشد','danger')
                return render(request,self.template_name,{'form':form})
        else:
            del session_user
            messages.error(request,'اطلاعات وارد شده صحیح نمیباشد','danger')
            return render(request,self.template_name,{'form':form})

#_______________________________________________________________________

class LoginView(View):# فرم لاگین یا ورود
    template_name='account/login.html'
    
    def dispatch(self,request,*args,**kwargs):
        if request.user.is_authenticated:  # اگر کاربر لاگین کرده باشد و قصد ورود به این صفحه را داشته باشد توسط این تابع از ورود ان جلوگیری میشود
            messages.warning(request,'برای ورود کاربر دیگر باید از بخش حساب کاربری دکمه خروج را زده و سپس امتحان کنید','warning')
            return redirect('main:main')
        return super().dispatch(request, *args, **kwargs)
    
    def get(self,request,*args,**kwargs):
        form=LoginForm()
        #وقتی میخواهیم به صفحه ایی ورود کنیم که باید لاگین کرده باشیم ، سیستم ما رو به سمت صفحه لاگین هدایت میکند.ولی ممکن است کاربری ثبت نام نکرده باشد
        #را تعریف کردیم و درون یک سشن گذاشتیم تا زمان ثبت نام کاربر پس از اینکه اتوماتیک لاگین شد،به همان صفحه بازگرددnext_url و بخواهد بر روی دکمه ثبت نام بزند.بخاطر همین در همین بخش برای خودمون
        next_url=request.GET.get('next')
        if next_url is not None:
            request.session['next_url']=next_url
        return render(request,self.template_name,{'form':form})
    
    def post(self,request,*args,**kwargs):
        form=LoginForm(request.POST)
        if form.is_valid():
            data=form.cleaned_data
            user=authenticate(username=data['mobile_number'],password=data['password'])
            if user is not None:
                db_user=CustomUser.objects.get(mobile_number=data['mobile_number'])
                if db_user.is_admin==False: # اگر کاربر ما ادمین نباشد میتواند از این بخش ورود کند
                    login(request,user)
                    messages.success(request,'ورود با موفقیت انجام شد','success')
                    next_url=request.GET.get('next')
                    if next_url is not None:
                        request.session['next_url']=next_url # در سشن برای کاربران ثبت نامی next_urlذخیره سازی 
                        return redirect(next_url)
                    else:
                        return redirect('main:main')
                else:
                    messages.error(request,'کاربر ادمین نمیتواند از اینجا وارد شود','warning')
                    return render(request,self.template_name,{'form':form})
            else:
                messages.error(request,'رمز یا نام کاربری اشتباه میباشد','warning')
                return render(request,self.template_name,{'form':form})
        else:
            messages.error(request,'اطلاعات وارد شده معتبر نمیباشد','warning')
            return render(request,self.template_name,{'form':form})
                           
#______________________________________________________________________   
class LogoutView(View):
    def dispatch(self,request,*args,**kwargs):
        if not request.user.is_authenticated:   #به کمک این ، اگر کاربری لاگین نکرده باشد نمیتواند این کلاس را اجرا کند
            messages.warning(request,'شما هنوز وارد نشدید که بخواهید خارج شوید','warning')
            return redirect('main:main')
        return super().dispatch(request, *args, **kwargs)    
    
    def get(self,request,*args,**kwargs):
        session_data=request.session.get('shop_cart')
        logout(request)  #از حساب کاربری توسط این متد خارج میشود
        request.session['shop_cart']=session_data
        messages.success(request,'خروج با موفقیت انجام شد','success')
        return redirect('main:main')

#_____________________________________________________________________
class UserPanelView(LoginRequiredMixin,View):  #پنل کاربران
    template_name='account/userpanel.html'
    def get(self,request):
        user=request.user
        try:
            customer=Customer.objects.get(user=request.user)
            user_info={
                'name':user.name,
                'family':user.family,
                'email':user.email,
                'phone_number':customer.phone_number,
                'address':customer.address,
                'image_name':customer.image_name,
            }
        except ObjectDoesNotExist:
            user_info={
                'name':user.name,
                'family':user.family,
                'email':user.email,
            }
        return render(request,'account/userpanel.html',{'user_info':user_info})
#_____________________________________________________________________
@login_required(login_url='/account/login_view/')
def show_last_orders(request):
    orders=Order.objects.filter(customer_id=request.user.id).order_by('-register_date')[:4]
    return render(request,'account/show_last_orders.html',{'orders':orders})

#_____________________________________________________________________
class ChangePasswordView(View): # کلاس تغییر رمز کاربران
    template_name='account/changepassword.html'
    def get(self,request,*args,**kwargs):
        form=ChangePasswordForm()
        return render(request,self.template_name,{'form':form})
    
    def post(self,request,*args,**kwargs):
        form=ChangePasswordForm(request.POST)
        if form.is_valid():
            data=form.cleaned_data
            session_user=request.session['session_user']#واکشی سشنی که از کلاس پایین میاد
            user=CustomUser.objects.get(mobile_number=session_user['mobile_number'])
            user.set_password(data['password1'])
            user.active_code=crete_random(5)
            user.save()
            messages.success(request,'رمز عبور شما با موفقیت تغییر کرد','success')
            del session_user
            return redirect('account:login_view')
        else:
            messages.error(request,'اطلاعات وارد شده نا معتبر میباشد','danger')
            return render(request,self.template_name,{'form':form})
            
                        
        
    
#_____________________________________________________________________
class GetMobileNumberForChangePasswordView(View): # کلاس گرفتن شماره موبایل برای تغییر رمز 
    template_name='account/get_mobile_number_for_change_password.html'
    def get(self,request,*args,**kwargs):
        form=GetMobileNumberForChangePasswordForm()
        return render(request,self.template_name,{'form':form})
    
    def post(self,request,*args,**kwargs):
        form=GetMobileNumberForChangePasswordForm(request.POST)
        if form.is_valid():
            try:
                data=form.cleaned_data
                user=CustomUser.objects.get(mobile_number=data['mobile_number'])
                active_code=crete_random(5)
                print('========================')
                print(active_code)
                print('========================')
                user.active_code=active_code
                user.save()
                send_sms1(data['mobile_number'],active_code)
                request.session['session_user']={
                    'active_code':str(active_code),
                    'mobile_number':data['mobile_number'],
                    'password':' ',
                    'remember_password':True
                }
                messages.success(request,'جهت تغییر رمز عبور خد، کد دریافتی را ارسال کنید','success')
                return redirect('account:verify_view')
            except:
                messages.error(request,'شماره موبایل وارد شده موجود نمیباشد','danger')
                return render(request,self.template_name,{'form':form})
                
                

                
            
#_____________________________________________________________________

class UpdateProfileView(LoginRequiredMixin,View):
    def get(self,request):
        user=request.user
        try:
            customer=Customer.objects.get(user=request.user)
            initial_dict={
                'mobile_number':user.mobile_number,
                'name':user.name,
                'family':user.family,
                'email':user.email,
                'phone_number':customer.phone_number,
                'address':customer.address,

            }
            image_url=customer.image_name
        except ObjectDoesNotExist:
            initial_dict={
                'mobile_number':user.mobile_number,
                'name':user.name,
                'family':user.family,
                'email':user.email,
            }
            image_url=None
        
        form=UpdateProfileForm(initial=initial_dict)
        
        return render(request,'account/update_profile.html',{'form':form,'image_url':image_url})
    
    def post(self,request):
        form=UpdateProfileForm(request.POST,request.FILES)
        if form.is_valid():
            cd=form.cleaned_data
            user=request.user
            user.name=cd['name']
            user.family=cd['family']
            user.email=cd['email']
            user.save()
            try:
                customer=Customer.objects.get(user=request.user)
                if customer.image_name:
                    customer.phone_number=cd['phone_number']
                    customer.address=cd['address']
                else:
                    customer.phone_number=cd['phone_number']
                    customer.address=cd['address']
                    customer.image_name=cd['image']
                customer.save()
            except ObjectDoesNotExist:
                Customer.objects.create(
                    user=request.user,
                    phone_number=cd['phone_number'],
                    address=cd['address'],
                    image_name=cd['image'],
                )
            messages.success(request,'ویرایش پروفایل با موفقیت انجام شد','success')
            return redirect('account:userpanel_view')
        else:
            messages.error(request,'اطلاعات وارد شده معتبر نمیباشد','danger')
            return render(request,'account/update_profile.html',{'form':form})
            
    
        