<template>
  <!-- Soft blue background like Figma -->
  <div class="min-h-screen" style="background: #EBF3F8;">

    <!-- Page Header -->
    <div class="bg-white/80 backdrop-blur border-b border-[#C7DDEA]/60 px-4 pt-5 pb-4">
      <div class="max-w-6xl mx-auto">
        <h1 class="text-2xl font-bold text-slate-900">Savat</h1>
      </div>
    </div>

    <!-- Empty Cart -->
    <div v-if="!cartStore.loading && !cartStore.items.length" class="flex flex-col items-center justify-center py-24 px-4">
      <div class="w-24 h-24 bg-white rounded-2xl flex items-center justify-center mb-5 shadow-sm border border-[#C7DDEA]/50">
        <ShoppingCart class="w-12 h-12 text-slate-300" />
      </div>
      <h2 class="text-xl font-bold text-slate-700 mb-2">Savat bo'sh</h2>
      <p class="text-slate-400 text-sm mb-6">Hali hech narsa qo'shmadingiz.</p>
      <router-link to="/catalog" class="btn-md bg-brand-950 text-white px-8">Katalogga o'tish</router-link>
    </div>

    <!-- Loading -->
    <div v-if="cartStore.loading" class="max-w-6xl mx-auto p-4 space-y-3">
      <div v-for="i in 3" :key="i" class="skeleton h-32 rounded-xl" />
    </div>

    <!-- Cart Content -->
    <div v-if="!cartStore.loading && cartStore.items.length" class="max-w-6xl mx-auto p-4">

      <!-- Desktop: Two-column grid | Mobile: single column -->
      <div class="lg:grid lg:grid-cols-3 lg:gap-6 flex flex-col gap-4">

        <!-- LEFT: Items List (2/3 width on desktop) -->
        <div class="lg:col-span-2 space-y-3">
          <TransitionGroup name="fade">
            <div
              v-for="item in cartStore.items"
              :key="item.id"
              class="bg-white rounded-xl border border-[#C7DDEA]/50 p-3 flex gap-3 relative shadow-sm"
            >
              <!-- Product Image -->
              <div class="w-20 h-20 lg:w-24 lg:h-24 rounded-lg bg-[#EBF3F8] flex-shrink-0 flex items-center justify-center overflow-hidden">
                <img
                  :src="item.main_image || 'https://placehold.co/100/EBF3F8/94A3B8?text=Rasm'"
                  :alt="item.product_name"
                  class="max-w-full max-h-full object-contain"
                />
              </div>

              <!-- Info -->
              <div class="flex-1 min-w-0 pr-6">
                <router-link :to="`/product/${item.product_slug}`" class="text-sm font-bold text-slate-900 hover:text-brand-600 line-clamp-1 block leading-snug mb-1">
                  {{ item.product_name }}
                </router-link>

                <!-- Tags -->
                <div class="flex flex-wrap items-center gap-1.5 mb-3">
                  <span class="flex items-center gap-1 px-2 py-0.5 bg-[#EBF3F8] rounded text-[11px] text-slate-600">
                    <span class="w-2.5 h-2.5 rounded-full border border-slate-300 flex-shrink-0" :style="{ backgroundColor: item.color_hex || '#888' }" />
                    {{ item.color_name || 'Standart' }}
                  </span>
                  <span class="px-2 py-0.5 bg-[#EBF3F8] rounded text-[11px] text-slate-600">
                    {{ item.width_mm }}×{{ item.height_mm }} mm
                  </span>
                </div>

                <!-- Qty + Price -->
                <div class="flex items-center justify-between">
                  <div class="inline-flex items-center bg-[#EBF3F8] rounded-lg h-8">
                    <button @click="changeQty(item, item.quantity - 1)" :disabled="item.quantity <= 1"
                      class="w-8 h-8 flex items-center justify-center text-slate-600 hover:text-slate-900 disabled:opacity-40 text-base font-semibold">
                      −
                    </button>
                    <span class="w-8 text-center text-sm font-bold text-slate-900">{{ item.quantity }}</span>
                    <button @click="changeQty(item, item.quantity + 1)"
                      class="w-8 h-8 flex items-center justify-center text-slate-600 hover:text-slate-900 text-base font-semibold">
                      +
                    </button>
                  </div>
                  <span class="text-base font-bold text-slate-900">{{ formatPrice(item.total_price) }}</span>
                </div>
              </div>

              <!-- Delete -->
              <button @click="removeItem(item.id)" class="absolute top-3 right-3 text-slate-300 hover:text-red-500 transition-colors">
                <Trash2 class="w-4 h-4" />
              </button>
            </div>
          </TransitionGroup>

          <!-- Clear Cart -->
          <div class="flex justify-end pt-1">
            <button @click="clearCart" class="text-xs text-red-400 hover:text-red-600 transition-colors flex items-center gap-1">
              <Trash2 class="w-3.5 h-3.5" /> Savatni tozalash
            </button>
          </div>
        </div>

        <!-- RIGHT: Summary (1/3 width on desktop) -->
        <div class="lg:col-span-1">
          <div class="bg-white rounded-xl border border-[#C7DDEA]/50 p-5 shadow-sm lg:sticky lg:top-24">
            <h2 class="font-bold text-slate-900 text-base mb-5">Buyurtma xulosasi</h2>

            <div class="space-y-3 text-sm mb-5">
              <div class="flex justify-between text-slate-600">
                <span>Mahsulotlar soni</span>
                <span class="font-semibold text-slate-900">{{ cartStore.itemCount }} ta</span>
              </div>
              <div class="flex justify-between text-slate-600">
                <span>Mahsulotlar qiymati</span>
                <span class="font-semibold text-slate-900">{{ formatPrice(cartStore.subtotal) }}</span>
              </div>
              <div class="flex justify-between text-slate-600">
                <span>Yetkazib berish</span>
                <span class="font-semibold text-emerald-600">Bepul</span>
              </div>
            </div>

            <div class="h-px bg-[#C7DDEA]/40 mb-5" />

            <div class="flex justify-between items-end mb-5">
              <span class="text-sm font-bold text-slate-900">Jami</span>
              <span class="text-2xl font-bold text-brand-700">{{ formatPrice(cartStore.subtotal) }}</span>
            </div>

            <router-link
              to="/checkout"
              class="block w-full text-center py-3.5 bg-brand-950 hover:bg-brand-900 text-white rounded-xl font-bold text-sm uppercase tracking-wider transition-colors"
            >
              Buyurtmani rasmiylashtirish
            </router-link>

            <p class="text-[10px] text-center text-slate-400 mt-3 leading-relaxed">
              Xarid qilish orqali siz foydalanish shartlariga rozi bo'lasiz
            </p>
          </div>
        </div>

      </div>
    </div>

    <!-- Confirm Modal -->
    <Transition name="fade">
      <div v-if="confirmModal.show" class="fixed inset-0 z-50 flex items-center justify-center p-4 bg-slate-900/50 backdrop-blur-sm">
        <div class="bg-white rounded-2xl shadow-xl max-w-sm w-full p-6">
          <div class="w-12 h-12 bg-red-100 rounded-full flex items-center justify-center mb-4 mx-auto">
            <AlertCircle class="w-6 h-6 text-red-500" />
          </div>
          <h3 class="text-lg font-bold text-slate-900 text-center mb-2">{{ confirmModal.title }}</h3>
          <p class="text-slate-500 text-center text-sm mb-6">{{ confirmModal.text }}</p>
          <div class="flex gap-3">
            <button @click="confirmModal.show = false" class="flex-1 btn-md btn-outline border-slate-200 text-slate-700">Bekor qilish</button>
            <button @click="executeConfirm" class="flex-1 btn-md btn-danger">Tasdiqlash</button>
          </div>
        </div>
      </div>
    </Transition>

  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { ShoppingCart, Trash2, AlertCircle } from '@lucide/vue'
import { useCartStore } from '@/stores/cart'
import { useAlertStore } from '@/stores/alert'

const cartStore  = useCartStore()
const alertStore = useAlertStore()

function formatPrice(price) {
  if (!price && price !== 0) return '—'
  return new Intl.NumberFormat('uz-UZ', { style: 'currency', currency: 'UZS', maximumFractionDigits: 0 }).format(price)
}

async function changeQty(item, qty) {
  if (qty < 1) return
  const result = await cartStore.updateItem(item.id, { quantity: qty })
  if (!result.success) alertStore.error('Xatolik yuz berdi')
}

async function removeItem(id) {
  await cartStore.removeItem(id)
  alertStore.info('Mahsulot savatdan olib tashlandi')
}

const confirmModal = ref({ show: false, title: '', text: '', action: null })
function showConfirm(title, text, action) {
  confirmModal.value = { show: true, title, text, action }
}
async function executeConfirm() {
  if (confirmModal.value.action) await confirmModal.value.action()
  confirmModal.value.show = false
}

function clearCart() {
  showConfirm(
    'Savatni tozalash',
    'Barcha mahsulotlar savatdan olib tashlanadi. Davom etasizmi?',
    async () => {
      await cartStore.clearCart()
      alertStore.info('Savat tozalandi')
    }
  )
}

onMounted(async () => {
  await cartStore.fetchCart()
})
</script>
