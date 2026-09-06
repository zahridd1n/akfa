from django.db import models
from django.conf import settings
from .product import Product, ProductColor


class Cart(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="cart",
        verbose_name="Foydalanuvchi",
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Savat"
        verbose_name_plural = "Savatlar"

    def __str__(self):
        return f"Savat — {self.user}"

    @property
    def total_items(self):
        return self.items.count()

    @property
    def total_amount(self):
        return sum(item.total_price for item in self.items.all())


class CartItem(models.Model):
    cart = models.ForeignKey(
        Cart, on_delete=models.CASCADE, related_name="items", verbose_name="Savat"
    )
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name="cart_items",
        verbose_name="Mahsulot",
    )
    color = models.ForeignKey(
        ProductColor,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="cart_items",
        verbose_name="Rang",
    )
    width_mm = models.PositiveIntegerField(verbose_name="Kenglik (mm)")
    height_mm = models.PositiveIntegerField(verbose_name="Balandlik (mm)")
    quantity = models.PositiveSmallIntegerField(default=1, verbose_name="Miqdori")
    added_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Savat elementi"
        verbose_name_plural = "Savat elementlari"
        ordering = ["-added_at"]

    def __str__(self):
        return f"{self.product.name} ({self.width_mm}x{self.height_mm}) x{self.quantity}"

    @property
    def unit_price(self):
        """Birlik narxi — avtomatik hisoblanadi"""
        return self.product.calculate_price(self.width_mm, self.height_mm, self.color)

    @property
    def total_price(self):
        """Jami narx = birlik narxi × miqdori"""
        return self.unit_price * self.quantity

    @property
    def sqm(self):
        """Kv.m hisobi"""
        return (self.width_mm / 1000) * (self.height_mm / 1000)
