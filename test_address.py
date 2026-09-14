import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from django.contrib.auth import get_user_model
from rest_framework.test import APIClient

User = get_user_model()
# Get first user
user = User.objects.first()
print(f"Testing with user: {user}")

client = APIClient()
client.force_authenticate(user=user)

data = {
    "region": "tashkent_city",
    "city": "Toshkent",
    "street": "Amir Temur",
    "house_number": "12",
    "apartment": "1",
    "full_address": "Toshkent Amir Temur 12",
    "is_default": True
}

response = client.post('/api/addresses/', data, format='json')
print(f"Status: {response.status_code}")
print(f"Response: {response.data if hasattr(response, 'data') else response.content}")
