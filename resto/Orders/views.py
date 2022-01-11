from rest_framework import generics, permissions, filters
from rest_framework.response import Response
from rest_framework.reverse import reverse
from rest_framework.decorators import api_view
from django_filters.rest_framework import DjangoFilterBackend
from .serializers import (TableListSerializer, TableDetailSerializer, 
                          OrderListSerializer, OrderDetailSerializer,
                          OrderItemListSerializer, OrderItemDetailSerializer
                        )
from django.db.models import Sum
from django.conf import settings
from .models import Table, Order, OrderItem

CURRENCY = settings.CURRENCY


@api_view(['GET'])
def ApiHomepage(request, format=None):
    return Response({
        'orders': reverse('order_list', request=request, format=format),
        'order-items': reverse('order_item_list', request=request, format=format),
        'tables': reverse('table_list', request=request, format=format),
        'products': reverse('product_list', request=request, format=format),
        'categories': reverse('category_list', request=request, format=format),
        
    })


@api_view(['GET'])
def ReportOrderApiView(request, format=None):
    table_name = request.GET.get('table', None)
    orders = Order.objects.all()
    orders = orders.filter(table__id=table_name) if table_name else orders
    total_value = orders.aggregate(Sum('value'))['value__sum'] if orders else 0
    total_orders = orders.count() if orders else 0
    average_order = round(total_value/total_orders, 2) if total_orders > 0 else 0
    return Response({
        'count': total_orders,
        'total': f'{total_value} {CURRENCY}',
        'avg': f'{average_order} {CURRENCY}',
    })


class TableListAPIView(generics.ListAPIView):
    serializer_class = TableListSerializer
    permission_classes = [permissions.AllowAny, ]
    queryset = Table.objects.filter(active=True)


class TableDetailAPIView(generics.RetrieveUpdateAPIView):
    serializer_class = TableDetailSerializer
    permission_classes = (permissions.AllowAny,)
    queryset = Table.objects.filter(active=True)


class OrderListAPIView(generics.ListCreateAPIView):
    serializer_class = OrderListSerializer
    permission_classes = (permissions.AllowAny, )
    queryset = Order.objects.all()
    filter_backends = (DjangoFilterBackend, )
    filter_fields = ('table', )
    

class OrderDetailAPIView(generics.RetrieveUpdateAPIView):
    serializer_class = OrderDetailSerializer
    permission_classes = [permissions.AllowAny]
    queryset = Order.objects.all()
    lookup_field = 'id'
    lookup_url_kwarg = 'pk'
    

class OrderItemListAPIView(generics.ListCreateAPIView):
    serializer_class = OrderItemListSerializer
    permission_classes = (permissions.AllowAny, )
    queryset = OrderItem.objects.all()
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, ]
    filter_fields = ['product_related', 'order_related', ]
    search_fields = ['product_related__title', 'order_related__title']


class OrderItemDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = OrderItemDetailSerializer
    permission_classes = (permissions.AllowAny, )
    queryset = OrderItem.objects.all()



class TableListApiAuthView(generics.ListAPIView):
    serializer_class = TableListSerializer
    permission_classes = (permissions.IsAuthenticated,)
    queryset = Table.objects.filter(active=True)