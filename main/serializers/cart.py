from rest_framework import serializers
from ..models import Cart, CartItem, Product, ProductColor


class CartItemSerializer(serializers.ModelSerializer):
    product_name = serializers.CharField(source='product.name', read_only=True)
    product_slug = serializers.CharField(source='product.slug', read_only=True)
    color_name = serializers.CharField(source='color.name', read_only=True)
    color_hex = serializers.CharField(source='color.hex_code', read_only=True)
    unit_price = serializers.FloatField(read_only=True)
    total_price = serializers.FloatField(read_only=True)
    sqm = serializers.FloatField(read_only=True)
    main_image = serializers.SerializerMethodField()

    class Meta:
        model = CartItem
        fields = [
            'id', 'product', 'product_name', 'product_slug',
            'color', 'color_name', 'color_hex',
            'width_mm', 'height_mm', 'quantity',
            'unit_price', 'total_price', 'sqm',
            'main_image', 'added_at',
        ]
        read_only_fields = ['id', 'unit_price', 'total_price', 'sqm', 'added_at']

    def get_main_image(self, obj):
        img = obj.product.images.filter(is_main=True).first() or obj.product.images.first()
        if img and img.image:
            request = self.context.get('request')
            return request.build_absolute_uri(img.image.url) if request else img.image.url
        return None


class CartSerializer(serializers.ModelSerializer):
    items = CartItemSerializer(many=True, read_only=True)
    total_items = serializers.IntegerField(read_only=True)
    total_amount = serializers.FloatField(read_only=True)

    class Meta:
        model = Cart
        fields = ['id', 'items', 'total_items', 'total_amount', 'updated_at']


class AddToCartSerializer(serializers.Serializer):
    product_id = serializers.IntegerField()
    color_id = serializers.IntegerField(required=False, allow_null=True)
    width_mm = serializers.IntegerField(min_value=100, max_value=10000)
    height_mm = serializers.IntegerField(min_value=100, max_value=10000)
    quantity = serializers.IntegerField(min_value=1, max_value=100, default=1)

    def validate_product_id(self, value):
        try:
            product = Product.objects.get(id=value, is_active=True)
            return value
        except Product.DoesNotExist:
            raise serializers.ValidationError('Mahsulot topilmadi')

    def validate(self, attrs):
        color_id = attrs.get('color_id')
        if color_id:
            try:
                ProductColor.objects.get(id=color_id, product_id=attrs['product_id'], is_available=True)
            except ProductColor.DoesNotExist:
                raise serializers.ValidationError({'color_id': 'Rang topilmadi yoki mavjud emas'})
        return attrs


class UpdateCartItemSerializer(serializers.Serializer):
    quantity = serializers.IntegerField(min_value=1, max_value=100)
    width_mm = serializers.IntegerField(min_value=100, max_value=10000, required=False)
    height_mm = serializers.IntegerField(min_value=100, max_value=10000, required=False)
