from django.contrib.auth import authenticate
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from drf_spectacular.utils import extend_schema, OpenApiExample, OpenApiResponse, inline_serializer
from drf_spectacular.types import OpenApiTypes
from rest_framework import serializers as drf_serializers
from ..serializers.auth import (
    RegisterSerializer,
    LoginSerializer,
    ProfileSerializer,
    ChangePasswordSerializer,
)


@extend_schema(
    tags=["🔐 Autentifikatsiya"],
    summary="Ro'yxatdan o'tish",
    description="""
Yangi foydalanuvchi ro'yxatdan o'tkazish.

**Kerakli maydonlar:**
- phone_number — Telefon raqam (+998XXXXXXXXX formatida)
- ull_name — To'liq ism
- password — Parol (kamida 6 ta belgi)
- password_confirm — Parol tasdiqlash

**Muvaffaqiyatli javob:** Token va foydalanuvchi ma'lumotlari qaytariladi.
Token keyingi barcha so'rovlarda Authorization: Token <token> sifatida yuborilishi kerak.
    """,
    request=RegisterSerializer,
    responses={
        201: OpenApiResponse(description="Muvaffaqiyatli ro'yxatdan o'tish — token qaytariladi"),
        400: OpenApiResponse(description="Xato ma'lumot — validatsiya xatosi"),
    },
)
@api_view(["POST"])
@permission_classes([AllowAny])
def register_view(request):
    """Yangi foydalanuvchi ro'yxatdan o'tkazish"""
    serializer = RegisterSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    user = serializer.save()

    token, _ = Token.objects.get_or_create(user=user)
    return Response({
        "message": "Muvaffaqiyatli ro'yxatdan o'tdingiz",
        "token": token.key,
        "user": {
            "id": user.id,
            "phone_number": user.phone_number,
            "full_name": user.full_name,
            "role": user.role,
        },
    }, status=status.HTTP_201_CREATED)


@extend_schema(
    tags=["🔐 Autentifikatsiya"],
    summary="Tizimga kirish",
    description="""
Telefon raqam va parol orqali tizimga kirish.

**Kerakli maydonlar:**
- phone_number — Telefon raqam (+998XXXXXXXXX)
- password — Parol

**Muvaffaqiyatli javob:** Token qaytariladi.
Bu tokenni keyingi so'rovlarda Authorization: Token <token> sifatida yuboring.
    """,
    request=LoginSerializer,
    responses={
        200: OpenApiResponse(description="Muvaffaqiyatli kirish — token qaytariladi"),
        400: OpenApiResponse(description="Noto'g'ri telefon raqam yoki parol"),
    },
)
@api_view(["POST"])
@permission_classes([AllowAny])
def login_view(request):
    """Tizimga kirish (telefon raqam + parol)"""
    serializer = LoginSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    user = serializer.validated_data["user"]

    token, _ = Token.objects.get_or_create(user=user)
    return Response({
        "message": "Muvaffaqiyatli kirdingiz",
        "token": token.key,
        "user": {
            "id": user.id,
            "phone_number": user.phone_number,
            "full_name": user.full_name,
            "role": user.role,
        },
    })


@extend_schema(
    tags=["🔐 Autentifikatsiya"],
    summary="Tizimdan chiqish",
    description="""
Joriy tokenni o'chirib tizimdan chiqish.

**Header:** Authorization: Token <token>

Chiqishdan so'ng bu token ishlamay qoladi. Qayta kirish uchun /api/auth/login/ ga murojaat qiling.
    """,
    responses={
        200: OpenApiResponse(description="Muvaffaqiyatli chiqish"),
        401: OpenApiResponse(description="Token taqdim etilmagan yoki noto'g'ri"),
    },
)
@api_view(["POST"])
@permission_classes([IsAuthenticated])
def logout_view(request):
    """Tizimdan chiqish — tokenni o'chirish"""
    request.user.auth_token.delete()
    return Response({"message": "Muvaffaqiyatli chiqdingiz"})


@extend_schema(
    tags=["🔐 Autentifikatsiya"],
    summary="Profil ko'rish va yangilash",
    description="""
Joriy foydalanuvchining profil ma'lumotlarini ko'rish yoki yangilash.

**GET** — Profil ma'lumotlarini olish  
**PUT** — To'liq yangilash  
**PATCH** — Qisman yangilash (faqat yuborilgan maydonlar o'zgaradi)

**Yangilanishi mumkin bo'lgan maydonlar:** ull_name

**Header:** Authorization: Token <token>
    """,
    responses={
        200: ProfileSerializer,
        401: OpenApiResponse(description="Autentifikatsiya talab qilinadi"),
    },
)
@api_view(["GET", "PUT", "PATCH"])
@permission_classes([IsAuthenticated])
def profile_view(request):
    """Profil ko'rish va yangilash"""
    user = request.user
    if request.method == "GET":
        serializer = ProfileSerializer(user)
        return Response(serializer.data)

    serializer = ProfileSerializer(user, data=request.data, partial=request.method == "PATCH")
    serializer.is_valid(raise_exception=True)
    serializer.save()
    return Response(serializer.data)


@extend_schema(
    tags=["🔐 Autentifikatsiya"],
    summary="Parol o'zgartirish",
    description="""
Joriy foydalanuvchining parolini o'zgartirish.

**Kerakli maydonlar:**
- old_password — Joriy parol
- 
ew_password — Yangi parol (kamida 6 ta belgi)
- 
ew_password_confirm — Yangi parol tasdiqlash

**Header:** Authorization: Token <token>

Parol o'zgartirilgandan so'ng, xavfsizlik uchun qayta login qilish tavsiya etiladi.
    """,
    request=ChangePasswordSerializer,
    responses={
        200: OpenApiResponse(description="Parol muvaffaqiyatli o'zgartirildi"),
        400: OpenApiResponse(description="Joriy parol noto'g'ri yoki parollar mos kelmadi"),
    },
)
@api_view(["POST"])
@permission_classes([IsAuthenticated])
def change_password_view(request):
    """Parol o'zgartirish"""
    serializer = ChangePasswordSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)

    user = request.user
    if not user.check_password(serializer.validated_data["old_password"]):
        return Response({"error": "Joriy parol noto'g'ri"}, status=status.HTTP_400_BAD_REQUEST)

    user.set_password(serializer.validated_data["new_password"])
    user.save()
    # Eski tokenni o'chir — xavfsizlik uchun
    Token.objects.filter(user=user).delete()
    token, _ = Token.objects.get_or_create(user=user)
    return Response({
        "message": "Parol muvaffaqiyatli o'zgartirildi",
        "token": token.key,
    })
