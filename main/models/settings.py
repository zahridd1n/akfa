from django.db import models


class SiteSettings(models.Model):
    """
    Sayt sozlamalari (yagona yozuv - Singleton pattern).
    Admin paneldan boshqariladi.
    """

    # Kontakt
    phone_main = models.CharField(
        max_length=20, blank=True, default="",
        verbose_name="Asosiy telefon",
        help_text="+998712345678"
    )
    phone_whatsapp = models.CharField(
        max_length=20, blank=True, default="",
        verbose_name="WhatsApp raqam"
    )
    phone_extra = models.CharField(
        max_length=20, blank=True, default="",
        verbose_name="Qo'shimcha telefon (ixtiyoriy)"
    )
    email = models.EmailField(
        blank=True, default="",
        verbose_name="Email"
    )
    address = models.CharField(
        max_length=300, blank=True, default="",
        verbose_name="Manzil"
    )
    work_hours = models.CharField(
        max_length=100, blank=True, default="",
        verbose_name="Ish vaqti",
        help_text="Masalan: Du-Sh 9:00-18:00"
    )

    # Ijtimoiy tarmoqlar
    telegram_url = models.URLField(blank=True, default="", verbose_name="Telegram")
    instagram_url = models.URLField(blank=True, default="", verbose_name="Instagram")
    facebook_url = models.URLField(blank=True, default="", verbose_name="Facebook")
    youtube_url = models.URLField(blank=True, default="", verbose_name="YouTube")

    # Footer
    footer_about = models.TextField(
        blank=True, default="",
        verbose_name="Footer haqida matni",
        help_text="Footer uchun qisqa kompaniya tavsifi"
    )
    footer_copyright = models.CharField(
        max_length=200, blank=True, default="",
        verbose_name="Copyright matni",
        help_text="Masalan: 2024 Saramax. Barcha huquqlar himoyalangan."
    )

    # SEO
    site_title = models.CharField(
        max_length=100, blank=True, default="Saramax",
        verbose_name="Sayt nomi (SEO title)"
    )
    site_description = models.TextField(
        blank=True, default="",
        verbose_name="Sayt tavsifi (SEO meta description)"
    )
    og_image = models.ImageField(
        upload_to="settings/og/",
        blank=True, null=True,
        verbose_name="OG rasm (ijtimoiy tarmoqlar uchun)"
    )

    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Sayt sozlamalari"
        verbose_name_plural = "Sayt sozlamalari"

    def __str__(self):
        return "Sayt sozlamalari"

    def save(self, *args, **kwargs):
        # Faqat bitta yozuv bo'lishi uchun
        self.pk = 1
        super().save(*args, **kwargs)

    @classmethod
    def get_settings(cls):
        obj, _ = cls.objects.get_or_create(pk=1)
        return obj


class Banner(models.Model):
    """
    Bosh sahifa hero banner / slider elementlari.
    """
    title = models.CharField(max_length=200, verbose_name="Sarlavha")
    subtitle = models.CharField(
        max_length=300, blank=True, default="",
        verbose_name="Pastki sarlavha (ixtiyoriy)"
    )
    button_text = models.CharField(
        max_length=50, blank=True, default="",
        verbose_name="Tugma matni",
        help_text="Masalan: Katalogni ko'rish"
    )
    button_url = models.CharField(
        max_length=200, blank=True, default="",
        verbose_name="Tugma havolasi",
        help_text="Masalan: /catalog yoki https://..."
    )
    image = models.ImageField(
        upload_to="banners/",
        verbose_name="Banner rasmi"
    )
    is_active = models.BooleanField(default=True, verbose_name="Faol")
    order = models.PositiveSmallIntegerField(default=0, verbose_name="Tartib raqami")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Banner"
        verbose_name_plural = "Bannerlar"
        ordering = ["order", "-created_at"]

    def __str__(self):
        return self.title