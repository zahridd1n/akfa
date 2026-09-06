from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from drf_spectacular.utils import extend_schema, OpenApiResponse
from ..models import Cart, CartItem, Product, ProductColor
from ..serializers.cart import (
    CartSerializer, CartItemSerializer,
    AddToCartSerializer, UpdateCartItemSerializer,
)


def get_or_create_cart(user):
    cart, _ = Cart.objects.get_or_create(user=user)
    return cart


@extend_schema(
    tags=["🛒 Savat"],
    summary="Savatni ko'rish",
    description="""
Joriy foydalanuvchining savatini ko'rsatadi.

Savat bo'sh bo'lsa items: [] va 	otal_amount: 0 qaytariladi.

Har bir savat elementi uchun ko'rsatiladi:
- Mahsulot nomi, rangi, o'lchami
- Birlik narxi (avtomatik hisoblangan: base_price + rang farqi × kv.m)
- Jami narxi (birlik narxi × miqdor)
- Kv.m hisobi

**Header:** Authorization: Token <token>
    """,
    responses={200: CartSerializer},
)
@api_view(["GET"])
@permission_classes([IsAuthenticated])
def cart_detail(request):
    """Savatni ko'rish"""
    cart = get_or_create_cart(request.user)
    serializer = CartSerializer(cart, context={"request": request})
    return Response(serializer.data)


@extend_schema(
    tags=["🛒 Savat"],
    summary="Savatga mahsulot qo'shish",
    description="""
Savatga yangi mahsulot qo'shish.

**Kerakli maydonlar:**
- product_id — Mahsulot ID
- width_mm — Kenglik (mm, 100–10000)
- height_mm — Balandlik (mm, 100–10000)
- quantity — Miqdor (1–100, default: 1)
- color_id — Rang ID (ixtiyoriy)

**Muhim:** Agar xuddi shunday mahsulot (bir xil o'lcham, rang) savatda mavjud bo'lsa,
miqdori qo'shiladi — yangi element yaratilmaydi.

Narx avtomatik hisoblanadi: (base_price + rang_farqi) × kv.m

**Header:** Authorization: Token <token>
    """,
    request=AddToCartSerializer,
    responses={
        201: OpenApiResponse(description="Savatga muvaffaqiyatli qo'shildi"),
        400: OpenApiResponse(description="Noto'g'ri ma'lumot — mahsulot topilmadi yoki rang noto'g'ri"),
    },
)
@api_view(["POST"])
@permission_classes([IsAuthenticated])
def cart_add(request):
    """Savatga mahsulot qo'shish"""
    serializer = AddToCartSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)

    cart = get_or_create_cart(request.user)
    data = serializer.validated_data

    product = Product.objects.get(id=data["product_id"])
    color = None
    if data.get("color_id"):
        color = ProductColor.objects.get(id=data["color_id"])

    existing = cart.items.filter(
        product=product,
        color=color,
        width_mm=data["width_mm"],
        height_mm=data["height_mm"],
    ).first()

    if existing:
        existing.quantity += data["quantity"]
        existing.save()
        item = existing
    else:
        item = CartItem.objects.create(
            cart=cart,
            product=product,
            color=color,
            width_mm=data["width_mm"],
            height_mm=data["height_mm"],
            quantity=data["quantity"],
        )

    serializer = CartItemSerializer(item, context={"request": request})
    return Response({
        "message": "Savatga qo'shildi",
        "item": serializer.data,
        "cart_total": cart.total_amount,
    }, status=status.HTTP_201_CREATED)


@extend_schema(
    tags=["🛒 Savat"],
    summary="Savat elementini yangilash",
    description="""
Savat elementining miqdori yoki o'lchamini o'zgartirish.

**PUT** — To'liq yangilash (barcha maydonlar kerak)  
**PATCH** — Qisman yangilash (faqat o'zgaradigan maydonlar)

**Yangilanishi mumkin:**
- quantity — Miqdor (1–100)
- width_mm — Kenglik (mm)
- height_mm — Balandlik (mm)

Narx o'lcham o'zgarsa avtomatik qayta hisoblanadi.

**Header:** Authorization: Token <token>
    """,
    request=UpdateCartItemSerializer,
)
@api_view(["PUT", "PATCH"])
@permission_classes([IsAuthenticated])
def cart_item_update(request, item_id):
    """Savat elementini yangilash"""
    cart = get_or_create_cart(request.user)
    try:
        item = cart.items.get(id=item_id)
    except CartItem.DoesNotExist:
        return Response({"error": "Element topilmadi"}, status=status.HTTP_404_NOT_FOUND)

    serializer = UpdateCartItemSerializer(data=request.data, partial=request.method == "PATCH")
    serializer.is_valid(raise_exception=True)

    for attr, val in serializer.validated_data.items():
        setattr(item, attr, val)
    item.save()

    return Response(CartItemSerializer(item, context={"request": request}).data)


@extend_schema(
    tags=["🛒 Savat"],
    summary="Savat elementini o'chirish",
    description="""
Savatdan bitta mahsulotni o'chirish.

item_id — Savat elementi ID (savatni ko'rishda qaytariladigan items[].id)

**Header:** Authorization: Token <token>
    """,
    responses={
        200: OpenApiResponse(description="Element o'chirildi, yangi savat jami qaytariladi"),
        404: OpenApiResponse(description="Savat elementi topilmadi"),
    },
)
@api_view(["DELETE"])
@permission_classes([IsAuthenticated])
def cart_item_delete(request, item_id):
    """Savat elementini o'chirish"""
    cart = get_or_create_cart(request.user)
    try:
        item = cart.items.get(id=item_id)
    except CartItem.DoesNotExist:
        return Response({"error": "Element topilmadi"}, status=status.HTTP_404_NOT_FOUND)

    item.delete()
    return Response({"message": "O'chirildi", "cart_total": cart.total_amount})


@extend_schema(
    tags=["🛒 Savat"],
    summary="Savatni to'liq tozalash",
    description="""
Savattagi barcha mahsulotlarni o'chirish.

Buyurtma rasmiylashtirish muvaffaqiyatli bo'lganda savat avtomatik tozalanadi.
Bu endpoint esa foydalanuvchi savatni qo'lda tozalamoqchi bo'lganda ishlatiladi.

**Header:** Authorization: Token <token>
    """,
    responses={200: OpenApiResponse(description="Savat tozalandi")},
)
@api_view(["DELETE"])
@permission_classes([IsAuthenticated])
def cart_clear(request):
    """Savatni tozalash"""
    cart = get_or_create_cart(request.user)
    cart.items.all().delete()
    return Response({"message": "Savat tozalandi"})
