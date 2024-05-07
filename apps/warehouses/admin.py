from django.contrib import admin
from .models import Warehouse,WarehouseType

@admin.register(WarehouseType)
class WarehouseTypeAdmin(admin.ModelAdmin):
    list_display=['warehouse_type_title']
    
@admin.register(Warehouse)
class WarehouseAdmin(admin.ModelAdmin):
    list_display=['warehouse_type','product','qty','price','register_date']