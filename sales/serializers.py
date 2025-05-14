from rest_framework import serializers
from .models import Order, OrderDetail

class OrderDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderDetail
        fields = ['product', 'quantity', 'total_price']

class OrderSerializer(serializers.ModelSerializer):
    items = OrderDetailSerializer(many=True)

    class Meta:
        model = Order
        fields = [
            'id', 'customer', 'employee',
            'total_amount', 'total_paid', 'total_remain',
            'created_at', 'items'
        ]
        read_only_fields = ['id', 'created_at', 'total_amount', 'total_remain']

    def create(self, validated_data):
        items_data = validated_data.pop('items')
        total_paid = validated_data.pop('total_paid', 0)

        total_amount = sum(item['total_price'] for item in items_data)
        total_remain = total_amount - total_paid

        order = Order.objects.create(
            total_amount=total_amount,
            total_paid=total_paid,
            total_remain=total_remain,
            **validated_data
        )

        for item_data in items_data:
            OrderDetail.objects.create(order=order, **item_data)

        return order