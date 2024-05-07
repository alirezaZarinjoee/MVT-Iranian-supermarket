from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.http.request import HttpRequest
from .forms import *
from .models import CustomUser,Customer
from django.http import HttpResponseForbidden



class CustomUserAdmin(UserAdmin):
    form=UserChangeForm
    add_form=UserCreationForm
    list_display=('mobile_number','email','name','family','gender','is_active','is_admin',)
    list_filter=('is_active','is_admin')
    list_editable=['is_active','is_admin']
    
    
    fieldsets=(
        (None,{'fields':('mobile_number','password')}),
        ('personal info',{'fields':('email','name','family','gender','active_code')}),
        ('permissions',{'fields':('is_active','is_admin','is_superuser','user_permissions','groups')}),
    )
    add_fieldsets=(
        (None,{'fields':('mobile_number','email','name','family','gender','password1','password2')}),
        
    )

    search_fields=('mobile_number',)
    ordering=('mobile_number',)
    filter_horizontal=('user_permissions','groups')
    
    
    #این تابع پایین برای محدود کردن دسترسی مدیران به یک دیگر و همچنین محدود کردن مدیران نسبت به کاربران سوپریوزر و محدود کردن دسترسی سوپریوزر ها نسبت به هم است
    def change_view(self, request, object_id, form_url='', extra_context=None):
        if CustomUser.objects.filter(pk=object_id, is_superuser=True).exists() and request.user.is_superuser is False:
            return HttpResponseForbidden('<h1 style="color:red; text-align:center;">You do not have permission to change and view and delete this user.</h1>')
        
        if CustomUser.objects.filter(pk=object_id, is_admin=True).exists() and request.user.is_superuser is False:
            return HttpResponseForbidden('<h1 style="color:red; text-align:center;">You do not have permission to change and view and delete this user.</h1>')
        
        if CustomUser.objects.filter(pk=object_id, is_superuser=True).exists() and request.user.is_superuser is True:
            return HttpResponseForbidden('<h1 style="color:black; text-align:center;">this user is SUPERUSER and you do not  have permission to change and view and delete this user.</h1>')
        
        return super().change_view(request, object_id, form_url, extra_context)
    

admin.site.register(CustomUser,CustomUserAdmin)

@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display=['user','phone_number']
    



