from django.shortcuts import render,redirect,get_object_or_404
from django.views import View
from .shop_cart import *
from apps.product.models import Product
from django.http import HttpResponse
from django.contrib.auth.mixins import LoginRequiredMixin
from apps.account.models import Customer,CustomUser
from .models import Order,OrderDetails,PaymentType,OrderState
from . forms import OrderForm
from apps.discount.forms import CouponForm
from apps.discount.models import Coupon
from django.db.models import Q
from datetime import datetime
from django.contrib import messages
from django.core.exceptions import ObjectDoesNotExist
import utils
import random
from apps.warehouses.models import Warehouse,WarehouseType


class ShopCartView(View):
    def get(self,request):
        shop_cart=ShopCart(request)
        return render(request,'orders/shop_cart.html',{'shop_cart':shop_cart})
    
        
def add_to_shop_cart(request):
    product_id=request.GET.get('product_id')
    qty=request.GET.get('qty')
    shop_cart=ShopCart(request)
    product=get_object_or_404(Product,id=product_id)
    shop_cart.add_to_shop_cart(product,qty)
    return HttpResponse('کالای مورد نظر شما به سبد خرید اضافه شد')


def show_shop_cart(request):
    shop_cart=ShopCart(request)
    total_price=shop_cart.calc_total_price()
    order_final_price,delivery,tax=utils.price_by_delivery_tax(total_price)
    
    context={
        'shop_cart':shop_cart,
        'shop_cart_count':shop_cart.count,
        'total_price':total_price,
        'delivery':delivery,
        'tax':tax,
        'order_final_price':order_final_price
      
    }
    return render(request,'orders/show_shop_cart.html',context)

def delete_from_shop_cart(request):
    product_id=request.GET.get('product_id')
    product=get_object_or_404(Product,id=product_id)
    shop_cart=ShopCart(request)
    shop_cart.delete_from_shop_cart(product)
    return redirect('orders:show_shop_cart')

    
def update_shop_cart(request):
    product_id_list=request.GET.getlist('product_id_list[]')
    qty_list=request.GET.getlist('qty_list[]')
    shop_cart=ShopCart(request)
    shop_cart.update(product_id_list,qty_list)
    return redirect('orders:show_shop_cart')

def status_of_shop_cart(request):
    shop_cart=ShopCart(request)
    return HttpResponse(shop_cart.count)


class CreateOrderView(LoginRequiredMixin,View):
    def get(self,request):
        try:
            customer=Customer.objects.get(user=request.user)
        except:
            customer=Customer.objects.create(user=request.user)
        order=Order.objects.create(customer=customer,payment_type=get_object_or_404(PaymentType,id=2))
        shop_cart=ShopCart(request)
        for item in shop_cart:
            OrderDetails.objects.create(
                order=order,
                product=item['product'],
                price=item['price'],
                qty=item['qty']
                )
        return redirect('orders:checkout_order',order.id)
    
            
class CheckoutOrderView(LoginRequiredMixin,View):
    def get(self,request,order_id):

        try:
            
            user=request.user
            customer=get_object_or_404(Customer,user=user)
            shop_cart=ShopCart(request)
            customer_order_ids=customer.orders.all()
            
            list_customer_order_ids=[]
            
            for order1 in customer_order_ids:
                list_customer_order_ids.append(order1.id)
            if order_id not in list_customer_order_ids:
                return redirect('main:main')

            order=get_object_or_404(Order,id=order_id)
            

            total_price=shop_cart.calc_total_price()
            order_final_price,delivery,tax=utils.price_by_delivery_tax(total_price)
            if order.discount>0:
                order_final_price=order_final_price-(order_final_price*order.discount/100)


            data={
                'name':user.name,
                'family':user.family,
                'email':user.email,
                'phone_number':customer.phone_number,
                'address':customer.address,
                # 'description':order.description
            }

            form=OrderForm(data)
            form_coupon=CouponForm()

            context={
                'shop_cart':shop_cart,
                'shop_cart_count':shop_cart.count,
                'total_price':total_price,
                'delivery':delivery,
                'tax':tax,
                'order_final_price':order_final_price,
                'form':form,
                'form_coupon':form_coupon,
                'order':order
            }
        
            return render(request,'orders/checkout.html',context)
        except:
            return redirect('main:main')
    
    def post(self,request,order_id):
        form=OrderForm(request.POST)
        if form.is_valid():
            cd=form.cleaned_data
            try:
                order=Order.objects.get(id=order_id)
                order.descrition=cd['description']
                order.payment_type=PaymentType.objects.get(id=cd['payment_type'])
                order.is_finaly=True
                # order.ref_id=get_random_string(10).lower()
                not_unique = True
                while not_unique:
                    unique_ref = random.randint(999999999, 999999999999999999999999999999)
                    if not Order.objects.filter(ref_id=unique_ref):
                        not_unique = False
                ref_id=str(unique_ref)
                order.ref_id=ref_id
                order.order_state=OrderState.objects.get(id=1)
                
                order.save()
                
                user=request.user
                user.name=cd['name']
                user.family=cd['family']
                user.email=cd['email']
                user.save()
                
                customer=Customer.objects.get(user=user)
                customer.phone_number=cd['phone_number']
                customer.address=cd['address']
                customer.save()
                
                for item in order.orders_details1.all():
                    Warehouse.objects.create(
                        warehouse_type=WarehouseType.objects.get(id=2),
                        user_register=request.user,
                        product=item.product,
                        qty=item.qty,
                        price=item.price
                    )
                    
                
                messages.success(request,f'اطلاعات با موفقیت ثبت شد کد پیگیری شما {ref_id}')
                return redirect('orders:final',order_id)

            except ObjectDoesNotExist:
                messages.error(request,'فاکتوری با این مشخصات یافت نشد','danger')
                return redirect('orders:checkout_order',order_id)
        return redirect('orders:checkout_order',order_id)
        
    
    
class ApplayCoupon(View):
    def post(self,request,*args,**kwargs):
        order_id=kwargs['order_id']
        coupon_form=CouponForm(request.POST)
        if coupon_form.is_valid():
            cd=coupon_form.cleaned_data
            coupon_code=cd['coupon_code']
            
        coupon=Coupon.objects.filter(
            Q(coupon_code=coupon_code) &
            Q(is_active=True) &
            Q(start_date__lte=datetime.now())&
            Q(end_date__gte=datetime.now())
        )
        
        discount=0
        try:
            order=Order.objects.get(id=order_id)
            if coupon:
                discount=coupon[0].discount
                order.discount=discount
                order.order_state_id=OrderState.objects.get(id=1)
                order.save()
                messages.success(request,'کد تخفیف با موفقیت اعمال شد')
                return redirect('orders:checkout_order',order_id)
            else:
                order.discount=discount
                order.save()
                messages.error(request,'کد وارد شده معتبر نمی باشد','danger')
        except ObjectDoesNotExist:
            messages.error(request,'ان سفارش موجود نمی باشد','danger')
            
        return redirect('orders:checkout_order',order_id)
    
    
    
    
class Final(View):
    def get(self,request,order_id):
        
        order=Order.objects.get(id=order_id)
        ref_id=order.ref_id
        
        customer_id=order.customer
        customer=Customer.objects.get(user_id=customer_id)
    
        user_id=customer.user_id

        my_user=CustomUser.objects.get(id=user_id)
        user_name=my_user.name
        user_family=my_user.family
        
        context={
            'ref_id':ref_id,
            'user_name':user_name,
            'user_family':user_family,
        }

        return render(request,'orders/final.html',context)
        
        