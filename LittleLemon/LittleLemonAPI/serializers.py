from rest_framework import serializers
from .models import Category, MenuItem, Cart, Order, OrderItem

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'slug', 'title']


class MenuItemSerializer(serializers.ModelSerializer):
    category = CategorySerializer()

    class Meta:
        model = MenuItem
        fields = ['id', 'title', 'price', 'featured', 'category']


class CartSerializer(serializers.ModelSerializer):
    menuitem = MenuItemSerializer()

    class Meta:
        model = Cart
        fields = ['id', 'user', 'menuitem', 'quantity', 'unit_price', 'price']


class OrderItemSerializer(serializers.ModelSerializer):
    menuitem = MenuItemSerializer()

    class Meta:
        model = OrderItem
        fields = ['id', 'order', 'menuitem', 'quantity', 'unit_price', 'price']


class OrderSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField()
    delivery_crew = serializers.StringRelatedField()
    order_items = OrderItemSerializer(many=True)

    class Meta:
        model = Order
        fields = ['id', 'user', 'delivery_crew', 'status', 'total', 'date', 'order_items']
