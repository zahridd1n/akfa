from datetime import date, timedelta
from io import BytesIO
from django.db.models import Count, Sum, Q
from django.http import HttpResponse
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes, parser_classes
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination
from drf_spectacular.utils import extend_schema, OpenApiParameter, OpenApiResponse
from drf_spectacular.types import OpenApiTypes
from ..models import (
    Product, ProductImage, ProductColor,
    Order, OrderItem, CustomUser,
)
from ..serializers.product import ProductDetailSerializer, ProductColorSerializer
from ..serializers.order import OrderSerializer
from ..serializers.admin_serializers import (
    AdminProductCreateSerializer,
    AdminOrderStatusSerializer,
    AdminCustomerSerializer,
)
from ..permissions.permissions import IsAdminUser
from ..filters.filters import OrderFilter, ProductFilter


# ─────────────────────────────────────────
# Dashboard
# ─────────────────────────────────────────
@extend_schema(
    tags=["🛡️ Admin"],
    summary="Dashboard — KPI ko'rsatkichlari",
    description="""
Admin boshqaruv paneli uchun asosiy statistika.

**Qaytariladigan ma'lumotlar:**
- 	otal_orders — Jami buyurtmalar soni
- 	oday_orders — Bugungi buyurtmalar soni
- pending_orders — Kutilayotgan buyurtmalar soni
- 	otal_products — Faol mahsulotlar soni
- 	otal_customers — Jami mijozlar soni
- monthly_revenue — Joriy oy daromadi (UZS, yetkazilgan va jarayondagi buyurtmalar)
- order_by_status — Holat bo'yicha buyurtmalar taqsimoti
- 	op_products — Eng ko'p buyurtma qilingan 5 ta mahsulot

**Header:** Authorization: Token <admin_token>  
**Ruxsat:** Faqat admin
    """,
    responses={
        200: OpenApiResponse(description="Dashboard statistikasi"),
        403: OpenApiResponse(description="Ruxsat yo'q — faqat adminlar"),
    },
)
@api_view(["GET"])
@permission_classes([IsAuthenticated, IsAdminUser])
def admin_dashboard(request):
    """Admin dashboard — KPI ko'rsatkichlari"""
    today = date.today()

    total_orders = Order.objects.count()
    today_orders = Order.objects.filter(created_at__date=today).count()
    pending_orders = Order.objects.filter(status=Order.Status.PENDING).count()
    total_products = Product.objects.filter(is_active=True).count()
    total_customers = CustomUser.objects.filter(role="client").count()

    from django.utils.timezone import now
    now_tz = now()
    month_start = now_tz.replace(day=1, hour=0, minute=0, second=0, microsecond=0)
    prev_month_end = month_start - timedelta(seconds=1)
    prev_month_start = prev_month_end.replace(day=1, hour=0, minute=0, second=0, microsecond=0)

    revenue_statuses = [Order.Status.DELIVERED, Order.Status.SHIPPED, Order.Status.PROCESSING]

    monthly_revenue = Order.objects.filter(
        created_at__gte=month_start,
        status__in=revenue_statuses,
    ).aggregate(total=Sum("total_amount"))["total"] or 0

    # ── Oylik o'zgarishlar (foiz) ──
    def _pct(curr, prev):
        if prev == 0:
            return 100 if curr > 0 else 0
        return round(((curr - prev) / prev) * 100, 1)

    last_month_order_count = Order.objects.filter(
        created_at__gte=prev_month_start, created_at__lt=month_start
    ).count()
    prev_month_revenue = Order.objects.filter(
        created_at__gte=prev_month_start,
        created_at__lt=month_start,
        status__in=revenue_statuses,
    ).aggregate(total=Sum("total_amount"))["total"] or 0
    this_month_customers = CustomUser.objects.filter(
        role="client", created_at__gte=month_start
    ).count()
    last_month_customers = CustomUser.objects.filter(
        role="client", created_at__gte=prev_month_start, created_at__lt=month_start
    ).count()
    this_month_products = Product.objects.filter(
        created_at__gte=month_start, is_active=True
    ).count()
    last_month_products = Product.objects.filter(
        created_at__gte=prev_month_start, created_at__lt=month_start, is_active=True
    ).count()

    changes = {
        "total_orders": _pct(total_orders, last_month_order_count),
        "monthly_revenue": _pct(float(monthly_revenue), float(prev_month_revenue)),
        "total_customers": _pct(this_month_customers, last_month_customers),
        "total_products": _pct(this_month_products, last_month_products),
    }

    # ── Sales chart (period: month | week) ──
    period = request.GET.get("period", "month")
    from django.db.models.functions import TruncMonth, TruncWeek

    if period == "week":
        since = now_tz - timedelta(weeks=12)
        rows = (
            Order.objects.filter(
                status__in=revenue_statuses, created_at__gte=since
            )
            .annotate(period_start=TruncWeek("created_at"))
            .values("period_start")
            .annotate(revenue=Sum("total_amount"))
            .order_by("period_start")
        )
        sales_chart_data = [
            {"label": r["period_start"].strftime("%Y-%m-%d"), "revenue": r["revenue"] or 0}
            for r in rows
        ]
    else:
        since = now_tz - timedelta(days=183)
        rows = (
            Order.objects.filter(
                status__in=revenue_statuses, created_at__gte=since
            )
            .annotate(month=TruncMonth("created_at"))
            .values("month")
            .annotate(revenue=Sum("total_amount"))
            .order_by("month")
        )
        sales_chart_data = [
            {"month": r["month"].strftime("%Y-%m"), "revenue": r["revenue"] or 0}
            for r in rows
        ]

    # ── Status bo'yicha taqsimot ──
    order_by_status = {}
    for status_val, status_label in Order.Status.choices:
        count = Order.objects.filter(status=status_val).count()
        order_by_status[status_val] = {"label": status_label, "count": count}

    # ── Top mahsulotlar ──
    top_products = (
        OrderItem.objects.values("product__name", "product__id")
        .annotate(total_qty=Sum("quantity"), total_revenue=Sum("total_price"))
        .order_by("-total_qty")[:5]
    )

    return Response({
        "total_orders": total_orders,
        "today_orders": today_orders,
        "pending_orders": pending_orders,
        "total_products": total_products,
        "total_customers": total_customers,
        "monthly_revenue": monthly_revenue,
        "order_by_status": order_by_status,
        "top_products": list(top_products),
        "sales_chart": sales_chart_data,
        "changes": changes,
    })


# ─────────────────────────────────────────
# Mahsulotlar boshqaruvi
# ─────────────────────────────────────────
@extend_schema(
    tags=["🛡️ Admin"],
    methods=["GET"],
    summary="[Admin] Barcha mahsulotlar ro'yxati",
    description="""
Faol va nofaol barcha mahsulotlarni ko'rsatadi (mijozlar katalogidan farqli — barcha holatlar ko'rinadi).

Filterlash, qidiruv va pagination qo'llab-quvvatlanadi.

**Header:** Authorization: Token <admin_token>  
**Ruxsat:** Faqat admin
    """,
)
@extend_schema(
    tags=["🛡️ Admin"],
    methods=["POST"],
    summary="[Admin] Yangi mahsulot yaratish",
    description="""
Yangi mahsulot qo'shish.

Mahsulot yaratilgandan keyin:
1. Rasmlar qo'shish: POST /api/admin-panel/products/{id}/images/
2. Ranglar qo'shish: POST /api/admin-panel/products/{id}/colors/

**Header:** Authorization: Token <admin_token>  
**Ruxsat:** Faqat admin
    """,
    request=AdminProductCreateSerializer,
    responses={
        201: OpenApiResponse(description="Mahsulot yaratildi"),
        400: OpenApiResponse(description="Noto'g'ri ma'lumot"),
    },
)
@api_view(["GET", "POST"])
@permission_classes([IsAuthenticated, IsAdminUser])
def admin_products_list(request):
    """Admin: mahsulotlar ro'yxati va yaratish"""
    if request.method == "GET":
        qs = Product.objects.all().select_related("category").prefetch_related("images", "colors")
        filterset = ProductFilter(request.GET, queryset=qs)
        qs = filterset.qs
        paginator = PageNumberPagination()
        paginator.page_size = 20
        page = paginator.paginate_queryset(qs, request)
        serializer = ProductDetailSerializer(page, many=True, context={"request": request})
        return paginator.get_paginated_response(serializer.data)

    serializer = AdminProductCreateSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    product = serializer.save()
    return Response(
        ProductDetailSerializer(product, context={"request": request}).data,
        status=status.HTTP_201_CREATED,
    )


@extend_schema(
    tags=["🛡️ Admin"],
    methods=["GET"],
    summary="[Admin] Mahsulot detali",
    description="Bitta mahsulotning to'liq ma'lumotlari (barcha rasmlar, ranglar, texnik xususiyatlar bilan).",
)
@extend_schema(
    tags=["🛡️ Admin"],
    methods=["PUT"],
    summary="[Admin] Mahsulotni to'liq yangilash",
    description="Mahsulotning barcha maydonlarini yangilash. Rasm va ranglar alohida endpointlar orqali boshqariladi.",
    request=AdminProductCreateSerializer,
)
@extend_schema(
    tags=["🛡️ Admin"],
    methods=["PATCH"],
    summary="[Admin] Mahsulotni qisman yangilash",
    description="Faqat yuborilgan maydonlarni yangilash (masalan, faqat narxni yoki faqat holatni o'zgartirish).",
    request=AdminProductCreateSerializer,
)
@extend_schema(
    tags=["🛡️ Admin"],
    methods=["DELETE"],
    summary="[Admin] Mahsulotni o'chirish",
    description="""
Mahsulotni o'chirish.

**Diqqat:** O'chirilgan mahsulot bilan bog'liq buyurtma elementlarida snapshot saqlanib qoladi
(product_name, color_name maydonlari orqali).
    """,
    responses={204: OpenApiResponse(description="O'chirildi")},
)
@api_view(["GET", "PUT", "PATCH", "DELETE"])
@permission_classes([IsAuthenticated, IsAdminUser])
def admin_product_detail(request, product_id):
    """Admin: mahsulot detail, tahrirlash, o'chirish"""
    try:
        product = Product.objects.select_related("category").prefetch_related("images", "colors").get(id=product_id)
    except Product.DoesNotExist:
        return Response({"error": "Mahsulot topilmadi"}, status=status.HTTP_404_NOT_FOUND)

    if request.method == "GET":
        return Response(ProductDetailSerializer(product, context={"request": request}).data)

    if request.method in ["PUT", "PATCH"]:
        serializer = AdminProductCreateSerializer(product, data=request.data, partial=request.method == "PATCH")
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(ProductDetailSerializer(product, context={"request": request}).data)

    product.delete()
    return Response(status=status.HTTP_204_NO_CONTENT)


@extend_schema(
    tags=["🛡️ Admin"],
    summary="[Admin] Mahsulotga rasm qo'shish",
    description="""
Mahsulotga yangi rasm yuklash.

**Multipart/form-data formati:**
- image — Rasm fayli (JPEG, PNG, WebP)
- is_main — Asosiy rasm (true/false, default: false)

Agar is_main=true yuborilsa, oldingi asosiy rasm o'zgartiriladi.

**Header:** Authorization: Token <admin_token>
    """,
    responses={
        201: OpenApiResponse(description="Rasm yuklandi"),
        400: OpenApiResponse(description="Rasm fayli talab qilinadi"),
    },
)
@api_view(["POST"])
@permission_classes([IsAuthenticated, IsAdminUser])
@parser_classes([MultiPartParser, FormParser])
def admin_product_add_image(request, product_id):
    """Admin: mahsulotga rasm qo'shish"""
    try:
        product = Product.objects.get(id=product_id)
    except Product.DoesNotExist:
        return Response({"error": "Mahsulot topilmadi"}, status=status.HTTP_404_NOT_FOUND)

    image_file = request.FILES.get("image")
    if not image_file:
        return Response({"error": "Rasm fayli talab qilinadi"}, status=status.HTTP_400_BAD_REQUEST)

    is_main = request.data.get("is_main", "false").lower() == "true"
    if is_main:
        product.images.filter(is_main=True).update(is_main=False)

    img = ProductImage.objects.create(product=product, image=image_file, is_main=is_main)
    return Response({
        "id": img.id,
        "image": request.build_absolute_uri(img.image.url),
        "is_main": img.is_main,
    }, status=201)


@extend_schema(
    tags=["🛡️ Admin"],
    summary="[Admin] Mahsulot rasmini o'chirish",
    description="Mahsulotdan bitta rasmni o'chirish. image_id — rasm ID (mahsulot detail'da ko'rinadi).",
    responses={204: OpenApiResponse(description="Rasm o'chirildi")},
)
@api_view(["DELETE"])
@permission_classes([IsAuthenticated, IsAdminUser])
def admin_product_delete_image(request, product_id, image_id):
    """Admin: mahsulot rasmini o'chirish"""
    try:
        img = ProductImage.objects.get(id=image_id, product_id=product_id)
    except ProductImage.DoesNotExist:
        return Response({"error": "Rasm topilmadi"}, status=status.HTTP_404_NOT_FOUND)
    img.delete()
    return Response(status=status.HTTP_204_NO_CONTENT)


@extend_schema(
    tags=["🛡️ Admin"],
    summary="[Admin] Asosiy rasmni belgilash",
    description="""
Bitta rasmni mahsulotning asosiy rasmi sifatida belgilash.

Oldingi asosiy rasm avtomatik asosiy bo'lmay qoladi. Faqat bitta asosiy rasm bo'lishi mumkin.

**Header:** Authorization: Token <admin_token>  
**Ruxsat:** Faqat admin
    """,
    responses={
        200: OpenApiResponse(description="Asosiy rasm o'rnatildi"),
        404: OpenApiResponse(description="Rasm topilmadi"),
    },
)
@api_view(["PUT", "PATCH"])
@permission_classes([IsAuthenticated, IsAdminUser])
def admin_product_set_main_image(request, product_id, image_id):
    """Admin: rasmni asosiy qilib belgilash"""
    try:
        img = ProductImage.objects.get(id=image_id, product_id=product_id)
    except ProductImage.DoesNotExist:
        return Response({"error": "Rasm topilmadi"}, status=status.HTTP_404_NOT_FOUND)

    img.product.images.filter(is_main=True).exclude(id=img.id).update(is_main=False)
    img.is_main = True
    img.save(update_fields=["is_main"])
    return Response({
        "id": img.id,
        "image": request.build_absolute_uri(img.image.url),
        "is_main": True,
        "message": "Asosiy rasm o'rnatildi",
    })


@extend_schema(
    tags=["🛡️ Admin"],
    summary="[Admin] Mahsulotga rang qo'shish",
    description="""
Mahsulotga yangi rang varianti qo'shish.

**Maydonlar:**
- 
ame — Rang nomi (Oq, Jigarrang, Antrasit, Bronza, ...)
- hex_code — Rang kodi (#FFFFFF formatida, ixtiyoriy)
- price_modifier — Narx farqi (UZS):
  -  — Asosiy narx (o'zgarmaydi)
  - 500000 — Asosiy narxga +500,000 UZS qo'shiladi
  - -100000 — Asosiy narxdan 100,000 UZS ayiriladi
- is_available — Mavjudligi (true/false)

**Header:** Authorization: Token <admin_token>
    """,
    request=ProductColorSerializer,
    responses={201: ProductColorSerializer},
)
@api_view(["POST"])
@permission_classes([IsAuthenticated, IsAdminUser])
def admin_product_add_color(request, product_id):
    """Admin: mahsulotga rang qo'shish"""
    try:
        product = Product.objects.get(id=product_id)
    except Product.DoesNotExist:
        return Response({"error": "Mahsulot topilmadi"}, status=status.HTTP_404_NOT_FOUND)

    serializer = ProductColorSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    color = serializer.save(product=product)
    return Response(ProductColorSerializer(color).data, status=201)


@extend_schema(
    tags=["🛡️ Admin"],
    methods=["PUT"],
    summary="[Admin] Rangni yangilash",
    description="Mahsulot rangini to'liq yangilash (nom, hex, narx farqi, mavjudligi).",
    request=ProductColorSerializer,
)
@extend_schema(
    tags=["🛡️ Admin"],
    methods=["PATCH"],
    summary="[Admin] Rangni qisman yangilash",
    description="Faqat o'zgartirilishi kerak bo'lgan rang maydonlarini yangilash.",
    request=ProductColorSerializer,
)
@extend_schema(
    tags=["🛡️ Admin"],
    methods=["DELETE"],
    summary="[Admin] Rangni o'chirish",
    description="Mahsulotdan bitta rang variantini o'chirish.",
    responses={204: OpenApiResponse(description="Rang o'chirildi")},
)
@api_view(["PUT", "PATCH", "DELETE"])
@permission_classes([IsAuthenticated, IsAdminUser])
def admin_product_color_detail(request, product_id, color_id):
    """Admin: rang tahrirlash va o'chirish"""
    try:
        color = ProductColor.objects.get(id=color_id, product_id=product_id)
    except ProductColor.DoesNotExist:
        return Response({"error": "Rang topilmadi"}, status=status.HTTP_404_NOT_FOUND)

    if request.method == "DELETE":
        color.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    serializer = ProductColorSerializer(color, data=request.data, partial=request.method == "PATCH")
    serializer.is_valid(raise_exception=True)
    serializer.save()
    return Response(serializer.data)


# ─────────────────────────────────────────
# Buyurtmalar boshqaruvi
# ─────────────────────────────────────────
@extend_schema(
    tags=["🛡️ Admin"],
    summary="[Admin] Barcha buyurtmalar",
    description="""
Tizimda barcha mijozlarning buyurtmalarini ko'rsatadi.

**Filtr parametrlari:**
- status — Holat bo'yicha filter
- date_from — Boshlanish sanasi (ISO 8601: 2026-01-01T00:00:00)
- date_to — Tugash sanasi

Har sahifada 20 ta buyurtma (eng so'nggisi birinchi).

**Header:** Authorization: Token <admin_token>  
**Ruxsat:** Faqat admin
    """,
    parameters=[
        OpenApiParameter("status", OpenApiTypes.STR, description="pending, processing, shipped, delivered, cancelled"),
        OpenApiParameter("date_from", OpenApiTypes.DATETIME, description="Boshlanish sanasi"),
        OpenApiParameter("date_to", OpenApiTypes.DATETIME, description="Tugash sanasi"),
    ],
    responses={200: OrderSerializer(many=True)},
)
@api_view(["GET"])
@permission_classes([IsAuthenticated, IsAdminUser])
def admin_orders_list(request):
    """Admin: barcha buyurtmalar"""
    qs = Order.objects.all().select_related("user", "delivery_address").prefetch_related("items")
    filterset = OrderFilter(request.GET, queryset=qs)
    qs = filterset.qs

    paginator = PageNumberPagination()
    paginator.page_size = 20
    page = paginator.paginate_queryset(qs, request)
    serializer = OrderSerializer(page, many=True, context={"request": request})
    return paginator.get_paginated_response(serializer.data)


@extend_schema(
    tags=["🛡️ Admin"],
    summary="[Admin] Buyurtma holatini o'zgartirish",
    description="""
Buyurtma holatini yangilash.

**Holat ketma-ketligi:**
`
pending → processing → shipped → delivered
                             ↓
                         cancelled
`

**Holatlar:**
- pending — Kutilmoqda (yangi buyurtma)
- processing — Tayyorlanmoqda
- shipped — Yo'lda (yetkazuvchiga topshirildi)
- delivered — Yetkazib berildi
- cancelled — Bekor qilindi

**Header:** Authorization: Token <admin_token>  
**Ruxsat:** Faqat admin
    """,
    request=AdminOrderStatusSerializer,
    responses={
        200: OpenApiResponse(description="Holat yangilandi"),
        404: OpenApiResponse(description="Buyurtma topilmadi"),
    },
)
@api_view(["PUT"])
@permission_classes([IsAuthenticated, IsAdminUser])
def admin_order_status(request, order_id):
    """Admin: buyurtma holatini o'zgartirish"""
    try:
        order = Order.objects.get(id=order_id)
    except Order.DoesNotExist:
        return Response({"error": "Buyurtma topilmadi"}, status=status.HTTP_404_NOT_FOUND)

    serializer = AdminOrderStatusSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    order.status = serializer.validated_data["status"]
    order.save()
    return Response({
        "message": "Holat yangilandi",
        "order_number": order.order_number,
        "status": order.status,
        "status_display": order.get_status_display(),
    })


# ─────────────────────────────────────────
# Mijozlar
# ─────────────────────────────────────────
@extend_schema(
    tags=["🛡️ Admin"],
    summary="[Admin] Mijozlar ro'yxati",
    description="""
Barcha mijozlarni ko'rsatadi (faqat ole=client foydalanuvchilar).

Har bir mijoz uchun ko'rsatiladi:
- Shaxsiy ma'lumotlar (ism, telefon)
- orders_count — Jami buyurtmalar soni
- 	otal_spent — Yetkazib berilgan buyurtmalar bo'yicha jami sarflangan summa

**Qidiruv:** ?search=telefon_yoki_ism

**Header:** Authorization: Token <admin_token>  
**Ruxsat:** Faqat admin
    """,
    parameters=[
        OpenApiParameter("search", OpenApiTypes.STR, description="Telefon raqam yoki ism bo'yicha qidiruv"),
    ],
    responses={200: AdminCustomerSerializer(many=True)},
)
@api_view(["GET"])
@permission_classes([IsAuthenticated, IsAdminUser])
def admin_customers_list(request):
    """Admin: barcha mijozlar ro'yxati"""
    qs = CustomUser.objects.filter(role="client").annotate(
        orders_count=Count("orders"),
        total_spent=Sum(
            "orders__total_amount",
            filter=Q(orders__status=Order.Status.DELIVERED),
        ),
).order_by("-created_at")

    search = request.GET.get("search")
    if search:
        qs = qs.filter(
            Q(phone_number__icontains=search) | Q(full_name__icontains=search)
        )

    paginator = PageNumberPagination()
    paginator.page_size = 20
    page = paginator.paginate_queryset(qs, request)
    serializer = AdminCustomerSerializer(page, many=True)
    return paginator.get_paginated_response(serializer.data)


# ─────────────────────────────────────────
# Hisobotlar
# ─────────────────────────────────────────
def _filter_orders_by_date(qs, request):
    date_from = request.GET.get("date_from")
    date_to = request.GET.get("date_to")
    if date_from:
        qs = qs.filter(created_at__date__gte=date_from)
    if date_to:
        qs = qs.filter(created_at__date__lte=date_to)
    return qs


@extend_schema(
    tags=["🛡️ Admin"],
    summary="[Admin] Hisobot statistikasi",
    description="""
Tanlangan sana oralig'i bo'yicha hisobot statistikasi.

**Filtr parametrlari:**
- date_from — Boshlanish sanasi (YYYY-MM-DD)
- date_to — Tugash sanasi (YYYY-MM-DD)

**Qaytariladigan ma'lumotlar:**
- total_orders — Jami buyurtmalar soni
- total_revenue — Jami tushum
- avg_order_value — O'rtacha buyurtma qiymati
- orders_by_status — Holat bo'yicha taqsimot
- top_products — Eng ko'p sotilgan mahsulotlar
- recent_orders — So'nggi 50 ta buyurtma

**Header:** Authorization: Token <admin_token>  
**Ruxsat:** Faqat admin
    """,
    parameters=[
        OpenApiParameter("date_from", OpenApiTypes.DATE, description="Boshlanish sanasi"),
        OpenApiParameter("date_to", OpenApiTypes.DATE, description="Tugash sanasi"),
    ],
    responses={200: OpenApiResponse(description="Hisobot statistikasi")},
)
@api_view(["GET"])
@permission_classes([IsAuthenticated, IsAdminUser])
def admin_reports_list(request):
    """Admin: sana oralig'i bo'yicha hisobot"""
    qs = _filter_orders_by_date(Order.objects.all(), request)

    total_orders = qs.count()
    total_revenue = qs.aggregate(total=Sum("total_amount"))["total"] or 0
    avg_order_value = float(total_revenue) / total_orders if total_orders else 0

    orders_by_status = {}
    for status_val, status_label in Order.Status.choices:
        count = qs.filter(status=status_val).count()
        orders_by_status[status_val] = {"label": status_label, "count": count}

    top_products = (
        OrderItem.objects.filter(order__in=qs)
        .values("product__name", "product__id")
        .annotate(total_qty=Sum("quantity"), total_revenue=Sum("total_price"))
        .order_by("-total_qty")[:5]
    )

    recent = qs.select_related("user", "delivery_address").prefetch_related("items")[:50]

    return Response({
        "total_orders": total_orders,
        "total_revenue": total_revenue,
        "avg_order_value": round(avg_order_value, 2),
        "orders_by_status": orders_by_status,
        "top_products": list(top_products),
        "recent_orders": OrderSerializer(recent, many=True, context={"request": request}).data,
    })


def _build_excel_export(qs, status_counts):
    from openpyxl import Workbook
    from openpyxl.styles import Font, PatternFill, Alignment, Border, Side

    wb = Workbook()
    ws = wb.active
    ws.title = "Hisobot"

    header_font = Font(bold=True, color="FFFFFF", size=12)
    header_fill = PatternFill(start_color="2F80ED", end_color="2F80ED", fill_type="solid")
    thin_border = Border(
        left=Side(style="thin", color="D1D5DB"),
        right=Side(style="thin", color="D1D5DB"),
        top=Side(style="thin", color="D1D5DB"),
        bottom=Side(style="thin", color="D1D5DB"),
    )

    ws.merge_cells("A1:F1")
    ws["A1"] = "SARAMAX — Sotuv hisoboti"
    ws["A1"].font = Font(bold=True, size=16, color="1F2937")
    ws["A1"].alignment = Alignment(horizontal="center")
    ws.merge_cells("A2:F2")
    ws["A2"] = "Yaratilgan sana: " + date.today().strftime("%d.%m.%Y")
    ws["A2"].alignment = Alignment(horizontal="center")

    headers = ["Buyurtma #", "Mijoz", "Telefon", "Summa (so'm)", "Holat", "Sana"]
    ws.append([])
    ws.append(headers)
    for cell in ws[3]:
        cell.font = header_font
        cell.fill = header_fill
        cell.border = thin_border
        cell.alignment = Alignment(horizontal="center")

    row = 4
    for order in qs:
        ism = order.user.full_name if order.user else "—"
        telefon = order.user.phone_number if order.user else "—"
        ws.append([
            order.order_number,
            ism,
            telefon,
            float(order.total_amount),
            order.get_status_display(),
            order.created_at.strftime("%d.%m.%Y %H:%M"),
        ])
        for cell in ws[row]:
            cell.border = thin_border
        ws.cell(row=row, column=4).number_format = "#,##0"
        row += 1

    total_row = row + 1
    ws.merge_cells(start_row=total_row, start_column=1, end_row=total_row, end_column=3)
    ws.cell(row=total_row, column=1, value="JAMI")
    ws.cell(row=total_row, column=1).font = Font(bold=True, size=12)
    ws.cell(row=total_row, column=4, value=float(qs.aggregate(t=Sum("total_amount"))["t"] or 0))
    ws.cell(row=total_row, column=4).font = Font(bold=True, size=12)
    ws.cell(row=total_row, column=4).number_format = "#,##0"

    ws.column_dimensions["A"].width = 14
    ws.column_dimensions["B"].width = 28
    ws.column_dimensions["C"].width = 20
    ws.column_dimensions["D"].width = 18
    ws.column_dimensions["E"].width = 18
    ws.column_dimensions["F"].width = 20

    buf = BytesIO()
    wb.save(buf)
    buf.seek(0)
    return buf


def _build_word_export(qs):
    html_rows = "".join(
        f"<tr>"
        f"<td>{o.order_number}</td>"
        f"<td>{o.user.full_name if o.user else '—'}</td>"
        f"<td>{o.user.phone_number if o.user else '—'}</td>"
        f"<td align='right'>{float(o.total_amount):,.0f}</td>"
        f"<td>{o.get_status_display()}</td>"
        f"<td>{o.created_at.strftime('%d.%m.%Y')}</td>"
        f"</tr>"
        for o in qs
    )
    total = qs.aggregate(t=Sum("total_amount"))["t"] or 0
    html = f"""<html><head><meta charset="utf-8"></head><body>
    <h2 style="text-align:center">SARAMAX — Sotuv hisoboti</h2>
    <p style="text-align:center">Yaratilgan sana: {date.today().strftime('%d.%m.%Y')}</p>
    <table border="1" cellpadding="6" cellspacing="0" style="border-collapse:collapse;width:100%">
    <tr style="background:#2F80ED;color:#fff">
      <th>Buyurtma #</th><th>Mijoz</th><th>Telefon</th><th>Summa (so'm)</th><th>Holat</th><th>Sana</th>
    </tr>{html_rows}
    <tr><td colspan="3"><b>JAMI</b></td><td align="right"><b>{float(total):,.0f}</b></td><td colspan="2"></td></tr>
    </table></body></html>"""
    buf = BytesIO()
    buf.write(html.encode("utf-8"))
    buf.seek(0)
    return buf


@extend_schema(
    tags=["🛡️ Admin"],
    summary="[Admin] Hisobotni export qilish",
    description="""
Hisobotni Excel (.xlsx) yoki Word (.doc) formatida yuklab olish.

**Parametrlar:**
- date_from — Boshlanish sanasi (YYYY-MM-DD)
- date_to — Tugash sanasi (YYYY-MM-DD)
- format — `excel` yoki `word` (default: excel)

**Header:** Authorization: Token <admin_token>  
**Ruxsat:** Faqat admin
    """,
    parameters=[
        OpenApiParameter("date_from", OpenApiTypes.DATE, description="Boshlanish sanasi"),
        OpenApiParameter("date_to", OpenApiTypes.DATE, description="Tugash sanasi"),
        OpenApiParameter("format", OpenApiTypes.STR, description="excel | word"),
    ],
    responses={200: OpenApiResponse(description="Fayl yuklanadi")},
)
@api_view(["GET"])
@permission_classes([IsAuthenticated, IsAdminUser])
def admin_reports_export(request):
    """Admin: hisobotni Excel/Word formatida eksport qilish"""
    qs = _filter_orders_by_date(Order.objects.select_related("user"), request)

    fmt = request.GET.get("format", "excel")
    if fmt == "word":
        buf = _build_word_export(qs)
        response = HttpResponse(
            buf.read(),
            content_type="application/msword",
        )
        response["Content-Disposition"] = f'attachment; filename="saramax_hisobot.doc"'
    else:
        buf = _build_excel_export(qs, {})
        response = HttpResponse(
            buf.read(),
            content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        )
        response["Content-Disposition"] = f'attachment; filename="saramax_hisobot.xlsx"'

    return response
