# Serverda (Ubuntu VPS) Loyihani O'rnatish Qo'llanmasi

Loyiha monorepo (Django Backend + Vue 3 Frontend) shaklida bo'lgani uchun serverda bitta papkada (`/var/www/akfa`) joylashadi va **Nginx** barcha so'rovlarni avtomatik boshqaradi.

---

## 1. Serverga kerakli dasturlarni o'rnatish
Serverga SSH orqali ulaning va quyidagi buyruqlarni bajaring:

```bash
# Tizimni yangilash
sudo apt update && sudo apt upgrade -y

# Python, Git, Nginx va muhim kutubxonalar
sudo apt install -y python3 python3-pip python3-venv git nginx curl libpq-dev

# Node.js (v20 LTS) va npm o'rnatish
curl -fsSL https://deb.nodesource.com/setup_20.x | sudo -E bash -
sudo apt install -y nodejs
```

---

## 2. Loyihani GitHub'dan serverga yuklash (Clone)

```bash
# Loyiha papkasini yaratish va unga o'tish
sudo mkdir -p /var/www
cd /var/www

# GitHub'dagi repository'ingizni clone qiling:
sudo git clone <GITHUB_REPO_URL> akfa
cd akfa

# Papka huquqlarini to'g'irlash
sudo chown -R $USER:$USER /var/www/akfa
sudo chmod -R 755 /var/www/akfa
```

---

## 3. Backend'ni sozlash (Django + Gunicorn)

```bash
cd /var/www/akfa

# Python virtual muhit (venv) yaratish va faollashtirish
python3 -m venv venv
source venv/bin/activate

# Kerakli kutubxonalarni o'rnatish
pip install -r requirements.txt

# Migratsiyalarni amalga oshirish
python manage.py migrate

# Superadmin foydalanuvchi yaratish (Dashboardga kirish uchun)
python manage.py createsuperuser

# Statik fayllarni yig'ish
python manage.py collectstatic --noinput
```

---

## 4. Frontend'ni build qilish (Vue 3)

```bash
cd /var/www/akfa/frontend

# Paketlarni o'rnatish va ishlab chiqarish (production) uchun build qilish
npm install
npm run build
```
*(Bu buyruq `/var/www/akfa/frontend/dist` papkasini hosil qiladi)*

---

## 5. Gunicorn Service'ni sozlash (Systemd)

Gunicorn xizmati server yonganda yoki qayta ishga tushganda Django'ni avtomatik fonda ishlatib turadi:

```bash
# Konfiguratsiya faylini tizimga nusxalash
sudo cp /var/www/akfa/deploy/akfa.service /etc/systemd/system/

# Tizimni yangilash va xizmatni yoqish
sudo systemctl daemon-reload
sudo systemctl start akfa
sudo systemctl enable akfa

# Holatini tekshirish
sudo systemctl status akfa
```

---

## 6. Nginx'ni sozlash

```bash
# Nginx konfiguratsiyasini nusxalash
sudo cp /var/www/akfa/deploy/nginx.conf /etc/nginx/sites-available/akfa

# Faylni tahrirlab o'z domeningizni yoki IP'ni yozing:
sudo nano /etc/nginx/sites-available/akfa
# (server_name qatoriga domen yoki server IP ni yozing)

# Saytni faollashtirish (symlink)
sudo ln -s /etc/nginx/sites-available/akfa /etc/nginx/sites-enabled/
sudo rm -f /etc/nginx/sites-enabled/default

# Nginx konfiguratsiyasini tekshirish va qayta yuklash
sudo nginx -t
sudo systemctl reload nginx
```

---

## 7. Bepul SSL (HTTPS) Sertifikatini o'rnatish (Ixtiyoriy, domen bo'lsa)

```bash
sudo apt install -y certbot python3-certbot-nginx
sudo certbot --nginx -d your_domain.uz -d www.your_domain.uz
```

---

## 8. Keyinchalik yangi kod yuklaganda (1 ta buyruq bilan yangilash)

Kodlarga o'zgartirish kiritib GitHub'ga push qilganingizdan keyin, serverda faqat quyidagi buyruqni ishga tushirasiz:

```bash
bash /var/www/akfa/deploy/deploy.sh
```
Bu skript avtomatik:
1. `git pull` qiladi
2. `pip install` va `migrate` qiladi
3. Frontendni yangitdan `npm run build` qiladi
4. Gunicorn va Nginx'ni qayta yuklaydi!
