<template>
  <div class="container-custom py-10 max-w-5xl">
    <div class="flex items-center gap-2 text-sm text-slate-500 mb-6">
      <router-link to="/cart" class="hover:text-brand-600 flex items-center gap-1">
        <ChevronLeft class="w-4 h-4" /> Savatga qaytish
      </router-link>
    </div>

    <h1 class="text-2xl md:text-3xl font-bold text-slate-900 mb-8">Buyurtmani Rasmiylashtirish</h1>

    <!-- Success State -->
    <div v-if="orderSuccess" class="text-center py-16">
      <div class="w-24 h-24 bg-emerald-100 rounded-full flex items-center justify-center mx-auto mb-6 animate-slide-up">
        <CheckCircle class="w-12 h-12 text-emerald-600" />
      </div>
      <h2 class="text-3xl font-bold text-slate-900 mb-3">Buyurtma Qabul Qilindi!</h2>
      <p class="text-slate-500 text-lg mb-3">Buyurtma raqamingiz:</p>
      <div class="inline-block bg-brand-50 border border-brand-200 rounded-2xl px-8 py-4 mb-8">
        <span class="text-3xl font-bold text-brand-600">#{{ orderNumber }}</span>
      </div>
      <p class="text-slate-500 mb-8 max-w-md mx-auto">
        Buyurtmangiz holati haqida xabarnomalar qabul qilasiz. Buyurtmalarim sahifasida kuzatib boring.
      </p>
      <div class="flex flex-wrap gap-3 justify-center">
        <router-link to="/profile?tab=orders" class="btn-lg btn-primary" id="view-orders-btn">
          Buyurtmalarni ko'rish <ArrowRight class="w-5 h-5" />
        </router-link>
        <router-link to="/" class="btn-lg btn-secondary">
          Bosh sahifaga qaytish
        </router-link>
      </div>
    </div>

    <!-- Checkout Form -->
    <div v-else class="grid grid-cols-1 lg:grid-cols-3 gap-8">
      <!-- Left: Delivery -->
      <div class="lg:col-span-2 space-y-6">

        <!-- Addresses -->
        <div class="card p-6">
          <h2 class="font-bold text-slate-900 text-lg mb-5 flex items-center gap-2">
            <MapPin class="w-5 h-5 text-brand-600" /> Yetkazib berish manzili
          </h2>

          <!-- Loading addresses -->
          <div v-if="loadingAddresses" class="space-y-3">
            <div v-for="i in 2" :key="i" class="skeleton h-24 rounded-xl" />
          </div>

          <!-- Address List -->
          <div v-else-if="addresses.length" class="space-y-3 mb-4">
            <div
              v-for="addr in addresses"
              :key="addr.id"
              @click="selectedAddressId = addr.id"
              class="border-2 rounded-xl p-4 cursor-pointer transition-all duration-200"
              :class="selectedAddressId === addr.id ? 'border-brand-500 bg-brand-50' : 'border-slate-200 hover:border-slate-300'"
              :id="`address-select-${addr.id}`"
            >
              <div class="flex items-start justify-between">
                <div>
                  <div class="flex items-center gap-2 mb-1">
                    <div class="w-4 h-4 rounded-full border-2 flex-shrink-0 flex items-center justify-center"
                         :class="selectedAddressId === addr.id ? 'border-brand-500' : 'border-slate-300'">
                      <div v-if="selectedAddressId === addr.id" class="w-2 h-2 rounded-full bg-brand-500" />
                    </div>
                    <span class="font-semibold text-slate-900 text-sm">{{ getRegionLabel(addr.region) }}</span>
                    <span v-if="addr.is_default" class="badge badge-green text-[10px]">Asosiy</span>
                  </div>
                  <p class="text-sm text-slate-500 ml-6">{{ addr.full_address || [addr.city, addr.street, addr.house_number].filter(Boolean).join(', ') }}</p>
                </div>
                <button 
                  @click.stop="deleteAddress(addr.id)" 
                  class="btn-sm btn-ghost text-red-500 hover:bg-red-50 p-2 ml-4 flex-shrink-0" 
                  title="O'chirish"
                >
                  <Trash2 class="w-4 h-4" />
                </button>
              </div>
            </div>
          </div>

          <!-- Add New Address -->
          <button
            @click="showNewAddressForm = !showNewAddressForm"
            class="btn-sm btn-outline w-full gap-2"
            id="add-new-address-btn"
          >
            <Plus class="w-4 h-4" />
            {{ showNewAddressForm ? 'Bekor qilish' : 'Yangi manzil qo\'shish' }}
          </button>

          <!-- New Address Form -->
          <Transition name="slide-up">
            <div v-if="showNewAddressForm" class="mt-4 space-y-4 p-5 bg-slate-50 rounded-2xl border border-slate-200">
              <h3 class="font-semibold text-slate-900">Yangi manzil</h3>

              <div>
                <label class="form-label">Viloyat *</label>
                <select v-model="newAddress.region" class="form-select" id="new-address-region">
                  <option value="">Viloyatni tanlang</option>
                  <option v-for="r in regions" :key="r.value" :value="r.value">{{ r.label }}</option>
                </select>
              </div>

              <div class="grid grid-cols-2 gap-3">
                <div>
                  <label class="form-label">Shahar / Tuman</label>
                  <input v-model="newAddress.city" type="text" placeholder="Toshkent" class="form-input" id="new-address-city" />
                </div>
                <div>
                  <label class="form-label">Ko'cha</label>
                  <input v-model="newAddress.street" type="text" placeholder="Amir Temur ko'chasi" class="form-input" id="new-address-street" />
                </div>
              </div>

              <div class="grid grid-cols-2 gap-3">
                <div>
                  <label class="form-label">Uy raqami</label>
                  <input v-model="newAddress.house_number" type="text" placeholder="12A" class="form-input" id="new-address-house" />
                </div>
                <div>
                  <label class="form-label">Xonadon (ixtiyoriy)</label>
                  <input v-model="newAddress.apartment" type="text" placeholder="5" class="form-input" />
                </div>
              </div>

              <div>
                <label class="form-label">To'liq manzil (aniq)</label>
                <textarea
                  v-model="newAddress.full_address"
                  rows="2"
                  placeholder="Masalan: Yunusobod tumani, Qoratosh MFY, 5-uy, 3-xonadon"
                  class="form-input resize-none"
                  id="new-address-full"
                />
              </div>

              <label class="flex items-center gap-2 cursor-pointer">
                <input v-model="newAddress.is_default" type="checkbox" class="w-4 h-4 rounded border-slate-300 text-brand-500" />
                <span class="text-sm text-slate-600">Asosiy manzil sifatida saqlash</span>
              </label>

              <button @click="saveNewAddress" :disabled="savingAddress" class="btn-md btn-primary w-full" id="save-address-btn">
                <span v-if="!savingAddress">Manzilni saqlash</span>
                <div v-else class="spinner" />
              </button>
            </div>
          </Transition>
        </div>

        <!-- Notes -->
        <div class="card p-6">
          <h2 class="font-bold text-slate-900 text-lg mb-4 flex items-center gap-2">
            <FileText class="w-5 h-5 text-brand-600" /> Izoh (ixtiyoriy)
          </h2>
          <textarea
            v-model="notes"
            rows="3"
            placeholder="Masalan: qavat, eshik rangi haqida qo'shimcha ma'lumot..."
            class="form-input resize-none"
            id="checkout-notes"
          />
        </div>
      </div>

      <!-- Right: Summary + Submit -->
      <div>
        <div class="card p-6 sticky top-20 space-y-4">
          <h2 class="font-bold text-slate-900 text-lg">Buyurtma Xulosasi</h2>

          <!-- Cart Items Summary -->
          <div class="space-y-3 max-h-64 overflow-y-auto">
            <div v-for="item in cartStore.items" :key="item.id" class="flex gap-3 items-start">
              <img
                :src="item.main_image || 'https://via.placeholder.com/48/F1F5F9/94A3B8?text='"
                :alt="item.product_name"
                class="w-12 h-12 rounded-lg object-cover flex-shrink-0 bg-slate-100"
              />
              <div class="flex-1 min-w-0">
                <p class="text-sm font-medium text-slate-900 line-clamp-1">{{ item.product_name }}</p>
                <p class="text-xs text-slate-500">{{ item.color_name }} · {{ item.width_mm }}×{{ item.height_mm }}mm · {{ item.quantity }} dona</p>
                <p class="text-sm font-semibold text-brand-600">{{ formatPrice(item.total_price) }}</p>
              </div>
            </div>
          </div>

          <div class="h-px bg-slate-100" />

          <div class="space-y-2 text-sm">
            <div class="flex justify-between text-slate-600">
              <span>Mahsulotlar</span>
              <span>{{ formatPrice(cartStore.subtotal) }}</span>
            </div>
            <div class="flex justify-between text-slate-600">
              <span>Yetkazib berish</span>
              <span class="text-emerald-600 font-medium">Kelishiladi</span>
            </div>
          </div>

          <div class="h-px bg-slate-100" />

          <div class="flex justify-between items-center">
            <span class="font-bold text-slate-900">Jami</span>
            <span class="text-2xl font-bold text-brand-600">{{ formatPrice(cartStore.subtotal) }}</span>
          </div>

          <!-- Order Button -->
          <button
            @click="placeOrder"
            :disabled="!selectedAddressId || submitting"
            class="btn-lg btn-primary w-full"
            id="place-order-btn"
          >
            <span v-if="!submitting">
              <ShoppingBag class="w-5 h-5" /> Buyurtmani tasdiqlash
            </span>
            <div v-else class="spinner" />
          </button>

          <p v-if="!selectedAddressId" class="text-xs text-amber-600 text-center flex items-center justify-center gap-1">
            <AlertCircle class="w-3.5 h-3.5" /> Manzil tanlang
          </p>
        </div>
      </div>
    </div>

    <!-- Confirm Modal -->
    <Transition name="fade">
      <div v-if="confirmModal.show" class="fixed inset-0 z-50 flex items-center justify-center p-4 bg-slate-900/50 backdrop-blur-sm">
        <div class="bg-white rounded-2xl shadow-xl max-w-sm w-full p-6 animate-slide-up">
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
import { ref, onMounted } from 'vue'
import { ChevronLeft, MapPin, Plus, FileText, ShoppingBag, ArrowRight, CheckCircle, AlertCircle, Trash2 } from '@lucide/vue'
import { addressApi } from '@/api/address'
import { ordersApi } from '@/api/orders'
import { useCartStore } from '@/stores/cart'
import { useAlertStore } from '@/stores/alert'

const cartStore = useCartStore()
const alertStore = useAlertStore()

const addresses = ref([])
const selectedAddressId = ref(null)
const loadingAddresses = ref(true)
const showNewAddressForm = ref(false)
const savingAddress = ref(false)
const submitting = ref(false)
const notes = ref('')
const orderSuccess = ref(false)
const orderNumber = ref('')

const newAddress = ref({
  region: '', city: '', street: '', house_number: '',
  apartment: '', full_address: '', is_default: false
})

// Confirm Modal state
const confirmModal = ref({
  show: false,
  title: '',
  text: '',
  action: null,
  loading: false
})

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

const regions = [
  { value: 'tashkent_city', label: 'Toshkent shahri' },
  { value: 'tashkent_region', label: 'Toshkent viloyati' },
  { value: 'samarkand', label: 'Samarqand' },
  { value: 'bukhara', label: 'Buxoro' },
  { value: 'namangan', label: 'Namangan' },
  { value: 'andijan', label: 'Andijon' },
  { value: 'fergana', label: "Farg'ona" },
  { value: 'kashkadarya', label: 'Qashqadaryo' },
  { value: 'surkhandarya', label: 'Surxondaryo' },
  { value: 'syrdarya', label: 'Sirdaryo' },
  { value: 'jizzakh', label: 'Jizzax' },
  { value: 'navoi', label: 'Navoiy' },
  { value: 'khorezm', label: 'Xorazm' },
  { value: 'karakalpakstan', label: "Qoraqalpog'iston" }
]

function getRegionLabel(val) {
  const r = regions.find(x => x.value === val)
  return r ? r.label : val
}

function formatPrice(price) {
  if (!price && price !== 0) return '—'
  return new Intl.NumberFormat('uz-UZ', { style: 'currency', currency: 'UZS', maximumFractionDigits: 0 }).format(price)
}

async function saveNewAddress() {
  if (!newAddress.value.region) { alertStore.warning('Viloyatni tanlang'); return }
  if (!newAddress.value.city) { alertStore.warning('Shahar/Tumanni kiriting'); return }
  if (!newAddress.value.street) { alertStore.warning('Ko\'chani kiriting'); return }
  if (!newAddress.value.house_number) { alertStore.warning('Uy raqamini kiriting'); return }
  if (!newAddress.value.full_address) { alertStore.warning('To\'liq manzilni kiriting'); return }
  
  savingAddress.value = true
  try {
    const res = await addressApi.createAddress(newAddress.value)
    addresses.value.push(res.data)
    selectedAddressId.value = res.data.id
    showNewAddressForm.value = false
    newAddress.value = { region: '', city: '', street: '', house_number: '', apartment: '', full_address: '', is_default: false }
    alertStore.success('Manzil saqlandi!')
  } catch (err) {
    const errors = err.response?.data
    let msg = 'Manzilni saqlashda xatolik'
    if (errors && typeof errors === 'object') {
      msg = Object.values(errors).flat().join(', ')
    }
    alertStore.error(msg)
  }
  savingAddress.value = false
}

function deleteAddress(id) {
  showConfirm(
    'Manzilni o\'chirish',
    'Manzilni o\'chirishni tasdiqlaysizmi?',
    async () => {
      try {
        await addressApi.deleteAddress(id)
        addresses.value = addresses.value.filter(a => a.id !== id)
        
        // Asosiy manzilni yangilash
        if (selectedAddressId.value === id) {
          const defaultAddr = addresses.value.find(a => a.is_default)
          if (defaultAddr) selectedAddressId.value = defaultAddr.id
          else if (addresses.value.length) selectedAddressId.value = addresses.value[0].id
          else selectedAddressId.value = null
        }
        
        alertStore.info("Manzil o'chirildi")
      } catch (err) {
        alertStore.error("Manzilni o'chirishda xatolik yuz berdi")
      }
    }
  )
}

async function placeOrder() {
  if (!selectedAddressId.value) { alertStore.warning('Manzil tanlang'); return }
  submitting.value = true
  try {
    const res = await ordersApi.createOrder({
      address_id: selectedAddressId.value,
      notes: notes.value,
    })
    orderNumber.value = res.data.order_number
    orderSuccess.value = true
    await cartStore.clearCart()
    alertStore.success('Buyurtma muvaffaqiyatli qabul qilindi!')
  } catch (err) {
    alertStore.error(err.response?.data?.detail || 'Buyurtma berishda xatolik yuz berdi')
  }
  submitting.value = false
}

onMounted(async () => {
  await cartStore.fetchCart()
  try {
    const res = await addressApi.getAddresses()
    addresses.value = res.data.results || res.data
    const defaultAddr = addresses.value.find(a => a.is_default)
    if (defaultAddr) selectedAddressId.value = defaultAddr.id
    else if (addresses.value.length) selectedAddressId.value = addresses.value[0].id
  } catch {}
  loadingAddresses.value = false
})
</script>
