from rest_framework import serializers
from .models import Purchase, PurchaseDetail

class PurchaseDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = PurchaseDetail
        fields = ['product', 'quantity', 'total_price']

class PurchaseSerializer(serializers.ModelSerializer):
    items = PurchaseDetailSerializer(many=True)

    class Meta:
        model = Purchase
        fields = [
            'id', 'supplier', 'employee', 'total_amount',
            'total_paid', 'total_remain', 'created_at', 'items'
        ]
        read_only_fields = ['id', 'created_at', 'total_amount', 'total_remain']

    def create(self, validated_data):
        items_data = validated_data.pop('items')
        total_paid = validated_data.pop('total_paid', 0)

        total_amount = sum(item['total_price'] for item in items_data)
        total_remain = total_amount - total_paid

        purchase = Purchase.objects.create(
            total_amount=total_amount,
            total_paid=total_paid,
            total_remain=total_remain,
            **validated_data
        )

        for item_data in items_data:
            PurchaseDetail.objects.create(purchase=purchase, **item_data)

        return purchase
