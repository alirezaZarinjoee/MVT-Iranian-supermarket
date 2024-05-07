from django.contrib import admin
from . models import Order,OrderDetails,PaymentType,OrderState

class OrderDetailsInline(admin.TabularInline):
    model=OrderDetails
    
@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    search_fields=('ref_id',)
    list_display=['customer','register_date','is_finaly','ref_id','discount']
    inlines=[OrderDetailsInline]
    

@admin.register(PaymentType)
class PaymentTypeAdmin(admin.ModelAdmin):
    list_display=['payment_title']
    
@admin.register(OrderState)
class OrderStateAdmin(admin.ModelAdmin):
    list_display=['id','order_state_title']
    
