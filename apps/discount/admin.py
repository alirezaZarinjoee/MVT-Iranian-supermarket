from django.contrib import admin
from . models import Coupon,DiscountBasket,DiscountBasketDetails

@admin.register(Coupon)
class CouponAdmin(admin.ModelAdmin):
    list_display=('coupon_code','start_date','end_date','discount','is_active',)
    ordering=('is_active',)
    
class DiscountBasketDetailsInline(admin.TabularInline):
    model=DiscountBasketDetails
    extra=3
    
@admin.register(DiscountBasket)
class DiscountBasketAdmin(admin.ModelAdmin):
    list_display=('discount_title','start_date1','end_date1','discount','is_active',)
    ordering=('is_active',)
    inlines=[DiscountBasketDetailsInline]