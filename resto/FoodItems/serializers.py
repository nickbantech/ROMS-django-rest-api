from rest_framework import serializers
from FoodItems.models import Product, Category


class ProductListSerializer(serializers.ModelSerializer):
    url = serializers.HyperlinkedIdentityField(view_name='product_detail', read_only=True)

    class Meta:
        model = Product
        fields = ['id', 'title', 'value', 'category', 'active', 'tag_category', 'tag_value', 'url']


class ProductDetailSerializer(serializers.ModelSerializer):

    class Meta:
        model = Product
        fields = ['id', 'title', 'value', 'category', 'tag_category', 'tag_value']


class CategoryListSerializer(serializers.ModelSerializer):

     class Meta:
         model = Category
         fields = ['id', 'title']