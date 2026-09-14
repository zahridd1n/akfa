<template>
  <div class="space-y-6">
    <!-- Page Title -->
    <div class="flex flex-wrap items-center justify-between gap-4">
      <div>
        <h1 class="text-2xl font-bold text-white mb-1">Dashboard</h1>
        <p class="text-slate-400 text-sm">Saramax savdo statistikasi va ko'rsatkichlari</p>
      </div>
      <div class="flex items-center gap-2 text-sm text-slate-400">
        <Clock class="w-4 h-4" />
        <span>{{ todayLabel }}</span>
      </div>
    </div>

    <!-- Error alert -->
    <div v-if="error" class="bg-red-950/40 border border-red-500/30 rounded-2xl p-4 flex items-start gap-3">
      <AlertTriangle class="w-5 h-5 text-red-400 flex-shrink-0 mt-0.5" />
      <div class="flex-1">
        <p class="text-red-300 font-semibold text-sm">Ma'lumotlarni yuklab bo'lmadi</p>
        <p class="text-red-400 text-sm mt-1">{{ error }}</p>
      </div>
      <button @click="loadDashboard" class="btn-sm btn-outline text-red-300 border-red-500/40 hover:bg-red-500/10">
        Qayta yuklash
      </button>
    </div>

    <!-- KPI Cards -->
    <div v-if="loading" class="grid grid-cols-1 sm:grid-cols-2 xl:grid-cols-4 gap-4">
      <div v-for="i in 4" :key="i" class="skeleton h-32 rounded-2xl bg-slate-800" />
    </div>

    <div v-else class="grid grid-cols-1 sm:grid-cols-2 xl:grid-cols-4 gap-4">
      <div
        v-for="card in kpiCards"
        :key="card.label"
        class="group relative overflow-hidden rounded-2xl border border-slate-700/60 bg-gradient-to-br p-5 transition-all duration-300 hover:-translate-y-0.5 hover:border-slate-500"
        :class="card.cardBg"
      >
        <div class="absolute -top-6 -right-6 w-20 h-20 rounded-full opacity-20 blur-2xl" :class="card.glow" />
        <div class="flex items-start justify-between mb-4 relative">
          <p class="text-slate-300 text-sm font-medium">{{ card.label }}</p>
          <div class="w-10 h-10 rounded-xl flex items-center justify-center backdrop-blur-sm" :class="card.iconBg">
            <component :is="card.icon" class="w-5 h-5" :class="card.iconColor" />
          </div>
        </div>
        <p class="text-[26px] font-bold text-white leading-tight relative">{{ card.value }}</p>
        <div class="mt-3 flex items-center gap-1.5 text-xs relative">
          <span :class="card.change > 0 ? 'text-emerald-400' : 'text-red-400'" class="font-semibold">
            {{ card.change > 0 ? '▲' : '▼' }} {{ Math.abs(card.change) }}%
          </span>
          <span class="text-slate-500">bu oy o`tgan oyga nisbatan</span>
        </div>
      </div>
    </div>

    <!-- Charts Row -->
    <div class="grid grid-cols-1 xl:grid-cols-3 gap-6">
      <!-- Sales Chart -->
      <div class="xl:col-span-2 bg-slate-800/60 rounded-2xl p-6 border border-slate-700/60 backdrop-blur-sm">
        <div class="flex items-center justify-between mb-6">
          <div>
            <h2 class="font-bold text-white">Savdo Dinamikasi</h2>
            <p class="text-slate-500 text-xs mt-0.5">Daromad bo'yicha oylik statistika</p>
          </div>
          <div class="flex gap-1.5 bg-slate-900/60 rounded-xl p-1 border border-slate-700/60">
            <button
              v-for="opt in chartPeriods"
              :key="opt.value"
              @click="chartPeriod = opt.value"
              class="px-3 py-1.5 rounded-lg text-xs font-medium transition-colors"
              :class="chartPeriod === opt.value
                ? 'bg-brand-500/20 text-brand-300 border border-brand-500/40'
                : 'text-slate-400 hover:text-slate-200 border border-transparent'"
            >
              {{ opt.label }}
            </button>
          </div>
        </div>
        <div class="h-64 relative">
          <div v-if="chartEmpty" class="absolute inset-0 flex flex-col items-center justify-center text-slate-500">
            <BarChart3 class="w-8 h-8 mb-2 opacity-40" />
            <p class="text-sm">Hali savdo ma'lumotlari yo'q</p>
          </div>
          <canvas v-show="!chartEmpty" ref="salesChartRef" />
        </div>
      </div>

      <!-- Order Status Breakdown -->
      <div class="bg-slate-800/60 rounded-2xl p-6 border border-slate-700/60 backdrop-blur-sm">
        <h2 class="font-bold text-white mb-6">Buyurtmalar Holati</h2>
        <div class="space-y-4">
          <div
            v-for="item in orderStatusData"
            :key="item.label"
            class="flex items-center gap-3 group cursor-pointer"
            @click="filterByStatus(item.status)"
          >
            <div class="w-3 h-3 rounded-full flex-shrink-0 transition-transform group-hover:scale-125" :style="{ backgroundColor: item.color, boxShadow: `0 0 12px ${item.color}66` }" />
            <div class="flex-1 min-w-0">
              <div class="flex justify-between text-sm mb-1.5">
                <span class="text-slate-300">{{ item.label }}</span>
                <span class="font-bold text-white">{{ item.count }}</span>
              </div>
              <div class="h-2 bg-slate-700/70 rounded-full overflow-hidden">
                <div
                  class="h-full rounded-full transition-all duration-1000"
                  :style="{ width: item.pct + '%', backgroundColor: item.color }"
                />
              </div>
            </div>
            <span class="text-xs text-slate-500 w-9 text-right">{{ item.pct }}%</span>
          </div>
        </div>

        <div class="mt-6 pt-6 border-t border-slate-700/70">
          <div class="flex items-center justify-between">
            <div>
              <p class="text-slate-500 text-xs">Umumiy buyurtma</p>
              <p class="text-xl font-bold text-white">{{ totalOrders }}</p>
            </div>
            <div class="text-right">
              <p class="text-slate-500 text-xs">Kutilmoqda</p>
              <p class="text-xl font-bold text-amber-400">{{ pendingOrders }}</p>
            </div>
            <div class="text-right">
              <p class="text-slate-500 text-xs">Bugun</p>
              <p class="text-xl font-bold text-brand-400">{{ todayOrders }}</p>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- Latest Orders + Top Products -->
    <div class="grid grid-cols-1 xl:grid-cols-3 gap-6">
      <!-- Latest Orders -->
      <div class="xl:col-span-2 bg-slate-800/60 rounded-2xl p-6 border border-slate-700/60 backdrop-blur-sm">
        <div class="flex items-center justify-between mb-6">
          <div>
            <h2 class="font-bold text-white">So'nggi Buyurtmalar</h2>
            <p class="text-slate-500 text-xs mt-0.5">Oxirgi 10 ta buyurtma</p>
          </div>
          <router-link to="/admin/orders" class="flex items-center gap-1 text-brand-400 text-sm font-medium hover:text-brand-300 transition-colors">
            Barchasi <ChevronRight class="w-4 h-4" />
          </router-link>
        </div>

        <div v-if="loadingOrders" class="space-y-3">
          <div v-for="i in 5" :key="i" class="skeleton h-12 rounded-xl bg-slate-700" />
        </div>

        <div v-else-if="latestOrders.length === 0" class="py-10 text-center text-slate-500">
          <ShoppingBag class="w-8 h-8 mx-auto mb-3 opacity-40" />
          <p class="text-sm">Hali buyurtmalar yo'q</p>
        </div>

        <div v-else class="overflow-x-auto -mx-2">
          <table class="w-full text-sm">
            <thead>
              <tr class="text-left">
                <th class="pb-3 px-2 text-slate-500 font-medium text-xs uppercase tracking-wider">Buyurtma #</th>
                <th class="pb-3 px-2 text-slate-500 font-medium text-xs uppercase tracking-wider">Mijoz</th>
                <th class="pb-3 px-2 text-slate-500 font-medium text-xs uppercase tracking-wider">Summa</th>
                <th class="pb-3 px-2 text-slate-500 font-medium text-xs uppercase tracking-wider">Holat</th>
                <th class="pb-3 px-2 text-slate-500 font-medium text-xs uppercase tracking-wider">Sana</th>
                <th class="pb-3 px-2" />
              </tr>
            </thead>
            <tbody class="divide-y divide-slate-700/60">
              <tr v-for="order in latestOrders" :key="order.id" class="hover:bg-slate-700/30 transition-colors group">
                <td class="py-3 px-2 font-bold text-brand-400">#{{ order.order_number }}</td>
                <td class="py-3 px-2 text-slate-300">{{ order.user_full_name || order.user_name }}</td>
                <td class="py-3 px-2 text-white font-medium whitespace-nowrap">
                  <span class="inline-flex items-center gap-1.5 text-slate-200">
                    {{ formatPrice(order.total_amount) }}
                  </span>
                </td>
                <td class="py-3 px-2">
                  <span class="badge inline-flex items-center gap-1.5" :class="statusBadgeClass(order.status)">
                    <span class="w-1.5 h-1.5 rounded-full" :class="statusDotClass(order.status)" />
                    {{ statusLabel(order.status) }}
                  </span>
                </td>
                <td class="py-3 px-2 text-slate-500 text-xs">{{ formatDate(order.created_at) }}</td>
                <td class="py-3 px-2">
                  <select
                    :value="order.status"
                    @change="updateStatus(order, $event.target.value)"
                    class="bg-slate-900/80 text-slate-300 border border-slate-600/70 rounded-lg px-2.5 py-1.5 text-xs focus:outline-none focus:border-brand-500/60 cursor-pointer"
                    :id="`order-status-${order.id}`"
                  >
                    <option v-for="s in statusOptions" :key="s.value" :value="s.value">{{ s.label }}</option>
                  </select>
                </td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>

      <!-- Top Products -->
      <div class="bg-slate-800/60 rounded-2xl p-6 border border-slate-700/60 backdrop-blur-sm">
        <h2 class="font-bold text-white mb-6">Top Mahsulotlar</h2>
        <div v-if="!topProducts.length" class="py-10 text-center text-slate-500">
          <Package class="w-8 h-8 mx-auto mb-3 opacity-40" />
          <p class="text-sm">Hali sotilgan mahsulotlar yo'q</p>
        </div>
        <div v-else class="space-y-4">
          <div
            v-for="(product, index) in topProducts"
            :key="product.product__id"
            class="flex items-center gap-3 p-3 rounded-xl border border-slate-700/50 bg-slate-900/30 hover:border-slate-600 transition-colors"
          >
            <div class="w-8 h-8 rounded-lg flex items-center justify-center text-sm font-bold flex-shrink-0"
              :class="['bg-brand-500/20 text-brand-300', 'bg-purple-500/20 text-purple-300', 'bg-amber-500/20 text-amber-300'][index % 3]">
              {{ index + 1 }}
            </div>
            <div class="flex-1 min-w-0">
              <p class="text-sm font-medium text-white truncate">{{ product.product__name }}</p>
              <p class="text-xs text-slate-500">{{ product.total_qty }} dona sotilgan</p>
            </div>
            <p class="text-sm font-semibold text-emerald-400 whitespace-nowrap">{{ formatPrice(product.total_revenue) }}</p>
          </div>
        </div>

        <div class="mt-6 pt-6 border-t border-slate-700/70">
          <div class="flex items-center justify-between">
            <div>
              <p class="text-slate-500 text-xs">Oylik daromad</p>
              <p class="text-lg font-bold text-emerald-400">{{ formatPrice(monthlyRevenue) }}</p>
            </div>
            <div class="text-right">
              <p class="text-slate-500 text-xs">Faol mahsulotlar</p>
              <p class="text-lg font-bold text-white">{{ totalProducts }}</p>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, watch, onMounted, nextTick } from 'vue'
import { ChevronRight, ShoppingBag, Users, Package, TrendingUp, Clock, AlertTriangle, BarChart3 } from '@lucide/vue'
import { Chart, registerables } from 'chart.js'
import { adminApi } from '@/api/admin'
import { useAlertStore } from '@/stores/alert'

Chart.register(...registerables)

const alertStore = useAlertStore()
const loading = ref(true)
const loadingOrders = ref(true)
const error = ref(null)
const chartPeriod = ref('month')
const salesChartRef = ref(null)
let chartInstance = null

const dashboardData = ref(null)
const latestOrders = ref([])
const topProducts = ref([])
const kpiCards = ref([])
const orderStatusData = ref([])

const chartPeriods = [
  { value: 'month', label: 'Oylik' },
  { value: 'week', label: 'Haftalik' },
]

function todayLabel() {
  return new Date().toLocaleDateString('uz-UZ', { weekday: 'long', year: 'numeric', month: 'long', day: 'numeric' })
}

const todayOrders = computed(() => dashboardData.value?.today_orders || 0)
const pendingOrders = computed(() => dashboardData.value?.pending_orders || 0)
const totalOrders = computed(() => dashboardData.value?.total_orders || 0)
const totalProducts = computed(() => dashboardData.value?.total_products || 0)
const monthlyRevenue = computed(() => dashboardData.value?.monthly_revenue || 0)
const chartEmpty = computed(() => !(dashboardData.value?.sales_chart?.length))

const statusOptions = [
  { value: 'pending', label: 'Kutilmoqda' },
  { value: 'processing', label: 'Tayyorlanmoqda' },
  { value: 'shipped', label: "Yo'lda" },
  { value: 'delivered', label: 'Yetkazildi' },
  { value: 'cancelled', label: 'Bekor qilindi' },
]

function statusLabel(s) {
  return statusOptions.find(o => o.value === s)?.label || s
}
function statusBadgeClass(s) {
  const map = { pending: 'badge-amber', processing: 'badge-blue', shipped: 'badge-purple', delivered: 'badge-green', cancelled: 'badge-red' }
  return map[s] || 'badge-slate'
}
function statusDotClass(s) {
  const map = { pending: 'bg-amber-400', processing: 'bg-blue-400', shipped: 'bg-purple-400', delivered: 'bg-emerald-400', cancelled: 'bg-red-400' }
  return map[s] || 'bg-slate-400'
}
function formatPrice(price) {
  if (!price) return '0 so\'m'
  return new Intl.NumberFormat('uz-UZ', { currency: 'UZS', maximumFractionDigits: 0 }).format(price) + ' so\'m'
}
function formatDate(d) {
  return new Date(d).toLocaleDateString('uz-UZ', { day: '2-digit', month: 'short', year: 'numeric' })
}

function filterByStatus(status) {
  localStorage.setItem('admin-order-filter', status)
  window.location.href = '/admin/orders'
}

async function updateStatus(order, newStatus) {
  try {
    await adminApi.updateOrderStatus(order.id, { status: newStatus })
    order.status = newStatus
    alertStore.success('Holat yangilandi')
    loadDashboard()
  } catch {
    alertStore.error('Xatolik yuz berdi')
  }
}

function buildKPIs(data) {
  const changes = data.changes || {}
  kpiCards.value = [
    {
      label: 'Jami Buyurtmalar', value: data.total_orders || 0,
      icon: ShoppingBag, cardBg: 'from-blue-950/40 to-slate-800/40', glow: 'bg-blue-500',
      iconBg: 'bg-blue-500/15', iconColor: 'text-blue-400', change: changes.total_orders ?? 0,
    },
    {
      label: "Oylik Tushum", value: formatPrice(data.monthly_revenue),
      icon: TrendingUp, cardBg: 'from-emerald-950/40 to-slate-800/40', glow: 'bg-emerald-500',
      iconBg: 'bg-emerald-500/15', iconColor: 'text-emerald-400', change: changes.monthly_revenue ?? 0,
    },
    {
      label: 'Jami Mijozlar', value: data.total_customers || 0,
      icon: Users, cardBg: 'from-purple-950/40 to-slate-800/40', glow: 'bg-purple-500',
      iconBg: 'bg-purple-500/15', iconColor: 'text-purple-400', change: changes.total_customers ?? 0,
    },
    {
      label: 'Jami Mahsulotlar', value: data.total_products || 0,
      icon: Package, cardBg: 'from-amber-950/40 to-slate-800/40', glow: 'bg-amber-500',
      iconBg: 'bg-amber-500/15', iconColor: 'text-amber-400', change: changes.total_products ?? 0,
    },
  ]
}

function buildStatusData(data) {
  const statusMap = data.order_by_status || {}
  const total = Object.values(statusMap).reduce((s, v) => s + (typeof v === 'object' ? (v.count || 0) : v), 0) || 1
  const colors = { pending: '#F59E0B', processing: '#3B82F6', shipped: '#8B5CF6', delivered: '#10B981', cancelled: '#EF4444' }
  orderStatusData.value = statusOptions.map(s => {
    const raw = statusMap[s.value]
    const count = typeof raw === 'object' ? (raw.count || 0) : (raw || 0)
    return {
      label: s.label,
      status: s.value,
      count,
      pct: Math.round((count / total) * 100),
      color: colors[s.value],
    }
  })
}

function buildSalesChart(data) {
  if (!salesChartRef.value) return
  if (chartInstance) chartInstance.destroy()
  chartInstance = null

  const salesChart = data.sales_chart || []
  if (!salesChart.length) return

  const months = ['Yan', 'Fev', 'Mar', 'Apr', 'May', 'Iyn', 'Iyl', 'Avg', 'Sen', 'Okt', 'Noy', 'Dek']
  const labels = salesChart.map(d => {
    const raw = d.month || d.label || ''
    if (chartPeriod.value === 'week') {
      const dt = new Date(raw)
      if (!isNaN(dt)) return `${dt.getDate()}.${dt.getMonth() + 1}.${String(dt.getFullYear()).slice(2)}`
      return raw
    }
    const [y, m] = raw.split('-')
    return months[parseInt(m) - 1] ? `${months[parseInt(m) - 1]} ${y}` : raw
  })
  const values = salesChart.map(d => d.revenue || d.amount || 0)

  chartInstance = new Chart(salesChartRef.value, {
    type: 'bar',
    data: {
      labels,
      datasets: [{
        label: 'Tushum',
        data: values,
        backgroundColor: ctx => {
          const { chart } = ctx
          const { ctx: c } = chart
          const g = c.createLinearGradient(0, 0, 0, 260)
          g.addColorStop(0, 'rgba(37,99,235,0.9)')
          g.addColorStop(1, 'rgba(37,99,235,0.1)')
          return g
        },
        borderColor: 'rgba(37,99,235,0.8)',
        borderWidth: 1,
        borderRadius: 8,
        borderSkipped: false,
        hoverBackgroundColor: 'rgba(59,130,246,0.95)',
      }],
    },
    options: {
      responsive: true,
      maintainAspectRatio: false,
      plugins: {
        legend: { display: false },
        tooltip: {
          backgroundColor: '#0F172A',
          borderColor: '#334155',
          borderWidth: 1,
          titleColor: '#94A3B8',
          bodyColor: '#E2E8F0',
          padding: 12,
          cornerRadius: 10,
          callbacks: {
            label: ctx => `Tushum: ${formatPrice(ctx.parsed.y)}`,
          },
        },
      },
      scales: {
        x: {
          grid: { color: 'rgba(51,65,85,0.4)' },
          ticks: { color: '#94A3B8', font: { size: 11 }, maxRotation: 0 },
          border: { color: '#334155' },
        },
        y: {
          grid: { color: 'rgba(51,65,85,0.3)' },
          ticks: { color: '#94A3B8', font: { size: 11 }, callback: v => `${Number(v) >= 1000000 ? (v / 1000000).toFixed(1) + 'M' : v}` },
          border: { color: '#334155' },
        },
      },
    },
  })
}

async function loadDashboard() {
  loading.value = true
  error.value = null
  try {
    const [dashRes, ordersRes] = await Promise.all([
      adminApi.getDashboard({ period: chartPeriod.value }),
      adminApi.getOrders({ page_size: 10, ordering: '-id' }),
    ])
    dashboardData.value = dashRes.data
    buildKPIs(dashRes.data)
    buildStatusData(dashRes.data)
    latestOrders.value = ordersRes.data.results || ordersRes.data
    topProducts.value = dashRes.data.top_products || []
    loading.value = false
    loadingOrders.value = false

    await nextTick()
    buildSalesChart(dashRes.data)
  } catch (e) {
    loading.value = false
    loadingOrders.value = false
    error.value = e.response?.data?.detail || e.message || 'API bilan bog\'lanishda xatolik'
  }
}

watch(chartPeriod, async () => {
  loading.value = true
  error.value = null
  try {
    const res = await adminApi.getDashboard({ period: chartPeriod.value })
    dashboardData.value = res.data
    buildKPIs(res.data)
    buildStatusData(res.data)
    afterUpdate()
  } catch (e) {
    error.value = e.response?.data?.detail || e.message || 'API bilan bog\'lanishda xatolik'
  } finally {
    loading.value = false
  }
})

async function afterUpdate() {
  await nextTick()
  buildSalesChart(dashboardData.value)
}

onMounted(loadDashboard)
</script>