from django.contrib import admin
from .models import Table, Order, OrderItem


@admin.register(Table)
class TableAdmin(admin.ModelAdmin):
    list_display = ['title', 'is_free', 'active', 'tag_value']
    list_filter = ['is_free', 'active']


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['table', 'tag_value', 'active']
    list_filter = ['active', 'table']
    search_fields = ['table__title', 'title']


@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = ['product_related', 'order_related', 'qty', 'tag_value', 'tag_total_value']
    list_filter = ['order_related__table']
    search_fields = ['product_related__title', 'order_related__title']
