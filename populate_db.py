import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from main.models import Category, Product, ProductColor, ProductImage

def run():
    print("Populating database with fake data...")
    
    # 1. Categories
    categories_data = [
        {'name': 'Deraza', 'slug': 'deraza'},
        {'name': 'Eshik', 'slug': 'eshik'},
        {'name': 'Fasad', 'slug': 'fasad'},
    ]
    
    categories = {}
    for data in categories_data:
        cat, created = Category.objects.get_or_create(slug=data['slug'], defaults={'name': data['name']})
        categories[data['slug']] = cat

    # 2. Products
    products_data = [
        {
            'category': categories['deraza'],
            'name': 'Thermo 78',
            'slug': 'thermo-78',
            'description': 'Premium darajadagi issiqlik izolyatsiyasi.',
            'base_price': 1500000.00,
            'material': 'aluminium',
            'status': 'active',
            'badge': 'new',
            'profile_thickness': '78 mm', 
            'sound_insulation': '50 dB', 
            'climate_resistance': 'Sovuq iqlim',
        },
        {
            'category': categories['deraza'],
            'name': 'Engelberg 76',
            'slug': 'engelberg-76',
            'description': 'Yuqori sifatli PVX deraza.',
            'base_price': 1200000.00,
            'material': 'pvc',
            'status': 'active',
            'badge': 'sale',
            'profile_thickness': '76 mm', 
            'sound_insulation': '45 dB', 
            'climate_resistance': "O'rta iqlim",
        },
        {
            'category': categories['eshik'],
            'name': 'Imzo Premium Eshik',
            'slug': 'imzo-premium-eshik',
            'description': 'Zamonaviy dizayndagi alyuminiy eshik.',
            'base_price': 2500000.00,
            'material': 'aluminium',
            'status': 'active',
            'badge': '',
            'profile_thickness': '70 mm',
            'sound_insulation': '',
            'climate_resistance': '',
        },
        {
            'category': categories['eshik'],
            'name': 'Lumina MDF Eshik',
            'slug': 'lumina-mdf-eshik',
            'description': 'Ichki xonalar uchun qulay eshik.',
            'base_price': 800000.00,
            'material': 'wood',
            'status': 'sale',
            'badge': 'sale',
            'profile_thickness': '',
            'sound_insulation': '',
            'climate_resistance': '',
        },
    ]

    import urllib.request
    from django.core.files.base import ContentFile
    from main.models import Banner

    def download_image(url, filename):
        try:
            response = urllib.request.urlopen(url)
            return ContentFile(response.read(), name=filename)
        except Exception as e:
            print(f"Failed to download image from {url}: {e}")
            return None

    # Add a banner
    banner_img = download_image("https://picsum.photos/1920/1080?seed=akfa_banner", "banner.jpg")
    if banner_img:
        Banner.objects.get_or_create(
            title="Uyingiz uchun zamonaviy AKFA eshik va romlar",
            defaults={
                "subtitle": "Premium sifat",
                "button_text": "Katalogni ko'rish",
                "button_url": "/catalog",
                "image": banner_img,
                "is_active": True,
            }
        )

    for i, p_data in enumerate(products_data):
        product, created = Product.objects.get_or_create(
            slug=p_data['slug'],
            defaults={
                'category': p_data['category'],
                'name': p_data['name'],
                'description': p_data['description'],
                'base_price': p_data['base_price'],
                'material': p_data['material'],
                'status': p_data['status'],
                'badge': p_data['badge'],
                'profile_thickness': p_data['profile_thickness'],
                'sound_insulation': p_data['sound_insulation'],
                'climate_resistance': p_data['climate_resistance'],
            }
        )
        
        if created:
            # 3. Colors
            ProductColor.objects.get_or_create(product=product, name='Oq', defaults={'hex_code': '#FFFFFF', 'price_modifier': 0.00})
            ProductColor.objects.get_or_create(product=product, name='Qora', defaults={'hex_code': '#000000', 'price_modifier': 50000.00})
            ProductColor.objects.get_or_create(product=product, name="Yog'och tekstura", defaults={'hex_code': '#8B5A2B', 'price_modifier': 150000.00})
            
        # 4. Image
        if not product.images.exists():
            img_file = download_image(f"https://picsum.photos/800/600?seed=akfa_prod_{i}", f"{product.slug}.jpg")
            if img_file:
                ProductImage.objects.create(product=product, image=img_file, is_main=True)
            print(f"Added image to product {product.name}")

    print("Done!")

if __name__ == "__main__":
    run()
