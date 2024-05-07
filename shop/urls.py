"""
URL configuration for shop project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path,include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('',include('apps.main.urls',namespace='main')),
    path('account/',include('apps.account.urls',namespace='account')),
    path('product/',include('apps.product.urls',namespace='product')),
    path('orders/',include('apps.orders.urls',namespace='orders')),
    path('warehouses/',include('apps.warehouses.urls',namespace='warehouses')),
    path('discount/',include('apps.discount.urls',namespace='discount')),
    path('csf/',include('apps.comment_scoring_favorites.urls',namespace='csf')),
    path('search/',include('apps.search.urls',namespace='search')),
    path('ckeditor/', include('ckeditor_uploader.urls')),
]+static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)