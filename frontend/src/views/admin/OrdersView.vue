<template>
  <div class="space-y-6">
    <div class="flex items-center justify-between flex-wrap gap-4">
      <div>
        <h1 class="text-2xl font-bold text-white">Buyurtmalar Boshqaruvi</h1>
        <p class="text-slate-400 text-sm mt-1">{{ totalCount }} ta buyurtma</p>
      </div>
    </div>

    <!-- Filters -->
    <div class="bg-slate-800 rounded-2xl p-4 border border-slate-700 flex flex-wrap gap-3">
      <div class="flex-1 min-w-[200px] relative">
        <input
          v-model="search"
          @input="debounceFetch"
          type="text"
          placeholder="Buyurtma # yoki mijoz..."
          class="bg-slate-700 text-slate-200 border border-slate-600 rounded-xl px-4 py-2.5 pl-10 w-full text-sm focus:outline-none focus:ring-2 focus:ring-brand-500"
        />
        <Search class="absolute left-3 top-1/2 -translate-y-1/2 w-4 h-4 text-slate-400" />
      </div>
      <div class="flex flex-wrap gap-2">
        <button
          v-for="s in ['all', ...statusOptions.map(s => s.value)]"
          :key="s"
          @click="filterStatus = s; fetchOrders()"
          class="px-4 py-2 rounded-xl text-sm font-medium transition-all"
          :class="filterStatus === s
            ? 'bg-brand-600 text-white'
            : 'bg-slate-700 text-slate-300 hover:bg-slate-600'"
        >
          {{ s === 'all' ? 'Barchasi' : statusOptions.find(o => o.value === s)?.label }}
        </button>
      </div>
    </div>

    <!-- Table -->
    <div class="bg-slate-800 rounded-2xl border border-slate-700 overflow-hidden">
      <div v-if="loading" class="p-6 space-y-3">
        <div v-for="i in 6" :key="i" class="skeleton h-14 rounded-xl bg-slate-700" />
      </div>

      <div v-else-if="!orders.length" class="py-16 text-center">
        <ShoppingBag class="w-12 h-12 text-slate-600 mx-auto mb-3" />
        <p class="text-slate-400">Buyurtmalar topilmadi</p>
      </div>

      <div v-else class="overflow-x-auto">
        <table class="w-full text-sm">
          <thead class="bg-slate-900/50">
            <tr>
              <th v-for="col in columns" :key="col" class="text-left px-4 py-3 text-slate-400 font-medium text-xs uppercase tracking-wider">
                {{ col }}
              </th>
            </tr>
          </thead>
          <tbody class="divide-y divide-slate-700">
            <tr v-for="order in orders" :key="order.id" class="hover:bg-slate-700/50 transition-colors">
              <td class="px-4 py-4 font-bold text-brand-400">#{{ order.order_number }}</td>
              <td class="px-4 py-4">
                <div>
                  <p class="text-slate-200 font-medium">{{ order.user_full_name }}</p>
                  <p class="text-slate-500 text-xs">{{ order.user_phone }}</p>
                </div>
              </td>
              <td class="px-4 py-4 text-slate-300">
                <div class="flex items-center gap-1.5 text-xs text-slate-400">
                  <MapPin class="w-3.5 h-3.5" />
                  {{ order.delivery_address?.region }}
                </div>
              </td>
              <td class="px-4 py-4 font-semibold text-white">{{ formatPrice(order.total_amount) }}</td>
              <td class="px-4 py-4">
                <span class="badge" :class="statusBadge(order.status)">{{ statusLabel(order.status) }}</span>
              </td>
              <td class="px-4 py-4 text-slate-400 text-xs">{{ formatDate(order.created_at) }}</td>
              <td class="px-4 py-4">
                <select
                  :value="order.status"
                  @change="updateStatus(order, $event.target.value)"
                  class="bg-slate-700 text-slate-300 border border-slate-600 rounded-lg px-2 py-1 text-xs"
                  :id="`admin-order-status-${order.id}`"
                >
                  <option v-for="s in statusOptions" :key="s.value" :value="s.value">{{ s.label }}</option>
                </select>
              </td>
            </tr>
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
import { Search, ShoppingBag, MapPin } from '@lucide/vue'
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
function formatPrice(p) { return p ? new Intl.NumberFormat('uz-UZ', { style: 'currency', currency: 'UZS', maximumFractionDigits: 0 }).format(p) : '—' }
function formatDate(d) { return new Date(d).toLocaleDateString('uz-UZ', { day: '2-digit', month: 'short', year: 'numeric' }) }

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

onMounted(fetchOrders)
</script>
