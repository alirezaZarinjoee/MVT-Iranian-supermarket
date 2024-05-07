from django.shortcuts import render
from django.conf import settings
from django.views import View
from .models import Slider
from django.db.models import Q
# Create your views here.
def media_admin(request):
    return {'media_url':settings.MEDIA_URL}

def index(request):
    return render(request,'main/index.html')

# def test_view(request):
#     return render(request,'main/test.html',{'ali':'ali'})

class SliderView(View):
    def get(self,request):
        sliders=Slider.objects.filter(Q(is_active=True))
        return render(request,'main/sliders.html',{'sliders':sliders})
    