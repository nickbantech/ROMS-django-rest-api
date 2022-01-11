from rest_framework import serializers
from .models import Table, Order, OrderItem


class TableListSerializer(serializers.ModelSerializer):
    url = serializers.HyperlinkedIdentityField(view_name='table_detail', read_only=True)

    class Meta:
        model = Table
        fields = ['id', 'title', 'is_free', 'tag_value', 'url', 'active_order_id']
    

class TableDetailSerializer(serializers.ModelSerializer):

    class Meta:
        model = Table
        fields = ['id', 'title', 'is_free', 'value', 'tag_value']


class OrderListSerializer(serializers.ModelSerializer):
    url = serializers.HyperlinkedIdentityField(view_name='order_detail', read_only=True)

    class Meta:
        model = Order
        fields = ['id', 'timestamp', 'tag_timestamp', 'title', 'tag_value', 'table', 'tag_table', 'active', 'tag_active', 'url']


class OrderDetailSerializer(serializers.ModelSerializer):

    class Meta:
        model = Order
        fields = ['id', 'title' , 'tag_value', 'table', 'tag_table', 'active']


class OrderItemListSerializer(serializers.ModelSerializer):
    url = serializers.HyperlinkedIdentityField(view_name='order_item_detail', read_only=True)

    class Meta:
        model = OrderItem
        fields = ['id', 'product_related', 'order_related', 
                  'value', 'qty', 'tag_total_value', 'tag_value',
                  'tag_product_related', 'tag_order_related',
                  'url'
                  ]


class OrderItemDetailSerializer(serializers.ModelSerializer):

    class Meta:
        model = OrderItem
        fields = ['id', 'product_related', 'order_related', 
                  'value', 'qty', 'tag_total_value', 'tag_value',
                  'tag_product_related', 'tag_order_related',
                  ]


