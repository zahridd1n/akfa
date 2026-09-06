from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination
from drf_spectacular.utils import extend_schema, OpenApiParameter, OpenApiResponse
from drf_spectacular.types import OpenApiTypes
from ..models import Order, OrderItem, Address, Cart
from ..serializers.order import OrderSerializer, CreateOrderSerializer
from ..filters.filters import OrderFilter


@extend_schema(
    tags=["📋 Buyurtmalar"],
    methods=["GET"],
    summary="Buyurtmalar ro'yxati",
    description="""
Joriy foydalanuvchining barcha buyurtmalarini ko'rsatadi.

**Filtr parametrlari:**
- status — Buyurtma holati:
  - pending — Kutilmoqda
  - processing — Tayyorlanmoqda
  - shipped — Yo'lda
  - delivered — Yetkazib berildi
  - cancelled — Bekor qilindi

**Buyurtma raqami formati:** AK-XXXX (masalan: AK-1452)

Har sahifada 10 ta buyurtma (eng so'nggisi birinchi).

**Header:** Authorization: Token <token>
    """,
    parameters=[
        OpenApiParameter("status", OpenApiTypes.STR, description="Holat bo'yicha filter: pending, processing, shipped, delivered, cancelled"),
    ],
    responses={200: OrderSerializer(many=True)},
)
@extend_schema(
    tags=["📋 Buyurtmalar"],
    methods=["POST"],
    summary="Yangi buyurtma rasmiylashtirish",
    description="""
Savatdagi mahsulotlardan yangi buyurtma yaratish.

**Oldindan kerakli shartlar:**
1. Savatda kamida bitta mahsulot bo'lishi kerak
2. Tizimga kirgan bo'lish kerak

**Kerakli maydonlar:**
- ddress_id — Yetkazib berish manzili ID (profildan)
- 
otes — Qo'shimcha izoh (ixtiyoriy, masalan: "4-qavat, chap eshik")
- delivery_fee — Yetkazib berish narxi (ixtiyoriy, default: 0)

**Buyurtma rasmiylashtirish jarayoni:**
1. Savat → buyurtmaga aylanadi
2. Har bir mahsulot snapshot saqlanadi (mahsulot o'chirilsa ham saqlansin)
3. Narxlar o'sha paytdagi narxlarda qotib qoladi
4. Savat avtomatik tozalanadi
5. Buyurtma raqami generatsiya qilinadi (AK-XXXX format)

**Header:** Authorization: Token <token>
    """,
    request=CreateOrderSerializer,
    responses={
        201: OpenApiResponse(description="Buyurtma muvaffaqiyatli yaratildi"),
        400: OpenApiResponse(description="Savat bo'sh yoki manzil topilmadi"),
    },
)
@api_view(["GET", "POST"])
@permission_classes([IsAuthenticated])
def orders_list_create(request):
    """Buyurtmalar ro'yxati va yangi buyurtma"""
    if request.method == "GET":
        qs = Order.objects.filter(user=request.user).prefetch_related("items", "delivery_address")
        filterset = OrderFilter(request.GET, queryset=qs)
        qs = filterset.qs

        paginator = PageNumberPagination()
        paginator.page_size = 10
        page = paginator.paginate_queryset(qs, request)
        serializer = OrderSerializer(page, many=True, context={"request": request})
        return paginator.get_paginated_response(serializer.data)

    serializer = CreateOrderSerializer(data=request.data, context={"request": request})
    serializer.is_valid(raise_exception=True)

    try:
        cart = request.user.cart
    except Cart.DoesNotExist:
        return Response({"error": "Savatingiz bo'sh"}, status=status.HTTP_400_BAD_REQUEST)

    if not cart.items.exists():
        return Response({"error": "Savatingiz bo'sh"}, status=status.HTTP_400_BAD_REQUEST)

    address = Address.objects.get(id=serializer.validated_data["address_id"], user=request.user)

    order = Order.objects.create(
        user=request.user,
        delivery_address=address,
        notes=serializer.validated_data.get("notes", ""),
        delivery_fee=serializer.validated_data.get("delivery_fee", 0),
    )

    subtotal = 0
    for cart_item in cart.items.all():
        unit_price = cart_item.unit_price
        total_price = unit_price * cart_item.quantity
        subtotal += total_price

        OrderItem.objects.create(
            order=order,
            product=cart_item.product,
            product_name=cart_item.product.name,
            color_name=cart_item.color.name if cart_item.color else "",
            color_hex=cart_item.color.hex_code if cart_item.color else "",
            width_mm=cart_item.width_mm,
            height_mm=cart_item.height_mm,
            quantity=cart_item.quantity,
            unit_price=unit_price,
            total_price=total_price,
        )

    order.subtotal = subtotal
    order.total_amount = subtotal + order.delivery_fee
    order.save()
    cart.items.all().delete()

    return Response(
        OrderSerializer(order, context={"request": request}).data,
        status=status.HTTP_201_CREATED,
    )


@extend_schema(
    tags=["📋 Buyurtmalar"],
    summary="Buyurtma detali",
    description="""
Bitta buyurtmaning to'liq ma'lumotlarini ko'rsatadi.

**Javobda ko'rsatiladi:**
- Buyurtma raqami va holati
- Yetkazib berish manzili (to'liq)
- Barcha buyurtma elementlari (mahsulot nomi, rangi, o'lchami, narxi — snapshot)
- Narx taqsimoti: subtotal + yetkazib berish = jami

**URL parametri:** order_number — buyurtma raqami (masalan: AK-1452)

**Header:** Authorization: Token <token>
    """,
    responses={
        200: OrderSerializer,
        404: OpenApiResponse(description="Buyurtma topilmadi"),
    },
)
@api_view(["GET"])
@permission_classes([IsAuthenticated])
def order_detail(request, order_number):
    """Buyurtma detali"""
    try:
        order = Order.objects.prefetch_related("items", "delivery_address").get(
            order_number=order_number,
            user=request.user,
        )
    except Order.DoesNotExist:
        return Response({"error": "Buyurtma topilmadi"}, status=status.HTTP_404_NOT_FOUND)

    serializer = OrderSerializer(order, context={"request": request})
    return Response(serializer.data)


@extend_schema(
    tags=["📋 Buyurtmalar"],
    summary="Buyurtmani bekor qilish",
    description="""
Buyurtmani bekor qilish.

**Faqat quyidagi holatlardagi buyurtmani bekor qilish mumkin:**
- pending — Kutilmoqda
- processing — Tayyorlanmoqda

Agar buyurtma shipped (yo'lda) yoki delivered (yetkazilgan) holatida bo'lsa — bekor qilib bo'lmaydi.

**URL parametri:** order_number — buyurtma raqami (masalan: AK-1452)

**Header:** Authorization: Token <token>
    """,
    responses={
        200: OpenApiResponse(description="Buyurtma bekor qilindi"),
        400: OpenApiResponse(description="Bu holatdagi buyurtmani bekor qilib bo'lmaydi"),
        404: OpenApiResponse(description="Buyurtma topilmadi"),
    },
)
@api_view(["POST"])
@permission_classes([IsAuthenticated])
def order_cancel(request, order_number):
    """Buyurtmani bekor qilish"""
    try:
        order = Order.objects.get(order_number=order_number, user=request.user)
    except Order.DoesNotExist:
        return Response({"error": "Buyurtma topilmadi"}, status=status.HTTP_404_NOT_FOUND)

    if order.status not in [Order.Status.PENDING, Order.Status.PROCESSING]:
        return Response(
            {"error": f"'{order.get_status_display()}' holatidagi buyurtmani bekor qilib bo'lmaydi"},
            status=status.HTTP_400_BAD_REQUEST,
        )

    order.status = Order.Status.CANCELLED
    order.save()
    return Response({"message": "Buyurtma bekor qilindi", "order_number": order.order_number})
