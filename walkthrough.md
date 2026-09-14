# Saramax Frontend - Bajarilgan Ishlar

Ushbu hujjatda figma dizayni asosida Saramax loyihasining frontend qismida amalga oshirilgan ishlar keltirilgan. 

## 🛠 Nimalar qilindi?

### 1. Asosiy soatlamalar va tuzilma
- **Vue 3 + Vite + Tailwind CSS** asosida loyiha yaratildi.
- API so'rovlari uchun **Axios** sozlandi, Token auth qilingan.
- Global holatni boshqarish uchun **Pinia** (Auth, Cart, Alert) o'rnatildi.
- CSS dagi `main.css` ichida loyiha brend ranglari (Figma dan) va dizayn tizimi (buttons, badges, inputs, cards) e'lon qilindi.

### 2. Foydalanuvchi qismi (Client Portal)
- **Bosh sahifa (Home)** - Banner, Kategoriyalar, Ommabop mahsulotlar va boshlang'ich ma'lumotlar, interaktiv Narx kalkulyatori qismi.
- **Katalog sahifasi (Catalog)** - Kategoriya, material va holat bo'yicha filterlar. Qidiruv, narx/nom bo'yicha saralash, ro'yxat/grid ko'rinish va paginatsiya.
- **Mahsulot sahifasi (Product Detail)** - Mahsulot suratlari galereyasi. Mahsulotning ranglarini tanlash va o'lchamlarini (bo'yi, eni) kiritish orqali **dinamik narx hisoblash (Kalkulyator)**. Savatga qo'shish imkoniyati.
- **Savat (Cart)** - Savatdagi mahsulotlarni ko'rish, sonini o'zgartirish, o'chirish va jami to'lovni hisoblash.
- **Rasmiylashtirish (Checkout)** - Yetkazib berish manzilini tanlash, yangi manzil qo'shish, buyurtmaga izoh yozish va buyurtma berish.
- **Profil sahifasi (Profile)** - 3 ta bo'limdan iborat: shaxsiy ma'lumotlarni o'zgartirish, buyurtmalar tarixi va manzillarni boshqarish.

### 3. Admin Panel qismi
- **Dashboard** - Jami savdo KPI lari, Chart.js yordamida savdo grafikasi, buyurtmalar holati bo'yicha statistika.
- **Buyurtmalar (Orders)** - Barcha buyurtmalarni ko'rish, qidirish, holatini o'zgartirish (masalan: "Tayyorlanmoqda", "Yo'lda").
- **Mahsulotlar (Products)** - Mahsulotlarni ro'yxati, kategoriya va nom bo'yicha qidirish, yangi qo'shish, tahrirlash (ranglar modifikatori, texnik xususiyatlar), o'chirish.
- **Mijozlar (Customers)** - Mijozlar ro'yxati, xaridlar tarixi (orders_count) va qidiruv.
- **Hisobotlar (Reports)** - Sana oralig'ida hisobotlarni ko'rish, umumiy tushumni tekshirish, va Excel/Word shaklida yuklab olish.

### 4. Komponentlar
- **AuthModal** - Saytning istalgan joyidan (masalan, savatga qo'shmoqchi bo'lsa) login qilish (telefon + parol) yoki ro'yxatdan o'tish uchun ochiladigan interaktiv modal (SMSsiz ishlaydi, talabga binoan).
- **Navbar va Footer** - Sayt navigatsiyasi, qidiruv paneli va pastki bog'lanish ma'lumotlari.
- **ProductCard** - Takrorlanuvchi maxsus mahsulot kartasi.

## 🚀 Qanday tekshirib ko'rish mumkin?

1. Hozirda **Django backend** (`http://localhost:8000`) va **Vue frontend** (`http://localhost:3000`) ishga tushirilgan.
2. Brauzeringizda **http://localhost:3000** manziliga kiring.
3. Katalog bo'limiga o'tib maxsulotlarni ko'ring, kalkulyator orqali hisoblang va savatga qo'shib buyurtma berib ko'ring.
4. Profilingizdan yoki Admin panel (agar akkaunt admin bo'lsa `http://localhost:3000/admin`) orqali xaridlarni boshqaring.

> [!TIP]
> Frontend to'liq API larni ulab tayyorlandi. Agar dizayn (ranglar, shriftlar) yoki logikada o'zgartirilishi kerak bo'lgan joylar bo'lsa, xabar bering, albatta moslab beraman!
