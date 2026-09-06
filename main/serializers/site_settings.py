from rest_framework import serializers
from ..models import SiteSettings, Banner


class SiteSettingsSerializer(serializers.ModelSerializer):
    class Meta:
        model = SiteSettings
        fields = [
            "phone_main", "phone_whatsapp", "phone_extra",
            "email", "address", "work_hours",
            "telegram_url", "instagram_url", "facebook_url", "youtube_url",
            "footer_about", "footer_copyright",
            "site_title", "site_description", "og_image",
            "updated_at",
        ]
        read_only_fields = ["updated_at"]


class BannerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Banner
        fields = [
            "id", "title", "subtitle",
            "button_text", "button_url",
            "image", "is_active", "order",
        ]