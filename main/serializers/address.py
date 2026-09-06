from rest_framework import serializers
from ..models import Address


class AddressSerializer(serializers.ModelSerializer):
    region_display = serializers.CharField(source='get_region_display', read_only=True)

    class Meta:
        model = Address
        fields = [
            'id', 'region', 'region_display',
            'city', 'street', 'house_number', 'apartment',
            'full_address', 'is_default', 'created_at',
        ]
        read_only_fields = ['id', 'region_display', 'created_at']

    def create(self, validated_data):
        validated_data['user'] = self.context['request'].user
        return super().create(validated_data)
