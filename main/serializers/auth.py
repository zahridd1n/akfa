import re
from django.contrib.auth import authenticate
from rest_framework import serializers
from rest_framework_simplejwt.tokens import RefreshToken
from ..models import CustomUser


def normalize_phone_number(value):
    if not value:
        return ""
    cleaned = re.sub(r'[\s\-\(\)\.]', '', str(value).strip())
    if cleaned.startswith('998') and not cleaned.startswith('+'):
        cleaned = '+' + cleaned
    elif len(cleaned) == 9 and not cleaned.startswith('+'):
        cleaned = '+998' + cleaned
    return cleaned


def validate_phone_number(value):
    value = normalize_phone_number(value)
    if not re.match(r'^\+998[0-9]{9}$', value):
        raise serializers.ValidationError(
            "Telefon raqam +998XXXXXXXXX formatida bo'lishi kerak"
        )
    return value


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, min_length=6)
    password_confirm = serializers.CharField(write_only=True, required=False, allow_blank=True, default="")

    class Meta:
        model = CustomUser
        fields = ["phone_number", "full_name", "password", "password_confirm"]

    def validate_phone_number(self, value):
        value = validate_phone_number(value)
        if CustomUser.objects.filter(phone_number=value).exists():
            raise serializers.ValidationError("Ushbu telefon raqam allaqachon ro'yxatdan o'tgan")
        return value

    def validate(self, attrs):
        password_confirm = attrs.pop("password_confirm", None)
        if password_confirm and attrs.get("password") != password_confirm:
            raise serializers.ValidationError({"password_confirm": "Parollar mos kelmadi"})
        return attrs

    def create(self, validated_data):
        return CustomUser.objects.create_user(**validated_data)


class LoginSerializer(serializers.Serializer):
    phone_number = serializers.CharField()
    password = serializers.CharField(write_only=True)

    def validate_phone_number(self, value):
        return validate_phone_number(value)

    def validate(self, attrs):
        phone = attrs["phone_number"]
        password = attrs["password"]
        user = authenticate(
            username=phone,
            password=password,
        )
        if not user:
            raise serializers.ValidationError("Telefon raqam yoki parol noto'g'ri")
        if not user.is_active:
            raise serializers.ValidationError("Hisobingiz faol emas")
        attrs["user"] = user
        return attrs


class TokenResponseSerializer(serializers.Serializer):
    access = serializers.CharField()
    refresh = serializers.CharField()
    user = serializers.SerializerMethodField()

    def get_user(self, obj):
        user = obj["user"]
        return {
            "id": user.id,
            "phone_number": user.phone_number,
            "full_name": user.full_name,
            "role": user.role,
        }


class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ["id", "phone_number", "full_name", "role", "created_at"]
        read_only_fields = ["id", "phone_number", "role", "created_at"]


class ChangePasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField(write_only=True)
    new_password = serializers.CharField(write_only=True, min_length=6)
    new_password_confirm = serializers.CharField(write_only=True)

    def validate(self, attrs):
        if attrs["new_password"] != attrs.pop("new_password_confirm"):
            raise serializers.ValidationError({"new_password_confirm": "Parollar mos kelmadi"})
        return attrs
