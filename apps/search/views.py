from django.shortcuts import render
from django.views import View
from django.db.models import Q
from apps.product.models import Product

class SearchResultsView(View):
    def get(self,request,*args,**kwargs):
        query=self.request.GET.get('q')
        products=Product.objects.filter(
            Q(product_name__icontains=query)
        )
        context={
            'products':products,
        }
        return render(request,'search/search_results.html',context)
    