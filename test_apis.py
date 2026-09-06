import requests
import json

BASE_URL = "http://127.0.0.1:8000/api"
TOKEN = None
PRODUCT_SLUG = "akfa-thermo-eshik"
COLOR_ID = 1
PRODUCT_ID = 1
ADDRESS_ID = 1

def print_result(name, res):
    status = "[OK]" if res.status_code in [200, 201] else f"[X] XATO ({res.status_code})"
    print(f"{name:35} | {status}")
    if res.status_code not in [200, 201]:
        print(f"Xato xabari: {res.text}")
    return res.status_code in [200, 201]

def run_tests():
    global TOKEN
    print("--- 1. OCHIQ API'LAR ---")
    
    res = requests.get(f"{BASE_URL}/site-settings/")
    print_result("Sayt sozlamalari", res)
    
    res = requests.get(f"{BASE_URL}/banners/")
    print_result("Bannerlar", res)

    res = requests.get(f"{BASE_URL}/categories/")
    print_result("Kategoriyalar ro'yxati", res)

    res = requests.get(f"{BASE_URL}/products/")
    print_result("Mahsulotlar ro'yxati", res)

    res = requests.get(f"{BASE_URL}/products/{PRODUCT_SLUG}/")
    print_result("Mahsulot detali", res)

    print("\n--- 2. NARX HISOBLASH API ---")
    payload = {
        "width_mm": 1500,
        "height_mm": 2000,
        "color_id": COLOR_ID
    }
    res = requests.post(f"{BASE_URL}/products/{PRODUCT_SLUG}/calculate_price/", json=payload)
    print_result("Narx hisoblash", res)
    if res.status_code == 200:
        print(f"   -> Hisoblangan narx: {res.json().get('calculated_price')} UZS")

    print("\n--- 3. AUTENTIFIKATSIYA ---")
    login_data = {
        "phone_number": "+998901112233",
        "password": "password123"
    }
    res = requests.post(f"{BASE_URL}/auth/login/", json=login_data)
    is_ok = print_result("Login (Token olish)", res)
    if is_ok:
        TOKEN = res.json().get("token")
        print(f"   -> Token olindi: {TOKEN[:10]}...")

    if not TOKEN:
        print("Token olinmadi, qolgan testlar bekor qilindi.")
        return

    headers = {"Authorization": f"Token {TOKEN}"}

    print("\n--- 4. HIMOYALANGAN API'LAR ---")
    res = requests.get(f"{BASE_URL}/auth/profile/", headers=headers)
    print_result("Profilni ko'rish", res)

    res = requests.get(f"{BASE_URL}/addresses/", headers=headers)
    print_result("Manzillar ro'yxati", res)
    if res.status_code == 200:
        data = res.json()
        results = data.get('results', data) if isinstance(data, dict) else data
        if results:
            global ADDRESS_ID
            ADDRESS_ID = results[0]['id']

    print("\n--- 5. SAVAT VA BUYURTMA ---")
    cart_item_data = {
        "product_id": PRODUCT_ID,
        "width_mm": 1500,
        "height_mm": 2000,
        "quantity": 2,
        "color_id": COLOR_ID
    }
    res = requests.post(f"{BASE_URL}/cart/add/", json=cart_item_data, headers=headers)
    print_result("Savatga qo'shish", res)

    res = requests.get(f"{BASE_URL}/cart/", headers=headers)
    print_result("Savatni ko'rish", res)
    
    if res.status_code == 200:
        cart_data = res.json()
        print(f"   -> Savat jami summasi: {cart_data.get('total_amount')} UZS")

    order_data = {
        "address_id": ADDRESS_ID,
        "notes": "Test orqali buyurtma berildi"
    }
    res = requests.post(f"{BASE_URL}/orders/", json=order_data, headers=headers)
    is_order_ok = print_result("Buyurtma rasmiylashtirish", res)
    
    if is_order_ok:
        print(f"   -> Buyurtma raqami: {res.json().get('order_number')}")
    
    res = requests.get(f"{BASE_URL}/orders/", headers=headers)
    print_result("Buyurtmalar ro'yxati", res)

if __name__ == "__main__":
    run_tests()
