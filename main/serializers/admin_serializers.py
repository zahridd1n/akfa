from rest_framework import serializers
from ..models import Product, ProductImage, ProductColor, Order, CustomUser


class AdminProductCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        exclude = ['created_at', 'updated_at']
        extra_kwargs = {
            'slug': {'required': False, 'allow_blank': True},
            'material': {'required': False, 'allow_blank': True},
            'design_style': {'required': False, 'allow_blank': True},
            'description': {'required': False, 'allow_blank': True},
            'badge': {'required': False, 'allow_blank': True},
            'status': {'required': False},
            'is_active': {'required': False},
            'price_type': {'required': False},
            'profile_thickness': {'required': False, 'allow_blank': True},
            'max_glass': {'required': False, 'allow_blank': True},
            'sound_insulation': {'required': False, 'allow_blank': True},
            'climate_resistance': {'required': False, 'allow_blank': True},
            'delivery_info': {'required': False, 'allow_blank': True},
        }


class AdminOrderStatusSerializer(serializers.Serializer):
    status = serializers.ChoiceField(choices=Order.Status.choices)


class AdminDashboardSerializer(serializers.Serializer):
    total_orders = serializers.IntegerField()
    today_orders = serializers.IntegerField()
    pending_orders = serializers.IntegerField()
    total_products = serializers.IntegerField()
    total_customers = serializers.IntegerField()
    monthly_revenue = serializers.DecimalField(max_digits=20, decimal_places=2)
    order_by_status = serializers.DictField()


class AdminCustomerSerializer(serializers.ModelSerializer):
    orders_count = serializers.IntegerField(read_only=True)
    total_spent = serializers.DecimalField(max_digits=20, decimal_places=2, read_only=True)

    class Meta:
        model = CustomUser
        fields = ['id', 'phone_number', 'full_name', 'is_active', 'created_at', 'orders_count', 'total_spent']
