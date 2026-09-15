from rest_framework import status
from rest_framework.decorators import api_view, permission_classes, parser_classes
from rest_framework.parsers import MultiPartParser, FormParser, JSONParser
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from drf_spectacular.utils import extend_schema, OpenApiResponse
from ..models import SiteSettings, Banner, ContactMessage, About
from ..serializers.site_settings import SiteSettingsSerializer, BannerSerializer, ContactMessageSerializer, AboutSerializer
from ..permissions.permissions import IsAdminUser



@extend_schema(
    tags=["Sayt sozlamalari"],
    summary="Sayt sozlamalarini olish",
    description="""
Saytning barcha umumiy sozlamalarini qaytaradi.

**Frontendda ishlatiladi:**
- Header: telefon raqamlar
- Footer: kompaniya haqida, copyright, ijtimoiy tarmoq havolalar
- Kontakt sahifa: email, manzil, ish vaqti
- SEO: title, description, og:image

Bu endpoint barcha foydalanuvchilar uchun ochiq (autentifikatsiya shart emas).
Sayt ochilganda bir marta chaqiriladi va keshlanadi.
    """,
    responses={200: SiteSettingsSerializer},
)
@api_view(["GET"])
@permission_classes([AllowAny])
def site_settings_view(request):
    """Sayt sozlamalarini qaytarish"""
    settings = SiteSettings.get_settings()
    serializer = SiteSettingsSerializer(settings, context={"request": request})
    return Response(serializer.data)


@extend_schema(
    tags=["Sayt sozlamalari"],
    summary="[Admin] Sayt sozlamalarini yangilash",
    description="""
Sayt sozlamalarini yangilash.

**PATCH** metodi bilan faqat kerakli maydonlarni yuborish mumkin.

Yangilanishi mumkin bo'lgan maydonlar:
- Telefon raqamlar (`phone_main`, `phone_whatsapp`, `phone_extra`)
- Kontakt (`email`, `address`, `work_hours`)
- Ijtimoiy tarmoqlar (`telegram_url`, `instagram_url`, `facebook_url`, `youtube_url`)
- Footer (`footer_about`, `footer_copyright`)
- SEO (`site_title`, `site_description`, `og_image`)

**Header:** Authorization: Token <admin_token>
**Ruxsat:** Faqat admin
    """,
    request=SiteSettingsSerializer,
    responses={
        200: SiteSettingsSerializer,
        403: OpenApiResponse(description="Ruxsat yo'q"),
    },
)
@api_view(["PUT", "PATCH"])
@permission_classes([IsAuthenticated, IsAdminUser])
@parser_classes([MultiPartParser, FormParser, JSONParser])
def admin_site_settings_update(request):
    """[Admin] Sayt sozlamalarini yangilash"""
    settings = SiteSettings.get_settings()
    serializer = SiteSettingsSerializer(
        settings,
        data=request.data,
        partial=True,
        context={"request": request},
    )
    serializer.is_valid(raise_exception=True)
    serializer.save()
    return Response(serializer.data)


@extend_schema(
    tags=["Sayt sozlamalari"],
    summary="Biz haqimizda sahifasi ma'lumotlarini olish",
    responses={200: AboutSerializer},
)
@api_view(["GET"])
@permission_classes([AllowAny])
def about_view(request):
    """Biz haqimizda sahifasi ma'lumotlari"""
    about = About.get_about()
    serializer = AboutSerializer(about, context={"request": request})
    return Response(serializer.data)


@extend_schema(
    tags=["Sayt sozlamalari"],
    summary="[Admin] Biz haqimizda ma'lumotlarini yangilash",
    request=AboutSerializer,
    responses={200: AboutSerializer},
)
@api_view(["PUT", "PATCH"])
@permission_classes([IsAuthenticated, IsAdminUser])
@parser_classes([MultiPartParser, FormParser, JSONParser])
def admin_about_update(request):
    """[Admin] Biz haqimizda ma'lumotlarini yangilash"""
    about = About.get_about()
    serializer = AboutSerializer(
        about,
        data=request.data,
        partial=True,
        context={"request": request},
    )
    serializer.is_valid(raise_exception=True)
    serializer.save()
    return Response(serializer.data)


@extend_schema(
    tags=["Sayt sozlamalari"],
    summary="Faol bannerlar ro'yxati",
    description="""
Bosh sahifa uchun faol bannerlarni tartib raqami bo'yicha qaytaradi.

Har bir banner:
- `title` - Sarlavha
- `subtitle` - Pastki sarlavha (ixtiyoriy)
- `button_text` - Tugma matni (masalan: "Katalogni ko'rish")
- `button_url` - Tugma havolasi
- `image` - Banner rasmi URL

Faqat `is_active=true` bo'lgan bannerlar qaytariladi.
Bu endpoint autentifikatsiyasiz ochiq.
    """,
    responses={200: BannerSerializer(many=True)},
)
@api_view(["GET"])
@permission_classes([AllowAny])
def banners_list(request):
    """Faol bannerlar ro'yxati"""
    banners = Banner.objects.filter(is_active=True).order_by("order", "-created_at")
    serializer = BannerSerializer(banners, many=True, context={"request": request})
    return Response(serializer.data)


@extend_schema(
    tags=["Sayt sozlamalari"],
    summary="[Admin] Banner qo'shish",
    description="""
Yangi banner yaratish.

**Multipart/form-data formatida:**
- `title` - Sarlavha (majburiy)
- `subtitle` - Pastki sarlavha (ixtiyoriy)
- `button_text` - Tugma matni
- `button_url` - Tugma havolasi
- `image` - Rasm fayli (majburiy)
- `is_active` - Faolmi (true/false, default: true)
- `order` - Tartib raqami (kichik raqam birinchi ko'rinadi)

**Header:** Authorization: Token <admin_token>
    """,
    request=BannerSerializer,
    responses={
        201: BannerSerializer,
        400: OpenApiResponse(description="Noto'g'ri ma'lumot"),
    },
)
@api_view(["POST"])
@permission_classes([IsAuthenticated, IsAdminUser])
@parser_classes([MultiPartParser, FormParser])
def admin_banner_create(request):
    """[Admin] Yangi banner yaratish"""
    serializer = BannerSerializer(data=request.data, context={"request": request})
    serializer.is_valid(raise_exception=True)
    serializer.save()
    return Response(serializer.data, status=status.HTTP_201_CREATED)


@extend_schema(
    tags=["Sayt sozlamalari"],
    methods=["PUT", "PATCH"],
    summary="[Admin] Bannerni yangilash",
    description="""
Bannerni yangilash.

**PUT** - barcha maydonlarni yangilash
**PATCH** - faqat yuborilgan maydonlarni yangilash (masalan, faqat `is_active` o'zgartirish)

**Header:** Authorization: Token <admin_token>
    """,
    request=BannerSerializer,
    responses={200: BannerSerializer},
)
@extend_schema(
    tags=["Sayt sozlamalari"],
    methods=["DELETE"],
    summary="[Admin] Bannerni o'chirish",
    description="Bannerni o'chirish. `banner_id` - banner ID raqami.",
    responses={204: OpenApiResponse(description="O'chirildi")},
)
@api_view(["PUT", "PATCH", "DELETE"])
@permission_classes([IsAuthenticated, IsAdminUser])
@parser_classes([MultiPartParser, FormParser, JSONParser])
def admin_banner_detail(request, banner_id):
    """[Admin] Bannerni yangilash va o'chirish"""
    try:
        banner = Banner.objects.get(id=banner_id)
    except Banner.DoesNotExist:
        return Response({"error": "Banner topilmadi"}, status=status.HTTP_404_NOT_FOUND)

    if request.method == "DELETE":
        banner.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    serializer = BannerSerializer(
        banner,
        data=request.data,
        partial=request.method == "PATCH",
        context={"request": request},
    )
    serializer.is_valid(raise_exception=True)
    serializer.save()
    return Response(serializer.data)


# ─── Contact Messages ─────────────────────────────────────────────────────────

@api_view(["POST"])
@permission_classes([AllowAny])
def contact_submit(request):
    """Murojat yuborish (ommaviy)"""
    serializer = ContactMessageSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    serializer.save()
    return Response({"detail": "Murojatingiz qabul qilindi!"}, status=status.HTTP_201_CREATED)


@api_view(["GET"])
@permission_classes([IsAuthenticated, IsAdminUser])
def admin_contacts_list(request):
    """[Admin] Murojatlar ro'yxati"""
    qs = ContactMessage.objects.all()
    # mark as read filter
    is_read = request.query_params.get("is_read")
    if is_read is not None:
        qs = qs.filter(is_read=is_read.lower() == "true")
    serializer = ContactMessageSerializer(qs, many=True)
    return Response(serializer.data)


@api_view(["PATCH", "DELETE"])
@permission_classes([IsAuthenticated, IsAdminUser])
def admin_contact_detail(request, contact_id):
    """[Admin] Murojatni o'qildi deb belgilash yoki o'chirish"""
    try:
        msg = ContactMessage.objects.get(id=contact_id)
    except ContactMessage.DoesNotExist:
        return Response({"error": "Topilmadi"}, status=status.HTTP_404_NOT_FOUND)

    if request.method == "DELETE":
        msg.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    msg.is_read = request.data.get("is_read", msg.is_read)
    msg.save()
    return Response(ContactMessageSerializer(msg).data)