from django.urls import path
from . import views

app_name='main'
urlpatterns = [
    path('',views.index,name='main'),
    # path('test_view/',views.test_view,name='test_view'),
    path('slider_view/',views.SliderView.as_view(),name='slider_view'),
]
