from rest_framework import serializers
from ..models import SiteSettings, Banner, ContactMessage, About


class SiteSettingsSerializer(serializers.ModelSerializer):
    class Meta:
        model = SiteSettings
        fields = [
            "id",
            "phone_main", "phone_whatsapp", "phone_extra",
            "email", "address", "map_location", "work_hours",
            "telegram_url", "instagram_url", "facebook_url", "youtube_url",
            "footer_about", "footer_copyright",
            "site_title", "site_description", "og_image",
            "updated_at"
        ]
        read_only_fields = ["updated_at"]


class AboutSerializer(serializers.ModelSerializer):
    class Meta:
        model = About
        fields = [
            "id",
            "title",
            "subtitle",
            "content",
            "image",
            "experience_years",
            "stat_1_number",
            "stat_1_label",
            "stat_2_number",
            "stat_2_label",
            "stat_3_number",
            "stat_3_label",
            "stat_4_number",
            "stat_4_label",
            "mission",
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


class ContactMessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ContactMessage
        fields = ["id", "name", "phone", "message", "is_read", "created_at"]
        read_only_fields = ["id", "is_read", "created_at"]