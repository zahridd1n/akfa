import os
import random
from django.core.management.base import BaseCommand
from django.core.files.uploadedfile import SimpleUploadedFile
from django.conf import settings
from main.models import (
    CustomUser, Category, Product, ProductColor, ProductImage,
    SiteSettings, Banner, Address
)

class Command(BaseCommand):
    help = 'Bazani test ma\'lumotlari bilan to\'ldirish'

    def create_dummy_image(self, name="dummy.jpg"):
        """Oddiy test rasmini yaratish"""
        # Minimalistic 1x1 pixel JPEG
        image_content = b'\xff\xd8\xff\xe0\x00\x10JFIF\x00\x01\x01\x01\x00H\x00H\x00\x00\xff\xdb\x00C\x00\x03\x02\x02\x02\x02\x02\x03\x02\x02\x02\x03\x03\x03\x03\x04\x06\x04\x04\x04\x04\x04\x08\x06\x06\x05\x06\t\x08\n\n\t\x08\t\t\n\x0c\x0f\x0c\n\x0b\x0e\x0b\t\t\r\x11\r\x0e\x0f\x10\x10\x11\x10\n\x0c\x12\x13\x12\x10\x13\x0f\x10\x10\x10\xff\xc0\x00\x0b\x08\x00\x01\x00\x01\x01\x01\x11\x00\xff\xc4\x00\x14\x00\x01\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x03\xff\xc4\x00\x14\x10\x01\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\xff\xda\x00\x08\x01\x01\x00\x00?\x00\xfd\xfc'
        return SimpleUploadedFile(name=name, content=image_content, content_type='image/jpeg')

    def handle(self, *args, **kwargs):
        self.stdout.write('Ma\'lumotlar yaratish boshlandi...')

        # 1. SiteSettings
        self.stdout.write('SiteSettings qo\'shilmoqda...')
        site_settings, _ = SiteSettings.objects.get_or_create(pk=1)
        site_settings.phone_main = "+998712001122"
        site_settings.phone_whatsapp = "+998901234567"
        site_settings.email = "info@akfa-saramax.uz"
        site_settings.address = "Toshkent sh., Yunusobod tumani, 19-kvartal, 12-uy"
        site_settings.work_hours = "Du-Sh 09:00 dan 18:00 gacha"
        site_settings.telegram_url = "https://t.me/akfagroup"
        site_settings.instagram_url = "https://instagram.com/akfa"
        site_settings.footer_about = "AKFA - O'zbekistondagi eng yirik eshik va rom ishlab chiqaruvchi kompaniya."
        site_settings.footer_copyright = "© 2024 Saramax. Barcha huquqlar himoyalangan."
        site_settings.site_title = "Saramax - AKFA eshik va romlari"
        site_settings.save()

        # 2. Banners
        self.stdout.write('Bannerlar qo\'shilmoqda...')
        Banner.objects.all().delete()
        Banner.objects.create(
            title="Zamonaviy AKFA Eshiklari",
            subtitle="Uyingiz uchun ajoyib yechim",
            button_text="Katalogni ko'rish",
            button_url="/catalog",
            image=self.create_dummy_image('banner1.jpg'),
            order=1
        )
        Banner.objects.create(
            title="Yozgi chegirmalar",
            subtitle="Derazalar uchun 20% gacha chegirma",
            button_text="Batafsil",
            button_url="/offers",
            image=self.create_dummy_image('banner2.jpg'),
            order=2
        )

        # 3. Categories
        self.stdout.write('Kategoriyalar qo\'shilmoqda...')
        Category.objects.all().delete()
        cat_doors = Category.objects.create(name="Eshiklar", slug="eshiklar", order=1)
        cat_windows = Category.objects.create(name="Derazalar", slug="derazalar", order=2)
        cat_balcony = Category.objects.create(name="Balkon romlari", slug="balkon-romlari", order=3)

        # 4. Products
        self.stdout.write('Mahsulotlar qo\'shilmoqda...')
        Product.objects.all().delete()
        products_data = [
            {
                "category": cat_doors, "name": "AKFA Thermo Eshik", "slug": "akfa-thermo-eshik",
                "base_price": 1200000, "material": "aluminium", "design_style": "modern",
                "profile_thickness": "70mm", "max_glass": "Ikki qavatli", "sound_insulation": "Yuqori",
                "badge": "new"
            },
            {
                "category": cat_doors, "name": "AKFA Classic Eshik", "slug": "akfa-classic-eshik",
                "base_price": 950000, "material": "pvc", "design_style": "classic",
                "profile_thickness": "60mm", "max_glass": "Bir qavatli", "sound_insulation": "O'rta",
                "badge": "sale"
            },
            {
                "category": cat_windows, "name": "AKFA Panorama Deraza", "slug": "akfa-panorama-deraza",
                "base_price": 1500000, "material": "aluminium", "design_style": "modern",
                "profile_thickness": "80mm", "max_glass": "Uch qavatli", "sound_insulation": "Maksimal",
                "badge": "warm"
            },
            {
                "category": cat_windows, "name": "AKFA Eco Deraza", "slug": "akfa-eco-deraza",
                "base_price": 800000, "material": "pvc", "design_style": "minimalist",
                "profile_thickness": "52mm", "max_glass": "Bir qavatli", "sound_insulation": "O'rta"
            }
        ]

        colors_data = [
            {"name": "Oq", "hex_code": "#FFFFFF", "price_modifier": 0},
            {"name": "Jigarrang (Yong'oq)", "hex_code": "#5C4033", "price_modifier": 150000},
            {"name": "Antrasit", "hex_code": "#383E42", "price_modifier": 200000}
        ]

        for p_data in products_data:
            product = Product.objects.create(
                category=p_data["category"],
                name=p_data["name"],
                slug=p_data["slug"],
                base_price=p_data["base_price"],
                material=p_data.get("material"),
                design_style=p_data.get("design_style"),
                profile_thickness=p_data.get("profile_thickness"),
                max_glass=p_data.get("max_glass", ""),
                sound_insulation=p_data.get("sound_insulation"),
                badge=p_data.get("badge", ""),
                description=f"{p_data['name']} - uyingiz uchun eng yaxshi tanlov."
            )
            
            # Add images
            ProductImage.objects.create(product=product, image=self.create_dummy_image(f"{p_data['slug']}_main.jpg"), is_main=True)
            ProductImage.objects.create(product=product, image=self.create_dummy_image(f"{p_data['slug']}_1.jpg"), is_main=False)
            
            # Add colors
            for c_data in colors_data:
                ProductColor.objects.create(
                    product=product,
                    name=c_data["name"],
                    hex_code=c_data["hex_code"],
                    price_modifier=c_data["price_modifier"]
                )

        # 5. Dummy User & Address
        self.stdout.write('Test foydalanuvchi va manzil qo\'shilmoqda...')
        user, created = CustomUser.objects.get_or_create(phone_number="+998901112233")
        if created:
            user.set_password("password123")
            user.full_name = "Test Mijoz"
            user.save()
            
        Address.objects.get_or_create(
            user=user,
            region="tashkent_city",
            city="Toshkent",
            street="Amir Temur",
            house_number="15",
            full_address="Toshkent sh., Amir Temur ko'chasi, 15-uy",
            is_default=True
        )

        self.stdout.write(self.style.SUCCESS('Bazaga test ma\'lumotlari muvaffaqiyatli qo\'shildi!'))
        self.stdout.write('Test user logini: +998901112233')
        self.stdout.write('Test user paroli: password123')
