<template>
  <div class="space-y-5 max-w-full overflow-hidden">
    <div class="flex items-center justify-between flex-wrap gap-3">
      <div>
        <h1 class="text-xl sm:text-2xl font-bold text-white">Mijozlar Ro'yxati</h1>
        <p class="text-slate-400 text-xs sm:text-sm mt-0.5">{{ totalCount || customers.length }} ta mijoz</p>
      </div>
    </div>

    <!-- Search & Stats -->
    <div class="flex flex-col md:flex-row gap-3">
      <div class="flex-1 w-full bg-slate-800/90 rounded-2xl p-3 sm:p-4 border border-slate-700/80">
        <div class="relative w-full">
          <input
            v-model="search"
            @input="debounceFetch"
            type="text"
            placeholder="Ism, telefon yoki email bo'yicha qidirish..."
            class="bg-slate-700/80 text-slate-200 placeholder-slate-400 border border-slate-600 rounded-xl px-4 py-2.5 pl-10 w-full text-xs sm:text-sm focus:outline-none focus:ring-2 focus:ring-brand-500"
          />
          <Search class="absolute left-3 top-1/2 -translate-y-1/2 w-4 h-4 text-slate-400" />
        </div>
      </div>
      <!-- Quick stat cards -->
      <div class="grid grid-cols-2 sm:flex gap-2.5 sm:gap-3 w-full md:w-auto">
        <div class="bg-slate-800/90 rounded-2xl p-3 sm:px-5 sm:py-3.5 border border-slate-700/80 flex items-center gap-3 flex-1">
          <div class="w-8 h-8 bg-purple-500/15 rounded-xl flex items-center justify-center flex-shrink-0">
            <Users class="w-4 h-4 text-purple-400" />
          </div>
          <div class="min-w-0">
            <p class="text-slate-400 text-[11px] leading-tight truncate">Jami mijozlar</p>
            <p class="text-white font-bold text-base sm:text-lg leading-none mt-1">{{ totalCount || customers.length }}</p>
          </div>
        </div>
        <div class="bg-slate-800/90 rounded-2xl p-3 sm:px-5 sm:py-3.5 border border-slate-700/80 flex items-center gap-3 flex-1">
          <div class="w-8 h-8 bg-emerald-500/15 rounded-xl flex items-center justify-center flex-shrink-0">
            <TrendingUp class="w-4 h-4 text-emerald-400" />
          </div>
          <div class="min-w-0">
            <p class="text-slate-400 text-[11px] leading-tight truncate">Faol mijozlar</p>
            <p class="text-white font-bold text-base sm:text-lg leading-none mt-1">{{ activeCount }}</p>
          </div>
        </div>
      </div>
    </div>

    <!-- Table -->
    <div class="bg-slate-800/90 rounded-2xl border border-slate-700/80 overflow-hidden shadow-sm">
      <div v-if="loading" class="p-4 sm:p-6 space-y-3">
        <div v-for="i in 5" :key="i" class="skeleton h-14 rounded-xl bg-slate-700" />
      </div>
      <div v-else-if="!customers.length" class="py-16 text-center">
        <Users class="w-12 h-12 text-slate-600 mx-auto mb-3" />
        <p class="text-slate-400 text-sm">Mijozlar topilmadi</p>
      </div>
      <div v-else class="overflow-x-auto w-full">
        <table class="w-full text-sm text-left min-w-[640px]">
          <thead class="bg-slate-900/60 border-b border-slate-700/80">
            <tr>
              <th v-for="col in columns" :key="col" class="px-4 py-3 text-slate-400 font-medium text-xs uppercase tracking-wider whitespace-nowrap">{{ col }}</th>
            </tr>
          </thead>
          <tbody class="divide-y divide-slate-700/60">
            <template v-for="c in customers" :key="c.id">
              <!-- Main row -->
              <tr
                @click="toggleExpand(c)"
                class="hover:bg-slate-700/40 transition-colors cursor-pointer"
                :class="expandedId === c.id ? 'bg-brand-900/10' : ''"
              >
                <!-- Avatar + Name -->
                <td class="px-4 py-3.5">
                  <div class="flex items-center gap-3 min-w-[140px]">
                    <div class="w-9 h-9 rounded-xl flex items-center justify-center text-sm font-bold flex-shrink-0"
                         :class="c.orders_count > 0 ? 'bg-brand-900 text-brand-400' : 'bg-slate-700 text-slate-400'">
                      {{ c.full_name?.charAt(0)?.toUpperCase() || '?' }}
                    </div>
                    <div class="min-w-0">
                      <p class="font-semibold text-white truncate max-w-[150px]">{{ c.full_name || '—' }}</p>
                      <p v-if="c.email" class="text-slate-500 text-xs truncate max-w-[150px]">{{ c.email }}</p>
                    </div>
                  </div>
                </td>
                <!-- Phone -->
                <td class="px-4 py-3.5 whitespace-nowrap">
                  <div class="flex items-center gap-1.5 text-slate-300">
                    <Phone class="w-3.5 h-3.5 text-slate-500 flex-shrink-0" />
                    <span>{{ c.phone_number || '—' }}</span>
                  </div>
                </td>
                <!-- Orders count -->
                <td class="px-4 py-3.5 whitespace-nowrap">
                  <div class="flex items-center gap-2">
                    <span class="text-white font-semibold">{{ c.orders_count || 0 }}</span>
                    <span
                      v-if="c.orders_count > 0"
                      class="text-[10px] px-2 py-0.5 rounded-full font-medium"
                      :class="c.orders_count >= 5 ? 'bg-emerald-900/50 text-emerald-400 border border-emerald-500/30' : 'bg-brand-900/50 text-brand-400 border border-brand-500/30'"
                    >
                      {{ c.orders_count >= 5 ? 'Doimiy' : 'Yangi' }}
                    </span>
                  </div>
                </td>
                <!-- Total spent -->
                <td class="px-4 py-3.5 whitespace-nowrap">
                  <div>
                    <p class="font-semibold text-brand-400">{{ formatPrice(c.total_spent) }}</p>
                    <p v-if="c.avg_order_value" class="text-[11px] text-slate-500 mt-0.5">
                      o'rtacha: {{ formatPrice(c.avg_order_value) }}
                    </p>
                  </div>
                </td>
                <!-- Last order -->
                <td class="px-4 py-3.5 whitespace-nowrap">
                  <div v-if="c.last_order_date">
                    <p class="text-slate-300 text-xs">{{ formatDate(c.last_order_date) }}</p>
                    <span v-if="c.last_order_status" class="text-[10px] mt-0.5 inline-block px-2 py-0.5 rounded-full font-medium"
                          :class="statusBadgeSmall(c.last_order_status)">
                      {{ statusLabel(c.last_order_status) }}
                    </span>
                  </div>
                  <p v-else class="text-slate-500 text-xs">—</p>
                </td>
                <!-- Join date -->
                <td class="px-4 py-3.5 text-slate-400 text-xs whitespace-nowrap">{{ formatDate(c.date_joined) }}</td>
                <!-- Expand button -->
                <td class="px-4 py-3.5 text-right whitespace-nowrap">
                  <button class="w-7 h-7 inline-flex items-center justify-center rounded-lg bg-slate-700/80 hover:bg-brand-600 text-slate-400 hover:text-white transition-all">
                    <ChevronDown class="w-4 h-4 transition-transform duration-200" :class="expandedId === c.id ? 'rotate-180' : ''" />
                  </button>
                </td>
              </tr>

              <!-- Expanded detail -->
              <tr v-if="expandedId === c.id" class="bg-slate-900/40">
                <td colspan="7" class="px-4 pb-5 pt-2">
                  <div class="grid grid-cols-1 md:grid-cols-3 gap-4">

                    <!-- Profile info -->
                    <div class="bg-slate-800/80 rounded-xl p-4 border border-slate-700/60">
                      <p class="text-xs text-slate-500 mb-3 font-semibold uppercase tracking-wider">Profil ma'lumotlari</p>
                      <div class="space-y-2.5">
                        <div class="flex items-center gap-2">
                          <User class="w-3.5 h-3.5 text-slate-500 flex-shrink-0" />
                          <span class="text-xs text-slate-400">Ism:</span>
                          <span class="text-xs text-white font-medium">{{ c.full_name || '—' }}</span>
                        </div>
                        <div class="flex items-center gap-2">
                          <Phone class="w-3.5 h-3.5 text-slate-500 flex-shrink-0" />
                          <span class="text-xs text-slate-400">Telefon:</span>
                          <span class="text-xs text-white font-medium">{{ c.phone_number || '—' }}</span>
                        </div>
                        <div v-if="c.email" class="flex items-center gap-2">
                          <Mail class="w-3.5 h-3.5 text-slate-500 flex-shrink-0" />
                          <span class="text-xs text-slate-400">Email:</span>
                          <span class="text-xs text-white font-medium">{{ c.email }}</span>
                        </div>
                        <div v-if="c.username" class="flex items-center gap-2">
                          <AtSign class="w-3.5 h-3.5 text-slate-500 flex-shrink-0" />
                          <span class="text-xs text-slate-400">Login:</span>
                          <span class="text-xs text-white font-medium">{{ c.username }}</span>
                        </div>
                        <div class="flex items-center gap-2">
                          <Calendar class="w-3.5 h-3.5 text-slate-500 flex-shrink-0" />
                          <span class="text-xs text-slate-400">Ro'yxatdan:</span>
                          <span class="text-xs text-white font-medium">{{ formatDate(c.date_joined) }}</span>
                        </div>
                        <div v-if="c.last_login" class="flex items-center gap-2">
                          <Clock class="w-3.5 h-3.5 text-slate-500 flex-shrink-0" />
                          <span class="text-xs text-slate-400">Oxirgi kirish:</span>
                          <span class="text-xs text-white font-medium">{{ formatDate(c.last_login) }}</span>
                        </div>
                      </div>
                    </div>

                    <!-- Addresses -->
                    <div class="bg-slate-800/80 rounded-xl p-4 border border-slate-700/60">
                      <p class="text-xs text-slate-500 mb-3 font-semibold uppercase tracking-wider flex items-center gap-1.5">
                        <MapPin class="w-3.5 h-3.5" /> Manzillar
                      </p>
                      <div v-if="c.addresses && c.addresses.length" class="space-y-3">
                        <div
                          v-for="(addr, idx) in c.addresses"
                          :key="idx"
                          class="bg-slate-900/50 rounded-lg p-3 border border-slate-700/40 text-xs"
                        >
                          <div v-if="addr.is_default" class="flex items-center gap-1 text-brand-400 mb-1.5">
                            <Star class="w-3 h-3" /> <span class="font-medium">Asosiy manzil</span>
                          </div>
                          <p class="text-slate-200">
                            {{ [addr.region_display || addr.region, addr.city, addr.street, addr.house_number, addr.apartment, addr.full_address].filter(Boolean).join(', ') || '—' }}
                          </p>
                          <p v-if="addr.extra_info" class="text-slate-500 mt-1">{{ addr.extra_info }}</p>
                        </div>
                      </div>
                      <p v-else class="text-slate-500 text-xs">Manzil kiritilmagan</p>
                    </div>

                    <!-- Stats -->
                    <div class="bg-slate-800/80 rounded-xl p-4 border border-slate-700/60">
                      <p class="text-xs text-slate-500 mb-3 font-semibold uppercase tracking-wider">Xarid statistikasi</p>
                      <div class="space-y-3">
                        <div class="flex justify-between items-center">
                          <span class="text-xs text-slate-400">Jami buyurtmalar</span>
                          <span class="text-sm font-bold text-white">{{ c.orders_count || 0 }}</span>
                        </div>
                        <div class="flex justify-between items-center">
                          <span class="text-xs text-slate-400">Jami xarid summasi</span>
                          <span class="text-sm font-bold text-brand-400">{{ formatPrice(c.total_spent) }}</span>
                        </div>
                        <div v-if="c.avg_order_value" class="flex justify-between items-center">
                          <span class="text-xs text-slate-400">O'rtacha buyurtma</span>
                          <span class="text-sm font-semibold text-emerald-400">{{ formatPrice(c.avg_order_value) }}</span>
                        </div>
                        <div v-if="c.last_order_date" class="flex justify-between items-center">
                          <span class="text-xs text-slate-400">Oxirgi buyurtma</span>
                          <span class="text-xs text-slate-300">{{ formatDate(c.last_order_date) }}</span>
                        </div>
                        <!-- Activity bar -->
                        <div class="pt-2">
                          <div class="flex justify-between text-xs mb-1">
                            <span class="text-slate-500">Faollik</span>
                            <span class="text-slate-300">{{ activityLevel(c) }}</span>
                          </div>
                          <div class="h-2 bg-slate-700 rounded-full overflow-hidden">
                            <div
                              class="h-full rounded-full transition-all"
                              :class="activityColor(c)"
                              :style="{ width: activityPct(c) + '%' }"
                            />
                          </div>
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
import { Search, Users, User, Phone, Mail, MapPin, Calendar, Clock, ChevronDown, Star, TrendingUp, AtSign } from '@lucide/vue'
import { adminApi } from '@/api/admin'

const customers = ref([])
const loading = ref(true)
const search = ref('')
const expandedId = ref(null)
const page = ref(1)
const pageSize = 20
const totalCount = ref(0)
const totalPages = computed(() => Math.ceil(totalCount.value / pageSize))
const activeCount = computed(() => customers.value.filter(c => (c.orders_count || 0) > 0).length)

const columns = ['Mijoz', 'Telefon', 'Buyurtmalar', 'Jami xarid', 'Oxirgi buyurtma', "Qo'shilgan sana", '']

const statusOptions = [
  { value: 'pending', label: 'Kutilmoqda' },
  { value: 'processing', label: 'Tayyorlanmoqda' },
  { value: 'shipped', label: "Yo'lda" },
  { value: 'delivered', label: 'Yetkazildi' },
  { value: 'cancelled', label: 'Bekor qilindi' },
]

function statusLabel(s) { return statusOptions.find(o => o.value === s)?.label || s }
function statusBadgeSmall(s) {
  return {
    pending: 'bg-amber-900/50 text-amber-400',
    processing: 'bg-blue-900/50 text-blue-400',
    shipped: 'bg-purple-900/50 text-purple-400',
    delivered: 'bg-emerald-900/50 text-emerald-400',
    cancelled: 'bg-red-900/50 text-red-400',
  }[s] || 'bg-slate-700 text-slate-400'
}
function formatPrice(p) { return p ? new Intl.NumberFormat('uz-UZ', { maximumFractionDigits: 0 }).format(p) + ' so\'m' : '—' }
function formatDate(d) { return d ? new Date(d).toLocaleDateString('uz-UZ', { day: '2-digit', month: 'short', year: 'numeric' }) : '—' }

function activityLevel(c) {
  const n = c.orders_count || 0
  if (n === 0) return 'Faol emas'
  if (n < 3) return 'Past'
  if (n < 7) return "O'rta"
  return 'Yuqori'
}
function activityPct(c) {
  const n = c.orders_count || 0
  return Math.min(n * 10, 100)
}
function activityColor(c) {
  const n = c.orders_count || 0
  if (n === 0) return 'bg-slate-600'
  if (n < 3) return 'bg-amber-500'
  if (n < 7) return 'bg-brand-500'
  return 'bg-emerald-500'
}

function toggleExpand(c) {
  expandedId.value = expandedId.value === c.id ? null : c.id
}

async function fetchCustomers() {
  loading.value = true
  try {
    const params = { page: page.value, page_size: pageSize }
    if (search.value) params.search = search.value
    const res = await adminApi.getCustomers(params)
    customers.value = res.data.results || res.data
    totalCount.value = res.data.count || customers.value.length
  } catch {}
  loading.value = false
}

function setPage(p) { page.value = p; fetchCustomers() }

let debounceTimer
function debounceFetch() { clearTimeout(debounceTimer); debounceTimer = setTimeout(fetchCustomers, 400) }

onMounted(fetchCustomers)
</script>
