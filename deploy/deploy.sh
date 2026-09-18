#!/usr/bin/env bash
# ==============================================================================
# Avtomatik yangilash va deploy qilish skripti (Serverda ishlatiladi)
# Ishga tushirish: bash /var/www/akfa/deploy/deploy.sh
# ==============================================================================

set -e

echo "🚀 [1/5] Yangi kodlarni GitHub'dan yuklab olish..."
cd /var/www/akfa
git pull origin main

echo "🐍 [2/5] Backend: Python paketlarni o'rnatish..."
source /var/www/akfa/venv/bin/activate
pip install -r requirements.txt --no-cache-dir

echo "📦 [3/5] Backend: Migratsiya va statik fayllarni yig'ish..."
python manage.py migrate --noinput
python manage.py collectstatic --noinput

echo "⚡ [4/5] Frontend: Vue 3 loyihasini build qilish..."
cd /var/www/akfa/frontend
npm install
npm run build

echo "🔄 [5/5] Xizmatlarni qayta ishga tushirish..."
sudo systemctl restart akfa
sudo systemctl reload nginx

echo "✅ Muvaffaqiyatli yakunlandi! Sayt yangilandi."
