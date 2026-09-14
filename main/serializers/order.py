from rest_framework import serializers
from ..models import Order, OrderItem, Address


class OrderItemSerializer(serializers.ModelSerializer):
    sqm = serializers.FloatField(read_only=True)
    main_image = serializers.SerializerMethodField()

    class Meta:
        model = OrderItem
        fields = [
            'id', 'product', 'product_name',
            'color_name', 'color_hex',
            'width_mm', 'height_mm', 'sqm',
            'quantity', 'unit_price', 'total_price',
            'main_image',
        ]
        read_only_fields = fields

    def get_main_image(self, obj):
        if not obj.product:
            return None
        img = obj.product.images.filter(is_main=True).first() or obj.product.images.first()
        if img and img.image:
            request = self.context.get('request')
            return request.build_absolute_uri(img.image.url) if request else img.image.url
        return None


class OrderAddressSerializer(serializers.ModelSerializer):
    region_display = serializers.CharField(source='get_region_display', read_only=True)

    class Meta:
        model = Address
        fields = ['id', 'region', 'region_display', 'city', 'street', 'house_number', 'full_address']


class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True, read_only=True)
    delivery_address = OrderAddressSerializer(read_only=True)
    status_display = serializers.CharField(source='get_status_display', read_only=True)
    customer_name = serializers.CharField(source='user.full_name', read_only=True)
    customer_phone = serializers.CharField(source='user.phone_number', read_only=True)
    user_full_name = serializers.CharField(source='user.full_name', read_only=True)
    user_phone = serializers.CharField(source='user.phone_number', read_only=True)

    class Meta:
        model = Order
        fields = [
            'id', 'order_number',
            'customer_name', 'customer_phone',
            'user_full_name', 'user_phone',
            'delivery_address',
            'status', 'status_display',
            'subtotal', 'delivery_fee', 'total_amount',
            'notes', 'items',
            'created_at', 'updated_at',
        ]
        read_only_fields = fields


class CreateOrderSerializer(serializers.Serializer):
    address_id = serializers.IntegerField()
    notes = serializers.CharField(required=False, allow_blank=True, default='')
    delivery_fee = serializers.DecimalField(max_digits=12, decimal_places=2, default=0)

    def validate_address_id(self, value):
        user = self.context['request'].user
        try:
            Address.objects.get(id=value, user=user)
        except Address.DoesNotExist:
            raise serializers.ValidationError('Manzil topilmadi')
        return value
