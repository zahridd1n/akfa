from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from drf_spectacular.utils import extend_schema, OpenApiResponse
from ..models import Address
from ..serializers.address import AddressSerializer


@extend_schema(tags=["📍 Manzillar"])
class AddressViewSet(viewsets.ModelViewSet):
    """
    Foydalanuvchining yetkazib berish manzillarini boshqarish.

    Har bir foydalanuvchi bir necha manzil saqlashi mumkin.
    Bitta manzil 'asosiy' (is_default=true) bo'lishi mumkin —
    buyurtma berishda bu manzil avtomatik taklif etiladi.

    **Header:** Authorization: Token <token>
    """
    serializer_class = AddressSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Address.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    @extend_schema(
        summary="Manzillar ro'yxati",
        description="Joriy foydalanuvchiga tegishli barcha manzillarni ko'rsatadi. Asosiy manzil ro'yxat boshida keladi.",
    )
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    @extend_schema(
        summary="Yangi manzil qo'shish",
        description="""
Profilga yangi manzil qo'shish.

**Maydonlar:**
- egion — Viloyat (choices: tashkent_city, tashkent_region, samarkand, bukhara, namangan, andijan, fergana, kashkadarya, surkhandarya, syrdarya, jizzakh, navoi, khorezm, karakalpakstan)
- city — Shahar yoki tuman nomi
- street — Ko'cha nomi
- house_number — Uy raqami
- partment — Xonadon (ixtiyoriy)
- ull_address — To'liq aniq manzil matni (mo'ljal, qavat va boshqalar)
- is_default — Asosiy manzil qilib belgilash (true/false)
        """,
    )
    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)

    @extend_schema(
        summary="Manzil detali",
        description="Bitta manzilning to'liq ma'lumotlarini ko'rsatadi.",
    )
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)

    @extend_schema(
        summary="Manzilni to'liq yangilash",
        description="Manzilning barcha maydonlarini yangilash.",
    )
    def update(self, request, *args, **kwargs):
        return super().update(request, *args, **kwargs)

    @extend_schema(
        summary="Manzilni qisman yangilash",
        description="Faqat yuborilgan maydonlarni yangilash.",
    )
    def partial_update(self, request, *args, **kwargs):
        return super().partial_update(request, *args, **kwargs)

    @extend_schema(
        summary="Manzilni o'chirish",
        description="Manzilni o'chirish. Agar bu manzil bilan bog'liq buyurtmalar mavjud bo'lsa o'chirib bo'lmaydi.",
        responses={
            204: OpenApiResponse(description="Muvaffaqiyatli o'chirildi"),
            400: OpenApiResponse(description="Buyurtmalar mavjud — o'chirib bo'lmaydi"),
        },
    )
    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        if instance.orders.exists():
            return Response(
                {"error": "Bu manzil bilan bog'liq buyurtmalar mavjud, o'chirib bo'lmaydi"},
                status=status.HTTP_400_BAD_REQUEST,
            )
        self.perform_destroy(instance)
        return Response(status=status.HTTP_204_NO_CONTENT)

    @extend_schema(
        summary="Asosiy manzil qilib belgilash",
        description="""
Bu manzilni asosiy (default) manzil sifatida belgilash.

Avvalgi asosiy manzil avtomatik o'zgartiriladi.
Asosiy manzil buyurtma berishda avtomatik taklif etiladi.
        """,
        responses={
            200: OpenApiResponse(description="Asosiy manzil o'rnatildi"),
        },
    )
    @action(detail=True, methods=["post"])
    def set_default(self, request, pk=None):
        """Manzilni asosiy qilib belgilash"""
        address = self.get_object()
        Address.objects.filter(user=request.user, is_default=True).update(is_default=False)
        address.is_default = True
        address.save()
        return Response({"message": "Asosiy manzil o'rnatildi", "id": address.id})
