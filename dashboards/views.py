from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from sales.models import Order
from django.db import models


from products.models import Product
from customers.models import Customer
from employees.models import Employee
from suppliers.models import Supplier
from purchases.models import Purchase

class DashboardSummaryView(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        total_products = Product.objects.count()
        total_customers = Customer.objects.count()
        total_employees = Employee.objects.count()
        total_suppliers = Supplier.objects.count()
        total_purchases = Purchase.objects.count()
        total_purchase_amount = Purchase.objects.aggregate(
            total_amount=models.Sum('total_amount')
        )['total_amount'] or 0

        total_sales = Order.objects.count()
        total_sales_amount = Order.objects.aggregate(
            total=models.Sum('total_amount')
        )['total'] or 0

        return Response({
            "total_products": total_products,
            "total_customers": total_customers,
            "total_employees": total_employees,
            "total_suppliers": total_suppliers,
            "total_purchases": total_purchases,
            "total_purchase_amount": total_purchase_amount,
            "total_sales": total_sales,
            "total_sales_amount": total_sales_amount
        })