from django.db import models
from django.conf import settings


class Address(models.Model):
    class Region(models.TextChoices):
        TASHKENT_CITY = "tashkent_city", "Toshkent shahri"
        TASHKENT_REGION = "tashkent_region", "Toshkent viloyati"
        SAMARKAND = "samarkand", "Samarqand"
        BUKHARA = "bukhara", "Buxoro"
        NAMANGAN = "namangan", "Namangan"
        ANDIJAN = "andijan", "Andijon"
        FERGANA = "fergana", "Farg''ona"
        KASHKADARYA = "kashkadarya", "Qashqadaryo"
        SURKHANDARYA = "surkhandarya", "Surxondaryo"
        SYRDARYA = "syrdarya", "Sirdaryo"
        JIZZAKH = "jizzakh", "Jizzax"
        NAVOI = "navoi", "Navoiy"
        KHOREZM = "khorezm", "Xorazm"
        KARAKALPAKSTAN = "karakalpakstan", "Qoraqalpog''iston"

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="addresses",
        verbose_name="Foydalanuvchi",
    )
    region = models.CharField(
        max_length=20,
        choices=Region.choices,
        verbose_name="Viloyat",
    )
    city = models.CharField(max_length=100, verbose_name="Shahar / tuman")
    street = models.CharField(max_length=200, verbose_name="Ko''cha")
    house_number = models.CharField(max_length=20, verbose_name="Uy raqami")
    apartment = models.CharField(
        max_length=20, blank=True, default="", verbose_name="Xonadon (ixtiyoriy)"
    )
    full_address = models.TextField(
        verbose_name="To''liq aniq manzil",
        help_text="Yetkazib beruvchi uchun qo''shimcha ma''lumot (mo''ljal, qavat, va boshqalar)",
    )
    is_default = models.BooleanField(default=False, verbose_name="Asosiy manzil")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Manzil"
        verbose_name_plural = "Manzillar"
        ordering = ["-is_default", "-created_at"]

    def __str__(self):
        return f"{self.get_region_display()}, {self.city}, {self.street} {self.house_number}"

    def save(self, *args, **kwargs):
        # Faqat bitta default manzil bo'lishi uchun
        if self.is_default:
            Address.objects.filter(user=self.user, is_default=True).exclude(pk=self.pk).update(
                is_default=False
            )
        super().save(*args, **kwargs)
