<template>
  <div class="space-y-5 max-w-full overflow-hidden">
    <div class="flex items-center justify-between flex-wrap gap-3">
      <div>
        <h1 class="text-xl sm:text-2xl font-bold text-white">Buyurtmalar Boshqaruvi</h1>
        <p class="text-slate-400 text-xs sm:text-sm mt-0.5">{{ totalCount }} ta buyurtma</p>
      </div>
    </div>

    <!-- Filters -->
    <div class="bg-slate-800/90 rounded-2xl p-3 sm:p-4 border border-slate-700/80 flex flex-col gap-3">
      <div class="w-full relative">
        <input
          v-model="search"
          @input="debounceFetch"
          type="text"
          placeholder="Buyurtma # yoki mijoz ismi/telefoni..."
          class="bg-slate-700/80 text-slate-200 placeholder-slate-400 border border-slate-600 rounded-xl px-4 py-2.5 pl-10 w-full text-xs sm:text-sm focus:outline-none focus:ring-2 focus:ring-brand-500"
        />
        <Search class="absolute left-3 top-1/2 -translate-y-1/2 w-4 h-4 text-slate-400" />
      </div>
      <div class="flex items-center gap-1.5 overflow-x-auto pb-1 sm:pb-0 sm:flex-wrap w-full scrollbar-none">
        <button
          v-for="s in ['all', ...statusOptions.map(s => s.value)]"
          :key="s"
          @click="filterStatus = s; fetchOrders()"
          class="px-3 py-1.5 sm:px-3.5 sm:py-2 rounded-xl text-xs sm:text-sm font-medium transition-all whitespace-nowrap flex-shrink-0"
          :class="filterStatus === s
            ? 'bg-brand-600 text-white shadow-sm'
            : 'bg-slate-700/80 text-slate-300 hover:bg-slate-600 hover:text-white'"
        >
          {{ s === 'all' ? 'Barchasi' : statusOptions.find(o => o.value === s)?.label }}
        </button>
      </div>
    </div>

    <!-- Table -->
    <div class="bg-slate-800/90 rounded-2xl border border-slate-700/80 overflow-hidden shadow-sm">
      <div v-if="loading" class="p-4 sm:p-6 space-y-3">
        <div v-for="i in 5" :key="i" class="skeleton h-14 rounded-xl bg-slate-700" />
      </div>

      <div v-else-if="!orders.length" class="py-16 text-center px-4">
        <ShoppingBag class="w-12 h-12 text-slate-600 mx-auto mb-3" />
        <p class="text-slate-400 text-sm">Buyurtmalar topilmadi</p>
      </div>

      <div v-else class="overflow-x-auto w-full">
        <table class="w-full text-sm text-left min-w-[700px]">
          <thead class="bg-slate-900/60 border-b border-slate-700/80">
            <tr>
              <th v-for="col in columns" :key="col" class="px-4 py-3 text-slate-400 font-medium text-xs uppercase tracking-wider whitespace-nowrap">
                {{ col }}
              </th>
            </tr>
          </thead>
          <tbody class="divide-y divide-slate-700/60">
            <template v-for="order in orders" :key="order.id">
              <!-- Order Row -->
              <tr
                @click="toggleDetail(order)"
                class="hover:bg-slate-700/40 transition-colors cursor-pointer"
                :class="expandedId === order.id ? 'bg-brand-900/10' : ''"
              >
                <td class="px-4 py-3.5 font-bold text-brand-400 whitespace-nowrap">#{{ order.order_number }}</td>
                <td class="px-4 py-3.5">
                  <div class="min-w-[130px]">
                    <p class="text-slate-200 font-medium truncate">{{ order.user_full_name }}</p>
                    <p class="text-slate-500 text-xs truncate">{{ order.user_phone }}</p>
                  </div>
                </td>
                <td class="px-4 py-3.5 text-slate-300 whitespace-nowrap">
                  <div class="flex items-center gap-1.5 text-xs text-slate-400">
                    <MapPin class="w-3.5 h-3.5 text-slate-500 flex-shrink-0" />
                    <span>{{ order.delivery_address?.region || '—' }}</span>
                  </div>
                </td>
                <td class="px-4 py-3.5 font-semibold text-white whitespace-nowrap">{{ formatPrice(order.total_amount) }}</td>
                <td class="px-4 py-3.5 whitespace-nowrap">
                  <span class="badge text-[10px] font-semibold" :class="statusBadge(order.status)">{{ statusLabel(order.status) }}</span>
                </td>
                <td class="px-4 py-3.5 text-slate-400 text-xs whitespace-nowrap">{{ formatDate(order.created_at) }}</td>
                <td class="px-4 py-3.5 text-right whitespace-nowrap" @click.stop>
                  <div class="flex items-center justify-end gap-1.5">
                    <select
                      :value="order.status"
                      @change="updateStatus(order, $event.target.value)"
                      class="bg-slate-700/90 text-slate-200 border border-slate-600 rounded-lg px-2.5 py-1 text-xs focus:outline-none focus:ring-1 focus:ring-brand-500 cursor-pointer"
                      :id="`admin-order-status-${order.id}`"
                    >
                      <option v-for="s in statusOptions" :key="s.value" :value="s.value">{{ s.label }}</option>
                    </select>
                    <button
                      @click="toggleDetail(order)"
                      class="w-7 h-7 inline-flex items-center justify-center rounded-lg bg-slate-700/80 hover:bg-brand-600 text-slate-400 hover:text-white transition-all"
                      :title="expandedId === order.id ? 'Yopish' : 'Batafsil'"
                    >
                      <ChevronDown class="w-4 h-4 transition-transform duration-200" :class="expandedId === order.id ? 'rotate-180' : ''" />
                    </button>
                  </div>
                </td>
              </tr>

              <!-- Expanded Detail Row -->
              <tr v-if="expandedId === order.id" class="bg-slate-900/40">
                <td colspan="7" class="px-3.5 sm:px-4 pb-5 pt-2">
                  <div v-if="detailLoading" class="flex items-center gap-3 py-4">
                    <div class="w-5 h-5 border-2 border-brand-500 border-t-transparent rounded-full animate-spin" />
                    <span class="text-slate-400 text-sm">Yuklanmoqda...</span>
                  </div>

                  <div v-else class="grid grid-cols-1 lg:grid-cols-3 gap-3 sm:gap-4 mt-1">
                    <!-- Customer + Address -->
                    <div class="space-y-3">
                      <!-- Customer -->
                      <div class="bg-slate-800/80 rounded-xl p-4 border border-slate-700/60">
                        <p class="text-xs text-slate-500 mb-3 font-semibold uppercase tracking-wider flex items-center gap-1.5">
                          <User class="w-3.5 h-3.5" /> Buyurtmachi
                        </p>
                        <div class="flex items-center gap-3">
                          <div class="w-10 h-10 bg-brand-900 rounded-xl flex items-center justify-center text-brand-400 font-bold text-sm flex-shrink-0">
                            {{ order.user_full_name?.charAt(0)?.toUpperCase() || '?' }}
                          </div>
                          <div>
                            <p class="font-semibold text-white text-sm">{{ order.user_full_name || '—' }}</p>
                            <p class="text-slate-400 text-xs mt-0.5">{{ order.user_phone || '—' }}</p>
                          </div>
                        </div>
                      </div>

                      <!-- Address -->
                      <div class="bg-slate-800/80 rounded-xl p-4 border border-slate-700/60">
                        <p class="text-xs text-slate-500 mb-3 font-semibold uppercase tracking-wider flex items-center gap-1.5">
                          <MapPin class="w-3.5 h-3.5" /> Yetkazib berish manzili
                        </p>
                        <div v-if="orderDetail?.delivery_address" class="space-y-1.5">
                          <div v-for="[label, key] in addressFields" :key="key" class="flex gap-2 text-xs">
                            <span class="text-slate-500 w-18 flex-shrink-0">{{ label }}:</span>
                            <span class="text-slate-200">{{ orderDetail.delivery_address[key] || '—' }}</span>
                          </div>
                        </div>
                        <p v-else class="text-slate-500 text-xs">Manzil ko'rsatilmagan</p>
                      </div>
                    </div>

                    <!-- Products -->
                    <div class="md:col-span-2">
                      <div class="bg-slate-800/80 rounded-xl p-4 border border-slate-700/60 h-full">
                        <p class="text-xs text-slate-500 mb-3 font-semibold uppercase tracking-wider flex items-center gap-1.5">
                          <Package class="w-3.5 h-3.5" /> Buyurtma tarkibi
                        </p>

                        <div v-if="orderItems.length" class="space-y-3">
                          <div
                            v-for="item in orderItems"
                            :key="item.id"
                            class="flex gap-3 bg-slate-900/50 rounded-xl p-3 border border-slate-700/40"
                          >
                            <!-- Image -->
                            <div class="w-16 h-16 rounded-lg overflow-hidden bg-slate-700 flex-shrink-0">
                              <img
                                v-if="item.main_image"
                                :src="item.main_image"
                                :alt="item.product_name"
                                class="w-full h-full object-cover"
                              />
                              <div v-else class="w-full h-full flex items-center justify-center">
                                <Package class="w-6 h-6 text-slate-500" />
                              </div>
                            </div>

                            <div class="flex-1 min-w-0">
                              <p class="font-semibold text-white text-sm">{{ item.product_name || '—' }}</p>

                              <!-- Color & Size badges -->
                              <div class="flex flex-wrap gap-2 mt-1.5">
                                <div v-if="item.color_name || item.color_hex" class="flex items-center gap-1.5 bg-slate-700/60 rounded-lg px-2 py-1">
                                  <div
                                    class="w-3 h-3 rounded-full border border-slate-500 flex-shrink-0"
                                    :style="{ backgroundColor: item.color_hex || '#888' }"
                                  />
                                  <span class="text-xs text-slate-300">{{ item.color_name }}</span>
                                </div>
                                <div v-if="item.width_mm || item.height_mm" class="flex items-center gap-1 bg-slate-700/60 rounded-lg px-2 py-1">
                                  <span class="text-xs text-slate-400">O'lcham:</span>
                                  <span class="text-xs font-medium text-slate-200">
                                    {{ item.width_mm }}×{{ item.height_mm }} mm
                                    <span v-if="item.sqm" class="text-slate-500">({{ item.sqm }} m²)</span>
                                  </span>
                                </div>
                              </div>

                              <div class="flex items-center justify-between mt-2">
                                <span class="text-xs text-slate-500">
                                  {{ item.quantity }} dona × {{ formatPrice(item.unit_price) }}
                                </span>
                                <span class="text-sm font-bold text-emerald-400">
                                  {{ formatPrice(item.total_price) }}
                                </span>
                              </div>
                            </div>
                          </div>
                        </div>
                        <p v-else class="text-slate-500 text-sm">Mahsulotlar topilmadi</p>

                        <!-- Totals -->
                        <div class="mt-4 pt-4 border-t border-slate-700/70 space-y-1.5">
                          <div v-if="orderDetail?.delivery_fee" class="flex justify-between text-sm">
                            <span class="text-slate-400">Yetkazib berish:</span>
                            <span class="text-slate-200">{{ formatPrice(orderDetail.delivery_fee) }}</span>
                          </div>
                          <div v-if="orderDetail?.discount_amount" class="flex justify-between text-sm">
                            <span class="text-slate-400">Chegirma:</span>
                            <span class="text-red-400">-{{ formatPrice(orderDetail.discount_amount) }}</span>
                          </div>
                          <div class="flex justify-between font-bold text-base">
                            <span class="text-white">Jami to'lov:</span>
                            <span class="text-brand-400">{{ formatPrice(order.total_amount) }}</span>
                          </div>
                          <div v-if="orderDetail?.payment_method" class="flex gap-2 text-xs pt-1">
                            <span class="text-slate-500">To'lov usuli:</span>
                            <span class="text-slate-300">{{ orderDetail.payment_method }}</span>
                          </div>
                        </div>

                        <!-- Notes -->
                        <div v-if="orderDetail?.notes || orderDetail?.comment" class="mt-3 p-3 bg-amber-950/30 border border-amber-700/40 rounded-xl">
                          <p class="text-xs text-amber-400 font-medium mb-1">Izoh:</p>
                          <p class="text-slate-300 text-xs">{{ orderDetail?.notes || orderDetail?.comment }}</p>
                        </div>
                      </div>
                    </div>
                  </div>
                </td>
              </tr>
            </template>
          </tbody>
        </table>
      </div>

      <!-- Pagination -->
      <div v-if="totalPages > 1" class="flex justify-center items-center gap-2 p-4 border-t border-slate-700">
        <button @click="setPage(page - 1)" :disabled="page <= 1" class="px-3 py-1.5 rounded-lg bg-slate-700 text-slate-300 hover:bg-slate-600 disabled:opacity-50 text-sm">‹</button>
        <span class="text-slate-400 text-sm">{{ page }} / {{ totalPages }}</span>
        <button @click="setPage(page + 1)" :disabled="page >= totalPages" class="px-3 py-1.5 rounded-lg bg-slate-700 text-slate-300 hover:bg-slate-600 disabled:opacity-50 text-sm">›</button>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { Search, ShoppingBag, MapPin, User, Package, ChevronDown } from '@lucide/vue'
import { adminApi } from '@/api/admin'
import { useAlertStore } from '@/stores/alert'

const alertStore = useAlertStore()
const orders = ref([])
const loading = ref(true)
const search = ref('')
const filterStatus = ref('all')
const page = ref(1)
const pageSize = 20
const totalCount = ref(0)
const totalPages = computed(() => Math.ceil(totalCount.value / pageSize))

// Detail expand
const expandedId = ref(null)
const orderDetail = ref(null)
const detailLoading = ref(false)
const orderItems = computed(() => {
  const d = orderDetail.value
  if (!d) return []
  return d.items || d.order_items || d.products || []
})

const addressFields = [
  ['Viloyat', 'region_display'],
  ['Shahar/Tuman', 'city'],
  ["Ko'cha", 'street'],
  ['Uy raqami', 'house_number'],
  ['Xonadon', 'apartment'],
  ['To\'liq manzil', 'full_address'],
]

const columns = ['Buyurtma #', 'Mijoz', 'Manzil', 'Summa', 'Holat', 'Sana', 'Amal']

const statusOptions = [
  { value: 'pending', label: 'Kutilmoqda' },
  { value: 'processing', label: 'Tayyorlanmoqda' },
  { value: 'shipped', label: "Yo'lda" },
  { value: 'delivered', label: 'Yetkazildi' },
  { value: 'cancelled', label: 'Bekor qilindi' },
]

function statusLabel(s) { return statusOptions.find(o => o.value === s)?.label || s }
function statusBadge(s) {
  return { pending: 'badge-amber', processing: 'badge-blue', shipped: 'badge-purple', delivered: 'badge-green', cancelled: 'badge-red' }[s] || 'badge-slate'
}
function formatPrice(p) { return p ? new Intl.NumberFormat('uz-UZ', { maximumFractionDigits: 0 }).format(p) + ' so\'m' : '—' }
function formatDate(d) { return d ? new Date(d).toLocaleDateString('uz-UZ', { day: '2-digit', month: 'short', year: 'numeric' }) : '—' }

async function toggleDetail(order) {
  if (expandedId.value === order.id) {
    expandedId.value = null
    orderDetail.value = null
    return
  }
  expandedId.value = order.id
  orderDetail.value = null
  detailLoading.value = true
  try {
    const res = await adminApi.getOrder(order.id)
    orderDetail.value = res.data
  } catch {
    orderDetail.value = order
  }
  detailLoading.value = false
}

async function fetchOrders() {
  loading.value = true
  try {
    const params = { page: page.value, page_size: pageSize, ordering: '-created_at' }
    if (search.value) params.search = search.value
    if (filterStatus.value !== 'all') params.status = filterStatus.value
    const res = await adminApi.getOrders(params)
    orders.value = res.data.results || res.data
    totalCount.value = res.data.count || orders.value.length
  } catch {}
  loading.value = false
}

async function updateStatus(order, newStatus) {
  try {
    await adminApi.updateOrderStatus(order.id, { status: newStatus })
    order.status = newStatus
    alertStore.success('Holat yangilandi')
  } catch { alertStore.error('Xatolik') }
}

function setPage(p) {
  page.value = p
  fetchOrders()
}

let debounceTimer
function debounceFetch() {
  clearTimeout(debounceTimer)
  debounceTimer = setTimeout(fetchOrders, 400)
}

onMounted(() => {
  const saved = localStorage.getItem('admin-order-filter')
  if (saved) { filterStatus.value = saved; localStorage.removeItem('admin-order-filter') }
  fetchOrders()
})
</script>
