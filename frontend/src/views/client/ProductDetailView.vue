<template>
  <div class="min-h-screen">
    <!-- Loading State -->
    <div v-if="loading" class="container-custom py-20">
      <div class="flex flex-col items-center justify-center gap-6">
        <div class="spinner-lg" />
        <p class="text-slate-500">Yuklanmoqda...</p>
      </div>
    </div>

    <!-- Error State -->
    <div v-else-if="!product" class="container-custom py-20 text-center">
      <Package class="w-16 h-16 text-slate-300 mx-auto mb-4" />
      <h2 class="text-2xl font-bold text-slate-700 mb-3">Mahsulot topilmadi</h2>
      <router-link to="/catalog" class="btn-md btn-primary">Katalogga qaytish</router-link>
    </div>

    <template v-else>
      <!-- Breadcrumb -->
      <div class="bg-white border-b border-slate-100">
        <div class="container-custom py-4">
          <div class="flex items-center gap-2 text-sm text-slate-500">
            <router-link to="/" class="hover:text-brand-600">Bosh sahifa</router-link>
            <ChevronRight class="w-4 h-4" />
            <router-link to="/catalog" class="hover:text-brand-600">Katalog</router-link>
            <ChevronRight class="w-4 h-4" />
            <span class="text-slate-900 font-medium truncate max-w-xs">{{ product.name }}</span>
          </div>
        </div>
      </div>

      <div class="container-custom py-10">
        <div class="grid grid-cols-1 lg:grid-cols-2 gap-12 mb-16">

          <!-- ===== IMAGE GALLERY ===== -->
          <div class="space-y-4">
            <!-- Main Image -->
            <div class="relative rounded-3xl overflow-hidden bg-slate-100 aspect-[4/3]">
              <img
                :src="selectedImage"
                :alt="product.name"
                class="w-full h-full object-cover transition-all duration-500"
                @error="handleImgError"
              />
              <div v-if="product.badge" class="absolute top-4 left-4">
                <span class="badge badge-new px-3 py-1.5 text-sm">{{ product.badge }}</span>
              </div>
            </div>

            <!-- Thumbnails -->
            <div v-if="product.images?.length > 1" class="flex gap-3 overflow-x-auto pb-1">
              <button
                v-for="img in product.images"
                :key="img.id"
                @click="selectedImage = img.image"
                class="w-20 h-20 rounded-xl overflow-hidden flex-shrink-0 border-2 transition-all duration-200"
                :class="selectedImage === img.image ? 'border-brand-500 shadow-md' : 'border-slate-200 hover:border-slate-300'"
              >
                <img :src="img.image" :alt="product.name" class="w-full h-full object-cover" />
              </button>
            </div>
          </div>

          <!-- ===== PRODUCT INFO & CALCULATOR ===== -->
          <div class="space-y-6">
            <div>
              <p class="text-[10px] font-bold text-slate-400 uppercase tracking-widest mb-1">{{ product.category_name }}</p>
              <h1 class="text-3xl md:text-4xl font-bold text-slate-900 mb-2">{{ product.name }}</h1>
              
              <!-- Base Price -->
              <p class="text-2xl font-bold text-slate-900 mb-6">
                {{ formatPrice(product.base_price) }} <span class="text-sm font-medium text-slate-400">/ kv.m</span>
              </p>
            </div>

            <!-- CALCULATOR -->
            <div class="space-y-6">
              
              <!-- Dimensions -->
              <div>
                <p class="text-sm font-bold text-slate-900 mb-3 flex items-center gap-2">
                  <svg class="w-4 h-4" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 8V4m0 0h4M4 4l5 5m11-1V4m0 0h-4m4 0l-5 5M4 16v4m0 0h4m-4 0l5-5m11 5l-5-5m5 5v-4m0 4h-4"></path></svg>
                  O'lcham (Kenglik x Balandlik)
                </p>
                <div class="flex items-center gap-4">
                  <div class="flex-1">
                    <label class="block text-xs text-slate-500 mb-1.5">Kenglik (mm)</label>
                    <input
                      v-model.number="dimensions.width"
                      type="number" min="200" max="6000" step="10"
                      placeholder="1200"
                      class="w-full px-4 py-2.5 rounded-lg border border-slate-200 text-sm focus:border-brand-500 focus:ring-1 focus:ring-brand-500 outline-none transition-all"
                      @input="calculatePrice"
                    />
                    <p class="text-[10px] text-slate-400 mt-1" v-if="dimensions.width">{{ (dimensions.width / 1000).toFixed(2) }} m</p>
                  </div>
                  <div class="flex-1">
                    <label class="block text-xs text-slate-500 mb-1.5">Balandlik (mm)</label>
                    <input
                      v-model.number="dimensions.height"
                      type="number" min="200" max="6000" step="10"
                      placeholder="1500"
                      class="w-full px-4 py-2.5 rounded-lg border border-slate-200 text-sm focus:border-brand-500 focus:ring-1 focus:ring-brand-500 outline-none transition-all"
                      @input="calculatePrice"
                    />
                    <p class="text-[10px] text-slate-400 mt-1" v-if="dimensions.height">{{ (dimensions.height / 1000).toFixed(2) }} m</p>
                  </div>
                </div>
              </div>

              <!-- Color Selection -->
              <div v-if="colors.length">
                <p class="text-sm font-bold text-slate-900 mb-3 flex items-center gap-2">
                  <svg class="w-4 h-4" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M7 21a4 4 0 01-4-4V5a2 2 0 012-2h4a2 2 0 012 2v12a4 4 0 01-4 4zm0 0h12a2 2 0 002-2v-4a2 2 0 00-2-2h-2.343M11 7.343l1.657-1.657a2 2 0 012.828 0l2.829 2.829a2 2 0 010 2.828l-8.486 8.485M7 17h.01"></path></svg>
                  Rang
                </p>
                <div class="flex flex-wrap gap-2.5">
                  <button
                    v-for="color in colors"
                    :key="color.id"
                    @click="selectColor(color)"
                    :title="`${color.name} ${color.price_modifier > 0 ? '+' + formatPrice(color.price_modifier) : ''}`"
                    class="w-8 h-8 rounded-full border-2 transition-all flex items-center justify-center relative"
                    :class="selectedColor?.id === color.id ? 'border-brand-600' : 'border-transparent'"
                  >
                    <div class="w-6 h-6 rounded-full border border-slate-200" :style="{ backgroundColor: color.hex_code }" />
                  </button>
                </div>
              </div>



              <!-- Quantity -->
              <div>
                <label class="block text-xs font-bold text-slate-900 mb-2">Miqdor</label>
                <div class="inline-flex items-center bg-white border border-slate-200 rounded-lg">
                  <button @click="qty > 1 ? qty-- : null" class="w-10 h-10 flex items-center justify-center text-slate-500 hover:text-slate-900 transition-colors">−</button>
                  <span class="w-12 text-center text-sm font-semibold text-slate-900">{{ qty }}</span>
                  <button @click="qty++" class="w-10 h-10 flex items-center justify-center text-slate-500 hover:text-slate-900 transition-colors">+</button>
                </div>
              </div>

              <!-- Buttons -->
              <div class="flex flex-col gap-3 pt-4">
                <button
                  @click="addToCart"
                  :disabled="!selectedColor || !dimensions.width || !dimensions.height || addingToCart"
                  class="w-full btn-md bg-brand-950 hover:bg-brand-900 text-white font-medium uppercase tracking-wider text-sm py-3.5 rounded-lg flex items-center justify-center gap-2 transition-colors disabled:opacity-50"
                >
                  <ShoppingCart class="w-4 h-4" />
                  <span v-if="!addingToCart">Savatga qo'shish</span>
                  <span v-else>Qo'shilmoqda...</span>
                </button>

                <a href="/#contact" class="w-full btn-md bg-white border border-slate-300 text-slate-700 hover:bg-slate-50 font-medium uppercase tracking-wider text-sm py-3.5 rounded-lg flex items-center justify-center gap-2 transition-colors">
                  <svg class="w-4 h-4" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M18.364 5.636l-3.536 3.536m0 5.656l3.536 3.536M9.172 9.172L5.636 5.636m3.536 9.192l-3.536 3.536M21 12a9 9 0 11-18 0 9 9 0 0118 0zm-5 0a4 4 0 11-8 0 4 4 0 018 0z"></path></svg>
                  Sotuvchi bilan bog'lanish
                </a>
              </div>

              <!-- Price Result display (subtle if computed) -->
              <div v-if="totalPrice && !calcLoading" class="text-right">
                <p class="text-xs text-slate-500">Umumiy hisob:</p>
                <p class="text-xl font-bold text-brand-600">{{ formatPrice(totalPrice) }}</p>
              </div>

            </div>
          </div>
        </div>

        <!-- Accordions Section -->
        <div class="max-w-3xl space-y-4">
          <!-- Description Accordion -->
          <details class="bg-white rounded-xl border border-slate-100 group">
            <summary class="flex justify-between items-center font-bold text-slate-900 p-5 cursor-pointer list-none">
              Mahsulot haqida
              <ChevronRight class="w-4 h-4 text-slate-400 group-open:rotate-90 transition-transform" />
            </summary>
            <div class="p-5 pt-0 text-slate-600 text-sm leading-relaxed">
              {{ product.description }}
            </div>
          </details>

          <!-- Specs Accordion -->
          <details class="bg-white rounded-xl border border-slate-100 group" open>
            <summary class="flex justify-between items-center font-bold text-slate-900 p-5 cursor-pointer list-none border-b border-slate-100">
              Texnik xususiyatlar
              <ChevronRight class="w-4 h-4 text-slate-400 group-open:rotate-90 transition-transform" />
            </summary>
            <div class="p-5">
              <div v-if="product.specs && Object.keys(product.specs).length" class="grid grid-cols-1 md:grid-cols-2 gap-x-12 gap-y-4">
                <div v-for="(value, key) in product.specs" :key="key" class="flex justify-between border-b border-slate-100 border-dashed pb-2">
                  <span class="text-xs text-slate-500">{{ specLabel(key) }}</span>
                  <span class="text-xs font-semibold text-slate-900">{{ value }}</span>
                </div>
              </div>
            </div>
          </details>
          
          <details class="bg-white rounded-xl border border-slate-100 group">
            <summary class="flex justify-between items-center font-bold text-slate-900 p-5 cursor-pointer list-none">
              Iqlimga chidamlilik
              <ChevronRight class="w-4 h-4 text-slate-400 group-open:rotate-90 transition-transform" />
            </summary>
            <div class="p-5 pt-0 text-slate-600 text-sm">
              Ushbu mahsulot turli iqlim sharoitlariga, ayniqsa O'zbekistonning issiq yoz va sovuq qish mavsumlariga chidamli qilib ishlab chiqarilgan.
            </div>
          </details>

          <details class="bg-white rounded-xl border border-slate-100 group">
            <summary class="flex justify-between items-center font-bold text-slate-900 p-5 cursor-pointer list-none">
              Yetkazib berish
              <ChevronRight class="w-4 h-4 text-slate-400 group-open:rotate-90 transition-transform" />
            </summary>
            <div class="p-5 pt-0 text-slate-600 text-sm">
              Yetkazib berish va o'rnatish xizmatlari Toshkent shahri va viloyatlar bo'ylab bepul amalga oshiriladi.
            </div>
          </details>
        </div>
      </div>
    </template>

    <!-- Auth Modal -->
    <AuthModal :open="authModalOpen" @close="authModalOpen = false" @success="authModalOpen = false" />
  </div>
</template>

<script setup>
import { ref, computed, onMounted, watch } from 'vue'
import { useRoute } from 'vue-router'
import { ChevronRight, ShoppingCart, Check, Package, Calculator } from '@lucide/vue'
import { productsApi } from '@/api/products'
import { useCartStore } from '@/stores/cart'
import { useAuthStore } from '@/stores/auth'
import { useAlertStore } from '@/stores/alert'
import AuthModal from '@/components/client/AuthModal.vue'

const route = useRoute()
const cartStore = useCartStore()
const authStore = useAuthStore()
const alertStore = useAlertStore()

const product = ref(null)
const colors = ref([])
const loading = ref(true)
const selectedColor = ref(null)
const selectedImage = ref(null)
const dimensions = ref({ width: null, height: null })
const qty = ref(1)
const pricePerUnit = ref(null)
const totalPrice = computed(() => pricePerUnit.value ? pricePerUnit.value * qty.value : null)
const calcLoading = ref(false)
const addingToCart = ref(false)
const authModalOpen = ref(false)

const specLabels = {
  profile_thickness: 'Profil qalinligi',
  max_glass: 'Shisha qalinligi',
  sound_insulation: 'Ovoz izolyatsiyasi',
  climate_resistance: 'Iqlim bardoshliligi',
  delivery_info: 'Yetkazib berish',
}

function specLabel(key) {
  return specLabels[key] || key.replace(/_/g, ' ')
}

function handleImgError(e) {
  e.target.src = 'https://via.placeholder.com/600x450/F1F5F9/94A3B8?text=Rasm'
}

function formatPrice(price) {
  if (!price && price !== 0) return '—'
  return new Intl.NumberFormat('uz-UZ', { style: 'currency', currency: 'UZS', maximumFractionDigits: 0 }).format(price)
}

function selectColor(color) {
  selectedColor.value = color
  calculatePrice()
}

async function calculatePrice() {
  if (!dimensions.value.width || !dimensions.value.height || !selectedColor.value) {
    pricePerUnit.value = null
    return
  }
  calcLoading.value = true
  try {
    const res = await productsApi.calculatePrice(route.params.slug, {
      width_mm: dimensions.value.width,
      height_mm: dimensions.value.height,
      color_id: selectedColor.value.id,
    })
    pricePerUnit.value = parseFloat(res.data.total_price)
  } catch {
    pricePerUnit.value = null
  } finally {
    calcLoading.value = false
  }
}

async function addToCart() {
  if (!authStore.isLoggedIn) { authModalOpen.value = true; return }
  if (!selectedColor.value || !dimensions.value.width || !dimensions.value.height) return
  addingToCart.value = true
  const result = await cartStore.addItem({
    product_id: product.value.id,
    color_id: selectedColor.value.id,
    width_mm: dimensions.value.width,
    height_mm: dimensions.value.height,
    quantity: qty.value,
  })
  addingToCart.value = false
  if (result.success) {
    alertStore.success('Mahsulot savatga qo\'shildi!')
  } else {
    alertStore.error('Xatolik yuz berdi. Qayta urinib ko\'ring.')
  }
}

function openAuthModal() {
  authModalOpen.value = true
}

onMounted(async () => {
  const slug = route.params.slug
  try {
    const [productRes, colorsRes] = await Promise.all([
      productsApi.getProduct(slug),
      productsApi.getProductColors(slug),
    ])
    product.value = productRes.data
    colors.value = colorsRes.data

    const mainImg = product.value.images?.find(i => i.is_main) || product.value.images?.[0]
    selectedImage.value = mainImg?.image || null

    if (colors.value.length) {
      selectedColor.value = colors.value[0]
    }
  } catch (e) {
    console.error(e)
  }
  loading.value = false
})
</script>
