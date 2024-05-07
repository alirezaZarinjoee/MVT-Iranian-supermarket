from django.contrib import admin
from django.contrib.admin import SimpleListFilter
from .models import Brand,ProductGroup,Product,Feature,ProductFeature,ProductGallery,FeatureValue
from django.db.models.aggregates import Count
from django_admin_listfilter_dropdown.filters import DropdownFilter
from django.db.models import Q
from admin_decorators import short_description,order_field
# Register your models here.


@admin.register(Brand)
class BrandAdmin(admin.ModelAdmin):
    list_display=('brand_title','slug')
    list_filter=(('brand_title',DropdownFilter),)
    search_fields=('brand_title',)
    ordering=('brand_title',)

#______________________________________________________________________

class GroupFilter(SimpleListFilter):
    title='گروه محصولات'
    parameter_name='group'
    def lookups(self, request, model_admin):
        sub_groups=ProductGroup.objects.filter(~Q(group_parent=None))
        groups=set([item.group_parent for item in sub_groups])
        return [(item.id,item.group_title) for item in groups]
    def queryset(self, request, queryset):
        if self.value()!=None:
            return queryset.filter(Q(group_parent=self.value()))
        return queryset
        


#______________________________________________________________________


def de_active_product_group(modeladmin,request,queryset):
    res=queryset.update(is_active=False)
    message=f'تعداد {res} گروه کالا غیر فعال شد'
    modeladmin.message_user(request,message)
    
def active_product_group(modeladmin,request,queryset):
    res=queryset.update(is_active=True)
    message=f'تعداد {res} گروه کالا فعال شد'
    modeladmin.message_user(request,message)

class ProductGroupInstanceInlineAdmin(admin.TabularInline):
    model=ProductGroup
    extra = 1
    
@admin.register(ProductGroup)
class ProductGroupAdmin(admin.ModelAdmin):
    list_display=('group_title','is_active','group_parent','register_date','update_date','count_sub_goup','count_product_of_groups')
    list_filter=(GroupFilter,)
    search_fields=('group_title',)
    ordering=('group_parent','group_title')
    filter_horizontal = ('features_of_groups',)
    inlines=[ProductGroupInstanceInlineAdmin]
    actions=[de_active_product_group,active_product_group]
    list_editable=['is_active']

    
    def get_queryset(self,*args,**kwargs):
        qs=super(ProductGroupAdmin,self).get_queryset(*args,**kwargs)
        # qs=qs.annotate(sub_group=Count('groups'),)
        qs=qs.annotate(count=Count('products_of_groups'))
        return qs
    
    
    
    @order_field('sub_group')
    def count_sub_goup(self,obj):
        # groups=ProductGroup.objects.all()
        set_list=(len(set([i for i in obj.groups.all()])))
        return set_list
    
    @order_field('count')
    def count_product_of_groups(self,obj):
        return obj.count
    
    count_sub_goup.short_description='تعداد زیر گروه ها'
    de_active_product_group.short_description='غیر فعال کردن گروه های انتخابی'
    active_product_group.short_description='فعال کردن گروه های انتخابی'
    count_product_of_groups.short_description='تعداد کالاهای گروه'
#_________________________________________________________________

class ProductGalleryInline(admin.TabularInline):
    model=ProductGallery
    extra=2


#_________________________________________________________________




class ProductFeatureInlineAdmin(admin.TabularInline):
    model = ProductFeature  
    extra = 1
    
    class Media:
        css={'all':('admin_style.css',)}
        
        js=(
            'https://ajax.googleapis.com/ajax/libs/jquery/3.6.0/jquery.min.js',
            'js/admin_script.js',
        )

    # def formfield_for_foreignkey(self, db_field,request,**kwargs):
    #     if db_field.name=='feature':
    #         kwargs['queryset'] = Feature.product_group.through.objects.filter(productgroup_id=5)
    #     return super().formfield_for_foreignkey(db_field, request, **kwargs)
#__________________________________________________________________


def de_active_product(modeladmin,request,queryset):
    res=queryset.update(is_active=False)
    message=f'تعداد {res} کالا غیر فعال شد'
    modeladmin.message_user(request,message)
    
def active_product(modeladmin,request,queryset):
    res=queryset.update(is_active=True)
    message=f'تعداد {res} کالا فعال شد'
    modeladmin.message_user(request,message)
    
@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display=('product_name','price','is_active','brand','update_date','display_product_groups','slug',)
    list_filter=(('brand__brand_title',DropdownFilter),("product_group__group_title",DropdownFilter,),)
    search_fields=('product_name',)
    ordering=('update_date','product_name')
    actions=[active_product,de_active_product]
    inlines=[ProductFeatureInlineAdmin,ProductGalleryInline]
    list_editable=['is_active']
    de_active_product.short_description='غیر فعال کردن کالا های انتخابی'
    active_product.short_description='فعال کردن کالا های انتخابی'
    

    def display_product_groups(self,obj):
        return '-'.join([group.group_title for group in obj.product_group.all()])
    display_product_groups.short_description='گروه های کالا'
    
    def formfield_for_manytomany(self, db_field,request,**kwargs):
        if db_field.name=='product_group':
            kwargs['queryset']=ProductGroup.objects.filter(~Q(group_parent=None))
        return super().formfield_for_manytomany(db_field, request, **kwargs)
#______________________________________________________________________
class FeatureValueInline(admin.TabularInline):
    model=FeatureValue
    extra=3

#______________________________________________________________________

@admin.register(Feature)
class FeatureAdmin(admin.ModelAdmin):
    list_display=('feature_name','display_groups','display_feature_values')
    list_filter=(('product_group__group_title',DropdownFilter),)
    search_fields=('feature_name',)
    ordering=('feature_name',)
    inlines=[FeatureValueInline]
    
    def display_groups(self,obj):
        return ', '.join([group.group_title for group in obj.product_group.all()])
    
    def display_feature_values(self,obj):
        return ', '.join([feature_value.value_title for feature_value in obj.feature_value.all()])
    
    display_groups.short_description='گروه های داری این ویژگی'
    display_feature_values.short_description='مقادیر ممکن برای این ویژگی'
    
#______________________________________________________________________
