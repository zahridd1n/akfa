import random
import string
from django.db import models
from django.conf import settings
from .address import Address
from .product import Product


def generate_order_number():
    """AK-XXXX formatida unikal buyurtma raqami yaratadi"""
    while True:
        number = "".join(random.choices(string.digits, k=4))
        order_number = f"AK-{number}"
        if not Order.objects.filter(order_number=order_number).exists():
            return order_number


class Order(models.Model):
    class Status(models.TextChoices):
        PENDING = "pending", "Kutilmoqda"
        PROCESSING = "processing", "Tayyorlanmoqda"
        SHIPPED = "shipped", "Yo''lda"
        DELIVERED = "delivered", "Yetkazib berildi"
        CANCELLED = "cancelled", "Bekor qilindi"

    order_number = models.CharField(
        max_length=10,
        unique=True,
        default=generate_order_number,
        verbose_name="Buyurtma raqami",
    )
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        related_name="orders",
        verbose_name="Mijoz",
    )
    delivery_address = models.ForeignKey(
        Address,
        on_delete=models.SET_NULL,
        null=True,
        related_name="orders",
        verbose_name="Yetkazib berish manzili",
    )
    status = models.CharField(
        max_length=15,
        choices=Status.choices,
        default=Status.PENDING,
        verbose_name="Holat",
    )
    subtotal = models.DecimalField(
        max_digits=15, decimal_places=2, default=0, verbose_name="Jami (chegirmasiz)"
    )
    delivery_fee = models.DecimalField(
        max_digits=12, decimal_places=2, default=0, verbose_name="Yetkazib berish narxi"
    )
    total_amount = models.DecimalField(
        max_digits=15, decimal_places=2, default=0, verbose_name="Umumiy summa"
    )
    notes = models.TextField(blank=True, default="", verbose_name="Izoh (ixtiyoriy)")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Buyurtma"
        verbose_name_plural = "Buyurtmalar"
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.order_number} — {self.user}"

    def calculate_totals(self):
        """Subtotal va total_amount ni hisoblaydi"""
        self.subtotal = sum(item.total_price for item in self.items.all())
        self.total_amount = self.subtotal + self.delivery_fee
        self.save(update_fields=["subtotal", "total_amount"])


class OrderItem(models.Model):
    order = models.ForeignKey(
        Order, on_delete=models.CASCADE, related_name="items", verbose_name="Buyurtma"
    )
    product = models.ForeignKey(
        Product,
        on_delete=models.SET_NULL,
        null=True,
        related_name="order_items",
        verbose_name="Mahsulot",
    )
    # Snapshot — mahsulot o'chirilsa ham saqlansin
    product_name = models.CharField(max_length=200, verbose_name="Mahsulot nomi (snapshot)")
    color_name = models.CharField(max_length=60, blank=True, verbose_name="Rang (snapshot)")
    color_hex = models.CharField(max_length=7, blank=True, verbose_name="Rang HEX (snapshot)")

    width_mm = models.PositiveIntegerField(verbose_name="Kenglik (mm)")
    height_mm = models.PositiveIntegerField(verbose_name="Balandlik (mm)")
    quantity = models.PositiveSmallIntegerField(default=1, verbose_name="Miqdori")
    unit_price = models.DecimalField(
        max_digits=12, decimal_places=2, verbose_name="Birlik narxi (snapshot)"
    )
    total_price = models.DecimalField(
        max_digits=15, decimal_places=2, verbose_name="Jami narxi"
    )

    class Meta:
        verbose_name = "Buyurtma elementi"
        verbose_name_plural = "Buyurtma elementlari"

    def __str__(self):
        return f"{self.product_name} ({self.width_mm}x{self.height_mm}) x{self.quantity}"

    @property
    def sqm(self):
        return (self.width_mm / 1000) * (self.height_mm / 1000)
