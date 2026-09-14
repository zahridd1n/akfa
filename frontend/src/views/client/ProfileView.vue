<template>
  <div class="min-h-screen" style="background: #EBF3F8;">

    <!-- Tabs Header (Sticky) -->
    <div class="bg-white border-b border-slate-100 sticky top-0 z-10">
      <div class="flex overflow-x-auto scrollbar-hide">
        <button
          v-for="tab in tabs"
          :key="tab.id"
          @click="activeTab = tab.id"
          class="flex-1 min-w-0 flex flex-col sm:flex-row items-center justify-center gap-1 sm:gap-2 py-3 px-3 text-xs sm:text-sm font-medium border-b-2 transition-all duration-200 whitespace-nowrap"
          :class="activeTab === tab.id ? 'border-brand-500 text-brand-600 bg-brand-50' : 'border-transparent text-slate-500 hover:text-slate-700'"
          :id="`tab-${tab.id}`"
        >
          <component :is="tab.icon" class="w-4 h-4 flex-shrink-0" />
          <span>{{ tab.label }}</span>
        </button>
      </div>
    </div>

    <!-- =================== PROFIL =================== -->
    <div v-if="activeTab === 'profile'" class="p-4 max-w-lg mx-auto">
      <!-- User Card -->
      <div class="bg-white rounded-2xl border border-slate-100 p-6 mb-4">
        <div class="flex items-center gap-4 mb-6">
          <div class="w-16 h-16 bg-gradient-to-br from-brand-400 to-brand-700 rounded-2xl flex items-center justify-center text-white text-2xl font-bold flex-shrink-0">
            {{ authStore.fullName.charAt(0).toUpperCase() }}
          </div>
          <div>
            <h2 class="text-lg font-bold text-slate-900">{{ authStore.fullName }}</h2>
            <p class="text-slate-500 text-sm">{{ authStore.user?.phone_number }}</p>
            <span class="inline-block mt-1 px-2 py-0.5 bg-brand-50 text-brand-600 text-[10px] font-bold rounded uppercase tracking-wider">
              {{ authStore.isAdmin ? 'Administrator' : 'Mijoz' }}
            </span>
          </div>
        </div>

        <form @submit.prevent="updateProfile" class="space-y-4">
          <div>
            <label class="form-label">Ism va Familiya</label>
            <input v-model="profileForm.full_name" type="text" class="form-input" id="profile-name" required />
          </div>
          <div>
            <label class="form-label">Telefon raqam</label>
            <input v-model="profileForm.phone_number" type="tel" class="form-input" disabled />
            <p class="text-xs text-slate-400 mt-1">Telefon raqamni o'zgartirib bo'lmaydi</p>
          </div>
          <button type="submit" :disabled="savingProfile" class="btn-md btn-primary w-full">
            <span v-if="!savingProfile">Saqlash</span>
            <div v-else class="spinner" />
          </button>
        </form>
      </div>

      <!-- Password Card -->
      <div class="bg-white rounded-2xl border border-slate-100 p-6">
        <h3 class="font-bold text-slate-900 mb-4">Parolni o'zgartirish</h3>
        <form @submit.prevent="changePassword" class="space-y-4">
          <div>
            <label class="form-label">Joriy parol</label>
            <input v-model="passwordForm.old_password" type="password" class="form-input" required />
          </div>
          <div>
            <label class="form-label">Yangi parol</label>
            <input v-model="passwordForm.new_password" type="password" class="form-input" required />
          </div>
          <p v-if="passwordError" class="text-sm text-red-500">{{ passwordError }}</p>
          <button type="submit" :disabled="savingPassword" class="btn-md btn-outline w-full">
            <span v-if="!savingPassword">Parolni o'zgartirish</span>
            <div v-else class="spinner" />
          </button>
        </form>
      </div>
    </div>

    <!-- =================== BUYURTMALARIM =================== -->
    <div v-if="activeTab === 'orders'" class="p-4 max-w-2xl mx-auto">
      <!-- Loading -->
      <div v-if="loadingOrders" class="space-y-3">
        <div v-for="i in 3" :key="i" class="skeleton h-40 rounded-xl" />
      </div>

      <!-- Empty -->
      <div v-else-if="!orders.length" class="text-center py-16">
        <div class="w-16 h-16 bg-slate-100 rounded-full flex items-center justify-center mx-auto mb-4">
          <Package class="w-8 h-8 text-slate-300" />
        </div>
        <h3 class="font-bold text-slate-700 mb-2">Buyurtmalar yo'q</h3>
        <p class="text-slate-400 text-sm mb-5">Hali birorta buyurtma bermadingiz</p>
        <router-link to="/catalog" class="btn-md btn-primary">Xarid qilish</router-link>
      </div>

      <!-- Orders List -->
      <div v-else class="space-y-3">
        <div v-for="order in orders" :key="order.id" class="bg-white rounded-xl border border-slate-100 overflow-hidden">

          <!-- Order Header -->
          <div class="flex items-center justify-between px-4 py-3 bg-slate-50 border-b border-slate-100">
            <div>
              <div class="flex items-center gap-2 mb-0.5">
                <span class="font-bold text-slate-900 text-sm">#{{ order.order_number }}</span>
                <span
                  class="px-2 py-0.5 rounded-full text-[10px] font-bold uppercase tracking-wider"
                  :class="{
                    'bg-amber-100 text-amber-700': order.status === 'pending',
                    'bg-blue-100 text-blue-700': order.status === 'processing',
                    'bg-purple-100 text-purple-700': order.status === 'shipped',
                    'bg-emerald-100 text-emerald-700': order.status === 'delivered',
                    'bg-red-100 text-red-600': order.status === 'cancelled',
                  }"
                >
                  {{ statusLabel(order.status) }}
                </span>
              </div>
              <p class="text-xs text-slate-400">{{ formatDate(order.created_at) }}</p>
            </div>
            <div class="text-right">
              <p class="text-[10px] text-slate-400 mb-0.5">Jami to'lov</p>
              <p class="text-base font-bold text-brand-600">{{ formatPrice(order.total_amount) }}</p>
            </div>
          </div>

          <!-- Order Items -->
          <div class="px-4 py-3 space-y-2">
            <div v-for="item in order.items" :key="item.id" class="flex items-center gap-3 text-sm">
              <!-- Image -->
              <div class="w-12 h-12 rounded-lg bg-[#EBF3F8] flex-shrink-0 flex items-center justify-center overflow-hidden">
                <img
                  v-if="item.main_image"
                  :src="item.main_image"
                  :alt="item.product_name"
                  class="max-w-full max-h-full object-contain"
                />
                <Package v-else class="w-5 h-5 text-slate-300" />
              </div>
              <div class="flex-1 min-w-0">
                <p class="font-semibold text-slate-800 truncate">{{ item.product_name }}</p>
                <p class="text-xs text-slate-400">{{ item.color_name }} · {{ item.width_mm }}×{{ item.height_mm }}mm · {{ item.quantity }} dona</p>
              </div>
              <span class="text-sm font-semibold text-slate-700 flex-shrink-0">{{ formatPrice(item.total_price) }}</span>
            </div>
          </div>

          <!-- Delivery + Actions -->
          <div class="px-4 py-3 border-t border-slate-100 flex items-center justify-between gap-3">
            <div v-if="order.delivery_address" class="flex items-start gap-1.5 text-xs text-slate-400 flex-1 min-w-0">
              <MapPin class="w-3.5 h-3.5 flex-shrink-0 mt-0.5 text-brand-400" />
              <span class="truncate">{{ order.delivery_address.region_display || order.delivery_address.region }}, {{ order.delivery_address.full_address || order.delivery_address.street }}</span>
            </div>
            <button
              v-if="order.status === 'pending'"
              @click="cancelOrder(order.order_number)"
              class="flex-shrink-0 px-3 py-1.5 rounded-lg border border-red-200 text-red-500 text-xs font-semibold hover:bg-red-50 transition-colors"
              :id="`cancel-order-${order.order_number}`"
            >
              Bekor qilish
            </button>
          </div>
        </div>
      </div>
    </div>

    <!-- =================== MANZILLARIM =================== -->
    <div v-if="activeTab === 'addresses'" class="p-4 max-w-2xl mx-auto">
      <!-- Loading -->
      <div v-if="loadingAddresses" class="space-y-3">
        <div v-for="i in 2" :key="i" class="skeleton h-24 rounded-xl" />
      </div>

      <div v-else>
        <!-- Addresses -->
        <div class="space-y-3 mb-4">
          <div v-for="addr in addresses" :key="addr.id" class="bg-white rounded-xl border border-slate-100 p-4">
            <div class="flex items-start justify-between gap-3">
              <div class="flex items-start gap-3 flex-1 min-w-0">
                <div class="w-8 h-8 bg-brand-50 rounded-lg flex items-center justify-center flex-shrink-0 mt-0.5">
                  <MapPin class="w-4 h-4 text-brand-600" />
                </div>
                <div class="flex-1 min-w-0">
                  <div class="flex items-center gap-2 mb-1">
                    <span class="font-semibold text-slate-900 text-sm">{{ getRegionLabel(addr.region) }}</span>
                    <span v-if="addr.is_default" class="px-1.5 py-0.5 bg-emerald-100 text-emerald-700 text-[9px] font-bold rounded uppercase">Asosiy</span>
                  </div>
                  <p class="text-xs text-slate-500 leading-relaxed">{{ addr.full_address || [addr.city, addr.street, addr.house_number].filter(Boolean).join(', ') }}</p>
                </div>
              </div>
              <div class="flex items-center gap-1 flex-shrink-0">
                <button
                  v-if="!addr.is_default"
                  @click="setDefault(addr.id)"
                  class="px-2 py-1 rounded-lg border border-slate-200 text-slate-600 text-[11px] font-medium hover:bg-slate-50 transition-colors"
                >Asosiy</button>
                <button @click="deleteAddress(addr.id)" class="p-1.5 rounded-lg text-red-400 hover:bg-red-50 transition-colors">
                  <Trash2 class="w-4 h-4" />
                </button>
              </div>
            </div>
          </div>

          <div v-if="!addresses.length" class="text-center py-10">
            <MapPin class="w-10 h-10 text-slate-200 mx-auto mb-3" />
            <p class="text-slate-400 text-sm">Manzillar yo'q</p>
          </div>
        </div>

        <!-- Add Address Button -->
        <button @click="showAddrForm = !showAddrForm" class="btn-md btn-outline w-full mb-4">
          <Plus class="w-4 h-4" />
          {{ showAddrForm ? 'Bekor qilish' : "Yangi manzil qo'shish" }}
        </button>

        <!-- Add Address Form -->
        <Transition name="slide-up">
          <div v-if="showAddrForm" class="bg-white rounded-xl border border-slate-100 p-4 space-y-4">
            <h3 class="font-semibold text-slate-900">Yangi manzil</h3>
            <div>
              <label class="form-label">Viloyat *</label>
              <select v-model="newAddr.region" class="form-select">
                <option value="">Tanlang...</option>
                <option v-for="r in regions" :key="r.value" :value="r.value">{{ r.label }}</option>
              </select>
            </div>
            <div class="grid grid-cols-2 gap-3">
              <div>
                <label class="form-label">Shahar/Tuman</label>
                <input v-model="newAddr.city" type="text" class="form-input" placeholder="Toshkent" />
              </div>
              <div>
                <label class="form-label">Ko'cha</label>
                <input v-model="newAddr.street" type="text" class="form-input" placeholder="Amir Temur" />
              </div>
              <div>
                <label class="form-label">Uy raqami</label>
                <input v-model="newAddr.house_number" type="text" class="form-input" placeholder="12A" />
              </div>
              <div>
                <label class="form-label">Xonadon</label>
                <input v-model="newAddr.apartment" type="text" class="form-input" placeholder="5" />
              </div>
            </div>
            <div>
              <label class="form-label">To'liq manzil</label>
              <textarea v-model="newAddr.full_address" rows="2" class="form-input resize-none" placeholder="Masalan: Yunusobod tumani, 5-uy" />
            </div>
            <label class="flex items-center gap-2 cursor-pointer">
              <input v-model="newAddr.is_default" type="checkbox" class="w-4 h-4" />
              <span class="text-sm text-slate-600">Asosiy manzil sifatida saqlash</span>
            </label>
            <button @click="addAddress" :disabled="savingAddr" class="btn-md btn-primary w-full">
              <span v-if="!savingAddr">Saqlash</span>
              <div v-else class="spinner" />
            </button>
          </div>
        </Transition>
      </div>
    </div>

    <!-- Confirm Modal -->
    <Transition name="fade">
      <div v-if="confirmModal.show" class="fixed inset-0 z-50 flex items-center justify-center p-4 bg-slate-900/50 backdrop-blur-sm">
        <div class="bg-white rounded-2xl shadow-xl max-w-sm w-full p-6">
          <div class="w-12 h-12 bg-red-100 rounded-full flex items-center justify-center mb-4 mx-auto">
            <AlertCircle class="w-6 h-6 text-red-600" />
          </div>
          <h3 class="text-lg font-bold text-slate-900 text-center mb-2">{{ confirmModal.title }}</h3>
          <p class="text-slate-500 text-center text-sm mb-6">{{ confirmModal.text }}</p>
          <div class="flex gap-3">
            <button @click="confirmModal.show = false" class="flex-1 btn-md btn-outline border-slate-200 text-slate-700">Bekor qilish</button>
            <button @click="executeConfirm" class="flex-1 btn-md btn-danger" :disabled="confirmModal.loading">
              <span v-if="!confirmModal.loading">Tasdiqlash</span>
              <div v-else class="spinner" />
            </button>
          </div>
        </div>
      </div>
    </Transition>

  </div>
</template>

<script setup>
import { ref, onMounted, watch } from 'vue'
import { useRoute } from 'vue-router'
import { User, Package, MapPin, Trash2, Plus, AlertCircle } from '@lucide/vue'
import { useAuthStore } from '@/stores/auth'
import { useAlertStore } from '@/stores/alert'
import { authApi } from '@/api/auth'
import { ordersApi } from '@/api/orders'
import { addressApi } from '@/api/address'

const route     = useRoute()
const authStore = useAuthStore()
const alertStore = useAlertStore()

const activeTab = ref(route.query.tab || 'profile')
const tabs = [
  { id: 'profile',   label: 'Profil',       icon: User },
  { id: 'orders',    label: 'Buyurtmalaim', icon: Package },
  { id: 'addresses', label: 'Manzillarim',  icon: MapPin },
]

// Profile
const profileForm   = ref({ full_name: authStore.user?.full_name || '', phone_number: authStore.user?.phone_number || '' })
const savingProfile = ref(false)
const passwordForm  = ref({ old_password: '', new_password: '' })
const savingPassword = ref(false)
const passwordError  = ref('')

async function updateProfile() {
  savingProfile.value = true
  const result = await authStore.updateProfile({ full_name: profileForm.value.full_name })
  if (result.success) alertStore.success('Profil yangilandi!')
  else alertStore.error('Xatolik yuz berdi')
  savingProfile.value = false
}

async function changePassword() {
  passwordError.value = ''
  savingPassword.value = true
  try {
    await authApi.changePassword(passwordForm.value)
    alertStore.success("Parol muvaffaqiyatli o'zgartirildi!")
    passwordForm.value = { old_password: '', new_password: '' }
  } catch (err) {
    passwordError.value = err.response?.data?.detail || "Eski parol noto'g'ri"
  }
  savingPassword.value = false
}

// Confirm Modal
const confirmModal = ref({ show: false, title: '', text: '', action: null, loading: false })
function showConfirm(title, text, action) {
  confirmModal.value = { show: true, title, text, action, loading: false }
}
async function executeConfirm() {
  if (confirmModal.value.action) {
    confirmModal.value.loading = true
    await confirmModal.value.action()
  }
  confirmModal.value.show = false
}

// Orders
const orders       = ref([])
const loadingOrders = ref(true)
async function fetchOrders() {
  loadingOrders.value = true
  try {
    const res = await ordersApi.getOrders()
    orders.value = res.data.results || res.data
  } catch {}
  loadingOrders.value = false
}
function cancelOrder(orderNumber) {
  showConfirm(
    'Buyurtmani bekor qilish',
    "Buyurtmani bekor qilmoqchimisiz? Bu amalni ortga qaytarib bo'lmaydi.",
    async () => {
      try {
        await ordersApi.cancelOrder(orderNumber)
        await fetchOrders()
        alertStore.success('Buyurtma bekor qilindi')
      } catch { alertStore.error('Bekor qilishda xatolik') }
    }
  )
}

// Addresses
const addresses       = ref([])
const loadingAddresses = ref(true)
const showAddrForm    = ref(false)
const savingAddr      = ref(false)
const newAddr = ref({ region: '', city: '', street: '', house_number: '', apartment: '', full_address: '', is_default: false })

const regions = [
  { value: 'tashkent_city',   label: 'Toshkent shahri' },
  { value: 'tashkent_region', label: 'Toshkent viloyati' },
  { value: 'samarkand',       label: 'Samarqand' },
  { value: 'bukhara',         label: 'Buxoro' },
  { value: 'namangan',        label: 'Namangan' },
  { value: 'andijan',         label: 'Andijon' },
  { value: 'fergana',         label: "Farg'ona" },
  { value: 'kashkadarya',     label: 'Qashqadaryo' },
  { value: 'surkhandarya',    label: 'Surxondaryo' },
  { value: 'syrdarya',        label: 'Sirdaryo' },
  { value: 'jizzakh',         label: 'Jizzax' },
  { value: 'navoi',           label: 'Navoiy' },
  { value: 'khorezm',         label: 'Xorazm' },
  { value: 'karakalpakstan',  label: "Qoraqalpog'iston" },
]

function getRegionLabel(val) {
  return regions.find(x => x.value === val)?.label || val
}

async function fetchAddresses() {
  loadingAddresses.value = true
  try {
    const res = await addressApi.getAddresses()
    addresses.value = res.data.results || res.data
  } catch {}
  loadingAddresses.value = false
}

async function setDefault(id) {
  await addressApi.setDefault(id)
  await fetchAddresses()
  alertStore.success('Asosiy manzil yangilandi')
}

function deleteAddress(id) {
  showConfirm(
    "Manzilni o'chirish",
    "Ushbu manzilni o'chirishni tasdiqlaysizmi?",
    async () => {
      try {
        await addressApi.deleteAddress(id)
        addresses.value = addresses.value.filter(a => a.id !== id)
        alertStore.info("Manzil o'chirildi")
      } catch { alertStore.error("Manzilni o'chirishda xatolik yuz berdi") }
    }
  )
}

async function addAddress() {
  if (!newAddr.value.region)        { alertStore.warning('Viloyatni tanlang'); return }
  if (!newAddr.value.city)          { alertStore.warning('Shahar/Tumanni kiriting'); return }
  if (!newAddr.value.street)        { alertStore.warning("Ko'chani kiriting"); return }
  if (!newAddr.value.house_number)  { alertStore.warning('Uy raqamini kiriting'); return }
  if (!newAddr.value.full_address)  { alertStore.warning("To'liq manzilni kiriting"); return }
  savingAddr.value = true
  try {
    const res = await addressApi.createAddress(newAddr.value)
    addresses.value.push(res.data)
    showAddrForm.value = false
    newAddr.value = { region: '', city: '', street: '', house_number: '', apartment: '', full_address: '', is_default: false }
    alertStore.success("Manzil qo'shildi!")
  } catch (err) {
    const errors = err.response?.data
    let msg = 'Xatolik yuz berdi'
    if (errors && typeof errors === 'object') msg = Object.values(errors).flat().join(', ')
    alertStore.error(msg)
  }
  savingAddr.value = false
}

// Utilities
function formatDate(d) {
  return new Date(d).toLocaleDateString('uz-UZ', { day: '2-digit', month: 'long', year: 'numeric' })
}
function formatPrice(price) {
  if (!price && price !== 0) return '—'
  return new Intl.NumberFormat('uz-UZ', { style: 'currency', currency: 'UZS', maximumFractionDigits: 0 }).format(price)
}
function statusLabel(s) {
  return { pending: 'Kutilmoqda', processing: 'Tayyorlanmoqda', shipped: "Yo'lda", delivered: 'Yetkazildi', cancelled: 'Bekor qilindi' }[s] || s
}

watch(activeTab, (tab) => {
  if (tab === 'orders' && !orders.value.length) fetchOrders()
  if (tab === 'addresses' && !addresses.value.length) fetchAddresses()
})

onMounted(() => {
  if (route.query.tab === 'orders')    fetchOrders()
  if (route.query.tab === 'addresses') fetchAddresses()
})
</script>

<style scoped>
.scrollbar-hide::-webkit-scrollbar { display: none; }
.scrollbar-hide { -ms-overflow-style: none; scrollbar-width: none; }
.slide-up-enter-active, .slide-up-leave-active { transition: all 0.25s ease; }
.slide-up-enter-from, .slide-up-leave-to { opacity: 0; transform: translateY(-8px); }
</style>
