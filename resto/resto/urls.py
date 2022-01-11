"""resto URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
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
from django.urls import path

from Orders.views import (TableListAPIView, TableDetailAPIView,
                              OrderListAPIView, OrderDetailAPIView,  
                              OrderItemListAPIView, OrderItemDetailAPIView,
                              ApiHomepage
                            )   

from FoodItems.views import ProductListAPIView, ProductDetailAPIView, CategoryListApiView

urlpatterns = [
    path('admin/', admin.site.urls),

    path('api/', ApiHomepage),
    path('api/table-list/', TableListAPIView.as_view(), name='table_list'),
    path('api/table-detail/<int:pk>/', TableDetailAPIView.as_view(), name='table_detail'),
    path('api/order-list/', OrderListAPIView.as_view(), name='order_list'),
    path('api/order-detail/<int:pk>/', OrderDetailAPIView.as_view(), name='order_detail'),
    path('api/order-item-list', OrderItemListAPIView.as_view(), name='order_item_list'),
    path('api/order-item-detail/<int:pk>/', OrderItemDetailAPIView.as_view(), name='order_item_detail'),

    path('api/product-list/', ProductListAPIView.as_view(), name='product_list'),
    path('api/product-detail/<int:pk>/', ProductDetailAPIView.as_view(), name='product_detail'),
    path('api/category-list/', CategoryListApiView.as_view(), name='category_list'),
    
    

]