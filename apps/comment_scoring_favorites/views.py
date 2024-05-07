from django.shortcuts import render,redirect,get_object_or_404
from . forms import CommentForm
from . models import Comment,scoring,Favorite
from apps.product.models import Product
from django.contrib import messages
from django.views import View
from django.http import HttpResponse,JsonResponse
from django.db.models import Q
from apps.product.models import Product


# Create your views here.
class CommentView(View):
    def get(self,request,*args,**kwargs):
        productId=request.GET.get('productId')
        commentId=request.GET.get('commentId')
        slug=kwargs['slug']
        initial_dict={
            'product_id':productId,
            'comment_id':commentId
        }
        
        form=CommentForm(initial=initial_dict)
        return render(request,'csf/create_comment.html',{'form':form,'slug':slug})
    
    def post(self,request,*args,**kwargs):
        slug=kwargs.get('slug')
        print('************')
        print(slug)
        print('************')
        product=get_object_or_404(Product,slug=slug)
        
        form=CommentForm(request.POST)
        
        if form.is_valid():
            cd=form.cleaned_data
            parent=None
            
            if (cd['comment_id']):
                parentId=cd['comment_id']
                parent=Comment.objects.get(id=parentId)
            
            Comment.objects.create(
                product=product,
                commenting_user=request.user,
                comment_text=cd['comment_text'],
                comment_parent=parent
            )
            messages.success(request,'نظر شما با موفقیت ثبت شد')
            return redirect('product:product_details',product.slug)
        
        messages.error(request,'نظر شما با موفقیت ثبت شد','danger')
        return redirect('product:product_details',product.slug)

        
        
def add_score(request):
    productId = request.GET.get("productId")
    score = request.GET.get("score")
    product = Product.objects.get(id=productId)
    
    scoring.objects.create(
        product = product,
        scoring_user = request.user,
        score = score, 
    )
    
    response_data = {
        'success': True,
        'message': 'امتیاز شما ثبت شد'
    }

    messages.success(request,"امتیاز شما ثبت شد","success")
    return JsonResponse(response_data)


def add_to_favorite(request):
    productId=request.GET.get('productId')
    product=Product.objects.get(id=productId)
    flag=Favorite.objects.filter(Q(favorite_user_id=request.user.id) & Q(product_id=productId)).exists()
    
    if (not flag):
        Favorite.objects.create(product=product,favorite_user=request.user)
        return HttpResponse('این کالا به لیست علاقه مندی ها اضافه شد')
    return HttpResponse('این کالا قبلا در لیست شما قرار گرفته')


class UserFavoriteView(View):
    def get(self,request,*args,**kwargs):
        user_favorite=Favorite.objects.filter(Q(favorite_user_id=request.user.id)).order_by('-register_date')
        return render(request,'csf/user_favorite.html',{'user_favorite':user_favorite})
    
def statuse_favorite_list(request):
    user_favorite=Favorite.objects.filter(Q(favorite_user_id=request.user.id))
    len_user_favorite=len(user_favorite)
    return HttpResponse(len_user_favorite)
    