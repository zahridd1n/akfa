from django.db import models
from django.utils.text import slugify


class Category(models.Model):
    name = models.CharField(max_length=100, verbose_name="Nomi")
    slug = models.SlugField(max_length=120, unique=True, verbose_name="Slug")
    icon = models.ImageField(
        upload_to="categories/icons/", blank=True, null=True, verbose_name="Ikonka"
    )
    order = models.PositiveSmallIntegerField(default=0, verbose_name="Tartib")
    is_active = models.BooleanField(default=True, verbose_name="Faol")

    class Meta:
        verbose_name = "Kategoriya"
        verbose_name_plural = "Kategoriyalar"
        ordering = ["order", "name"]

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)


class Product(models.Model):
    class PriceType(models.TextChoices):
        PER_SQM = "per_sqm", "Kv.m uchun"
        FIXED = "fixed", "Qat'iy narx"

    class Status(models.TextChoices):
        ACTIVE = "active", "Faol"
        SALE = "sale", "Aksiya"
        OUT_OF_STOCK = "out_of_stock", "Mavjud emas"

    class Badge(models.TextChoices):
        NEW = "new", "Yangi"
        WARM = "warm", "Iliq-issiq"
        SALE = "sale", "Sotuvda"

    class Material(models.TextChoices):
        ALUMINIUM = "aluminium", "Alyuminiy"
        PVC = "pvc", "PVX (Plastik)"
        WOOD = "wood", "Yog''och"
        STEEL = "steel", "Po''lat"

    class DesignStyle(models.TextChoices):
        MODERN = "modern", "Zamonaviy"
        CLASSIC = "classic", "Klassik"
        MINIMALIST = "minimalist", "Minimalist"

    name = models.CharField(max_length=200, verbose_name="Mahsulot nomi")
    slug = models.SlugField(max_length=220, unique=True, verbose_name="Slug")
    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        null=True,
        related_name="products",
        verbose_name="Kategoriya",
    )
    description = models.TextField(blank=True, verbose_name="Tavsif")

    # Klassifikatsiya
    material = models.CharField(
        max_length=20, choices=Material.choices, blank=True, verbose_name="Material"
    )
    design_style = models.CharField(
        max_length=20, choices=DesignStyle.choices, blank=True, verbose_name="Dizayn uslubi"
    )

    # Narx
    base_price = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        verbose_name="Asosiy narx (UZS)",
        help_text="Kv.m uchun narx yoki qat'iy narx",
    )
    price_type = models.CharField(
        max_length=10,
        choices=PriceType.choices,
        default=PriceType.PER_SQM,
        verbose_name="Narx turi",
    )

    # Ko'rinish
    badge = models.CharField(
        max_length=10, choices=Badge.choices, blank=True, default="", verbose_name="Badge (yorliq)"
    )
    status = models.CharField(
        max_length=15,
        choices=Status.choices,
        default=Status.ACTIVE,
        verbose_name="Holat",
    )
    is_active = models.BooleanField(default=True, verbose_name="Aktiv")

    # Texnik xususiyatlar
    profile_thickness = models.CharField(
        max_length=20, blank=True, verbose_name="Profil qalinligi (mm)"
    )
    max_glass = models.CharField(max_length=20, blank=True, verbose_name="Max shisha (mm)")
    sound_insulation = models.CharField(
        max_length=20, blank=True, verbose_name="Tovush izolyatsiyasi (dB)"
    )
    climate_resistance = models.TextField(blank=True, verbose_name="Iqlim chidamliligi")
    delivery_info = models.TextField(blank=True, verbose_name="Yetkazib berish ma''lumoti")

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Mahsulot"
        verbose_name_plural = "Mahsulotlar"
        ordering = ["-created_at"]

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def calculate_price(self, width_mm: int, height_mm: int, color=None) -> float:
        """
        Narxni hisoblash:
        - per_sqm: effective_price * (width_mm/1000) * (height_mm/1000)
        - fixed: effective_price
        """
        if color:
            if hasattr(color, "get_effective_price"):
                effective_price = color.get_effective_price()
            elif getattr(color, "price", None) is not None:
                effective_price = float(color.price)
            else:
                effective_price = float(self.base_price) + float(getattr(color, "price_modifier", 0) or 0)
        else:
            effective_price = float(self.base_price)

        if self.price_type == self.PriceType.PER_SQM:
            return effective_price * (width_mm / 1000) * (height_mm / 1000)
        return effective_price


class ProductImage(models.Model):
    product = models.ForeignKey(
        Product, on_delete=models.CASCADE, related_name="images", verbose_name="Mahsulot"
    )
    image = models.ImageField(upload_to="products/images/", verbose_name="Rasm")
    is_main = models.BooleanField(default=False, verbose_name="Asosiy rasm")
    order = models.PositiveSmallIntegerField(default=0, verbose_name="Tartib")

    class Meta:
        verbose_name = "Mahsulot rasmi"
        verbose_name_plural = "Mahsulot rasmlari"
        ordering = ["-is_main", "order"]

    def __str__(self):
        return f"{self.product.name} - rasm {self.order}"


class ProductColor(models.Model):
    product = models.ForeignKey(
        Product, on_delete=models.CASCADE, related_name="colors", verbose_name="Mahsulot"
    )
    name = models.CharField(max_length=60, verbose_name="Rang nomi")
    hex_code = models.CharField(
        max_length=7, blank=True, verbose_name="HEX kodi", help_text="#RRGGBB formatida"
    )
    price = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        null=True,
        blank=True,
        default=None,
        verbose_name="Rang narxi (UZS)",
        help_text="Ushbu rang uchun to'liq narx. Agar kiritilsa, mahsulot asosiy narxi o'rniga ishlatiladi",
    )
    price_modifier = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        default=0,
        verbose_name="Narx farqi (UZS)",
        help_text="0 = asosiy narx, musbat = qimmatroq, manfiy = arzonroq",
    )
    is_available = models.BooleanField(default=True, verbose_name="Mavjud")

    class Meta:
        verbose_name = "Mahsulot rangi"
        verbose_name_plural = "Mahsulot ranglari"
        ordering = ["name"]

    def __str__(self):
        return f"{self.product.name} — {self.name}"

    def get_effective_price(self) -> float:
        """Ushbu rang uchun amaldagi narx (UZS)"""
        if self.price is not None:
            return float(self.price)
        base = float(self.product.base_price) if self.product else 0
        return base + float(self.price_modifier or 0)

    def save(self, *args, **kwargs):
        # price va price_modifier o'rtasidagi ikki tomonlama sinxronlik
        if self.price is not None and self.product_id:
            try:
                base = float(self.product.base_price)
                self.price_modifier = float(self.price) - base
            except Exception:
                pass
        elif self.price is None and self.product_id:
            try:
                base = float(self.product.base_price)
                self.price = base + float(self.price_modifier or 0)
            except Exception:
                pass
        super().save(*args, **kwargs)
