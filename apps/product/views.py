from django.shortcuts import render,get_object_or_404,redirect
from . models import Product,ProductGroup,FeatureValue,Brand
from django.db.models import Q,Count,Min,Max
from django.views import View
from django.http.response import JsonResponse
from . filters import *
from django.core.paginator import Paginator
from . compare import CompareProduct
from django.http import HttpResponse


#واکشی گروه ها
def get_root_group():
    return ProductGroup.objects.filter(Q(is_active=True) & Q(group_parent=None))
    
#---------------------------------------------------------------------------------------------------
#ارزان ترین محصولات
def get_cheapest_products(request,*args,**kwargs):
    products=Product.objects.filter(is_active=True).order_by('price')[:5]
    product_groups=get_root_group()
    context={
        'products':products,
        'product_groups':product_groups
    }
    return render(request,'product/cheapest_products.html',context)

#-----------------------------------------------------------------------------------------------------
#جدید ترین محصولات
def get_last_products(request,*args,**kwargs):
    products=Product.objects.filter(is_active=True).order_by('-published_date')[:5]
    product_groups=get_root_group()

    context={
        'products':products,
        'product_groups':product_groups
        
    }
    return render(request,'product/last_product.html',context)

#------------------------------------------------------------------------------------------------------
#دسته های محبوب
def popular_product_groups(request,*args,**kwargs):
    products_group=ProductGroup.objects.filter(Q(is_active=True)).annotate(count=Count('products_of_groups')).order_by('-count','group_title')[:6]#در اینجا هم بر اساس تعداد کالا ها و نام گروه مرتب سازی کردیم
    context={
        'products_group':products_group,
    }
    return render(request,'product/popular_product_groups.html',context)

#-------------------------------------------------------------------------------------------------------
#جزییات محصول
class ProductDetailView(View):
    def get(self,request,slug):
        product=get_object_or_404(Product,slug=slug)
        product_comments=product.comments_product.filter(Q(is_active=True))
        len_product=len(product_comments)
        if product.is_active:
            return render(request,'product/product_detail.html',{'product':product,'len_product':len_product})
        
#-------------------------------------------------------------------------------------------------------
#محصولات مرتبط
def get_related_products(request,slug):
    current_product=get_object_or_404(Product,slug=slug)
    related_products=[]
    for group in current_product.product_group.all():
        related_products.extend(Product.objects.filter(Q(is_active=True) & Q(product_group=group) & ~Q(id=current_product.id)))
    
    set_list_related_products=set(related_products)#این دو خط کد برای اینه که ما وقتی محصولات مرتبط را بر اساس گروه میاوردیم ، یک کالا درون دوتا گروه اگر بود ، برای ما دوبار ان کالا را در محصولات مشابه میاورد ولی با این کار  محصولات تکراری حذف میشن
    list_related_products=list(set_list_related_products)
        
    return render(request,'product/related_products.html',{'related_products':list_related_products})

#-------------------------------------------------------------------------------------------------------
#لیست کلیه گروه ها
class ProductGroupsView(View):
    def get(self,request):
        products_group=ProductGroup.objects.filter(Q(is_active=True) & ~Q(group_parent=None))\
                                                    .annotate(count=Count('products_of_groups'))\
                                                    .order_by('-count','group_title')
        
        return render(request,'product/product_group.html',{'products_group':products_group})
#-------------------------------------------------------------------------------------------------------
#tow dropdown in aminpanel
def get_filter_value_for_feature(request):
    if request.method=='GET':
        feature_id=request.GET['feature_id']
        feature_values=FeatureValue.objects.filter(feature_id=feature_id)
        res={fv.value_title:fv.id for fv in feature_values}
        print(100*'*')
        print(res)
        print(100*'*')
        return JsonResponse(data=res)

#-------------------------------------------------------------------------------------------------------
#واکشی گروه ها برای فیلتر
def get_product_groups(request):
    product_groups=ProductGroup.objects.annotate(count=Count('products_of_groups'))\
                                            .filter(Q(is_active=True) & ~Q(count=0))\
                                            .order_by('-count')
    return render(request,'product/product_groups.html',{'product_groups':product_groups})

        

#-------------------------------------------------------------------------------------------------------
#لیست محصولات هر گروه
class ProduuctByGroupView(View):
    def get(self,request,*args,**kwargs):
        slug=kwargs['slug']
        current_group=get_object_or_404(ProductGroup,slug=slug)
        list_of_product=Product.objects.filter(Q(is_active=True) & Q(product_group=current_group))
        copy_list_of_product=list_of_product
        
        res_aggre=list_of_product.aggregate(min=Min('price'),max=Max('price'))
        
        #price filter
        filter=ProduuctFilter(request.GET,queryset=list_of_product)
        list_of_product=filter.qs
        
        #brand filter
        brands_filter=request.GET.getlist('brand')
        if brands_filter:
            list_of_product=list_of_product.filter(brand__id__in=brands_filter)
        
        #feature filter
        features_filter=request.GET.getlist('faeture')
        if features_filter:
            list_of_product=list_of_product.filter(product_features__filter_value__id__in=features_filter).distinct()
            
        #sort type
        sort_type=request.GET.get('sort_type')
        if not sort_type:
            sort_type='0'
        if sort_type=='1':
            list_of_product=list_of_product.order_by('price')
        elif sort_type=='2':
            list_of_product=list_of_product.order_by('-price')
            
        
        
        group_slug=slug
        product_pre_page=10
        paginator=Paginator(list_of_product,product_pre_page)
        page_number=request.GET.get('page')
        page_obj=paginator.get_page(page_number)
        product_count=list_of_product.count();
        
        context={
            
            'list_of_product':list_of_product,
            'current_group':current_group,
            'group_slug':group_slug,
            'res_aggre':res_aggre,
            'page_obj':page_obj,
            'product_count':product_count,
            'filter':filter,
            'sort_type':sort_type
            
        }
        
        return render(request,'product/product_list.html',context)

#-------------------------------------------------------------------------------------------------------
#لیست برند ها برای فیلتر
def get_brands(request,*args,**kwargs):
    product_group=get_object_or_404(ProductGroup,slug=kwargs['slug'])
    brand_list_id=product_group.products_of_groups.filter(is_active=True).values('brand_id')
    brands=Brand.objects.filter(pk__in=brand_list_id).annotate(count=Count('brands')).filter(~Q(count=0)).order_by('-count')
    
    return render(request,'product/brands.html',{'brands':brands})

#-------------------------------------------------------------------------------------------------------
#لیست ویژگی های یک گرروه برای فیلتر کردن
def get_features_for_filter(request,*args,**kwargs):
    product_group=get_object_or_404(ProductGroup,slug=kwargs['slug'])
    feature_list=product_group.features_of_groups.all()
    # print(feature_list)
    feature_dict={}
    for feature in feature_list:
        feature_dict[feature]=feature.feature_value.all()
    # print(feature_dict)
    return render(request,'product/features_filter.html',{'feature_dict':feature_dict})

        
#---------------------------------------------------------------------------------------------------------
class ShowCompareListView(View):
    def get(self,request,*args,**kwargs):
        compare_list=CompareProduct(request)
        context={
            'compare_list':compare_list
        }
        return render(request,'product/compare_list.html',context)

#---------------------------------------------------------------------------------------------------------
def compare_table(request):
    compareList=CompareProduct(request)
    products=[]
    for productId in compareList.compare_product:
        product=Product.objects.get(id=productId)
        products.append(product)
    
    features=[]
    for product in products:
        for item in product.product_features.all():
            if item.feature not in features:
                features.append(item.feature)
                
    context={
        'products':products,
        'features':features
    }
    return render(request,'product/compare_table.html',context)

#---------------------------------------------------------------------------

def add_to_compare_list(request):
    productId=request.GET.get('productId')
    productGroupId=request.GET.get('productGroupId')
    productGroupId=int(productGroupId)
    compare_list=CompareProduct(request)
    products_group=[]
    for product1 in compare_list.compare_product:
        product=Product.objects.get(id=product1)
        for group in product.product_group.all():
            print(type(group.id))
            products_group.append(group.id)
            
    if compare_list.count==0:
        compare_list.add_to_compare_product(productId)
        return HttpResponse('کالا به لیست اضافه شد')
    else:
        if productGroupId not in products_group:
            return HttpResponse('این کالا با کالایی که درون لیست مقایسه اضافه کردید هم گروه نیست')
        else:
            compare_list.add_to_compare_product(productId)
            return HttpResponse('کالا به لیست اضافه شد')
#---------------------------------------------------------------------------
def status_of_compare_list(request):
    compareList=CompareProduct(request)
    return HttpResponse(compareList.count)

#---------------------------------------------------------------------------
def delete_from_compare_list(request):
    productId=request.GET.get('productId')
    compareList=CompareProduct(request)
    compareList.delete_from_compare_product(productId)
    return redirect('product:compare_table')


# from django.db.models import Count
# from apps.product.models import Product

def get_best_selling(request):
    top_products = Product.objects.annotate(
        num_orders=Count('orders_details2')
    ).order_by('-num_orders')[:5]

    return render(request,'product/best_selling.html',{'top_products':top_products})
