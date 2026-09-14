import os
import django
import requests
import re

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from django.contrib.auth import get_user_model
from rest_framework.authtoken.models import Token

User = get_user_model()
user = User.objects.first()
token, _ = Token.objects.get_or_create(user=user)

url = 'http://127.0.0.1:8000/api/addresses' # Without slash
headers = {
    'Authorization': f'Token {token.key}',
    'Content-Type': 'application/json'
}
data = {
    "region": "tashkent_city",
    "city": "Toshkent",
    "street": "Amir Temur",
    "house_number": "12",
    "apartment": "1",
    "full_address": "Toshkent Amir Temur 12",
    "is_default": False
}

try:
    response = requests.post(url, headers=headers, json=data, allow_redirects=False)
    print(f"Status Code: {response.status_code}")
    if response.status_code == 301:
        print("Redirect Location:", response.headers.get('Location'))
    elif response.status_code == 500:
        match = re.search(r'<title>(.*?)</title>', response.text, re.IGNORECASE | re.DOTALL)
        print("Exception:", match.group(1).strip() if match else "Unknown Error")
    else:
        print("Response:", response.text)
except Exception as e:
    print(f"Request failed: {e}")
