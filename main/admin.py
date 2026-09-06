from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.utils.html import format_html
from .models import (
    CustomUser, Address,
    Category, Product, ProductImage, ProductColor,
    Cart, CartItem,
    Order, OrderItem,
    SiteSettings, Banner,
)


@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    model = CustomUser
    list_display = ["phone_number", "full_name", "role", "is_active", "created_at"]
    list_filter = ["role", "is_active"]
    search_fields = ["phone_number", "full_name"]
    ordering = ["-created_at"]
    fieldsets = (
        (None, {"fields": ("phone_number", "password")}),
        ("Shaxsiy malumot", {"fields": ("full_name", "role")}),
        ("Ruxsatlar", {"fields": ("is_active", "is_staff", "is_superuser", "groups", "user_permissions")}),
        ("Sanalar", {"fields": ("last_login",)}),
    )
    add_fieldsets = (
        (None, {
            "classes": ("wide",),
            "fields": ("phone_number", "full_name", "role", "password1", "password2"),
        }),
    )


@admin.register(Address)
class AddressAdmin(admin.ModelAdmin):
    list_display = ["user", "region_display", "city", "street", "is_default"]
    list_filter = ["region", "is_default"]
    search_fields = ["user__phone_number", "user__full_name", "city", "street"]

    def region_display(self, obj):
        return obj.get_region_display()
    region_display.short_description = "Viloyat"


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ["name", "slug", "order", "is_active"]
    list_editable = ["order", "is_active"]
    prepopulated_fields = {"slug": ("name",)}


class ProductImageInline(admin.TabularInline):
    model = ProductImage
    extra = 1
    readonly_fields = ["image_preview"]

    def image_preview(self, obj):
        if obj.image:
            return format_html('<img src="{}" style="height:60px;"/>', obj.image.url)
        return "-"
    image_preview.short_description = "Korinish"


class ProductColorInline(admin.TabularInline):
    model = ProductColor
    extra = 1


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ["name", "category", "material", "base_price", "price_type", "status", "is_active"]
    list_filter = ["category", "material", "status", "is_active", "price_type"]
    list_editable = ["base_price", "status", "is_active"]
    search_fields = ["name", "description"]
    prepopulated_fields = {"slug": ("name",)}
    inlines = [ProductImageInline, ProductColorInline]
    fieldsets = (
        ("Asosiy", {"fields": ("name", "slug", "category", "description")}),
        ("Klassifikatsiya", {"fields": ("material", "design_style", "badge", "status", "is_active")}),
        ("Narx", {"fields": ("base_price", "price_type")}),
        ("Texnik xususiyatlar", {
            "fields": ("profile_thickness", "max_glass", "sound_insulation", "climate_resistance", "delivery_info"),
            "classes": ("collapse",),
        }),
    )


class CartItemInline(admin.TabularInline):
    model = CartItem
    extra = 0


@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    list_display = ["user", "total_items", "total_amount", "updated_at"]
    readonly_fields = ["total_items", "total_amount"]
    inlines = [CartItemInline]


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0
    readonly_fields = ["sqm", "total_price"]


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ["order_number", "user", "status", "total_amount", "created_at"]
    list_filter = ["status", "created_at"]
    list_editable = ["status"]
    search_fields = ["order_number", "user__phone_number", "user__full_name"]
    readonly_fields = ["order_number", "subtotal", "total_amount"]
    inlines = [OrderItemInline]
    fieldsets = (
        ("Buyurtma", {"fields": ("order_number", "user", "delivery_address", "status")}),
        ("Moliya", {"fields": ("subtotal", "delivery_fee", "total_amount")}),
        ("Qoshimcha", {"fields": ("notes",)}),
    )


# ─────────────────────────────────────────
# Sayt sozlamalari
# ─────────────────────────────────────────
@admin.register(SiteSettings)
class SiteSettingsAdmin(admin.ModelAdmin):
    """Sayt sozlamalari - faqat bitta yozuv"""

    fieldsets = (
        ("Kontakt ma'lumotlari", {
            "fields": ("phone_main", "phone_whatsapp", "phone_extra", "email", "address", "work_hours")
        }),
        ("Ijtimoiy tarmoqlar", {
            "fields": ("telegram_url", "instagram_url", "facebook_url", "youtube_url")
        }),
        ("Footer", {
            "fields": ("footer_about", "footer_copyright")
        }),
        ("SEO", {
            "fields": ("site_title", "site_description", "og_image")
        }),
    )
    readonly_fields = ["updated_at"]

    def has_add_permission(self, request):
        # Faqat bitta yozuv bo'lishi uchun
        return not SiteSettings.objects.exists()

    def has_delete_permission(self, request, obj=None):
        return False


@admin.register(Banner)
class BannerAdmin(admin.ModelAdmin):
    list_display = ["title", "is_active", "order", "preview", "created_at"]
    list_editable = ["is_active", "order"]
    list_filter = ["is_active"]
    search_fields = ["title", "subtitle"]

    def preview(self, obj):
        if obj.image:
            return format_html('<img src="{}" style="height:40px; border-radius:4px;">', obj.image.url)
        return "-"
    preview.short_description = "Ko'rinish"

