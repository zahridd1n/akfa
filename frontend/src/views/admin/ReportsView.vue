<template>
  <div class="space-y-5 max-w-full overflow-hidden">
    <div class="flex flex-col sm:flex-row sm:items-center justify-between gap-3">
      <div>
        <h1 class="text-xl sm:text-2xl font-bold text-white">Hisobotlar & Export</h1>
        <p class="text-slate-400 text-xs sm:text-sm mt-0.5">Sotuvlar va daromadlar bo'yicha tahlil hamda hujjatlarni yuklab olish</p>
      </div>
      <!-- Quick export options directly in header -->
      <div class="flex items-center gap-2">
        <button
          @click="exportReport('excel')"
          :disabled="exporting"
          class="btn-sm btn-primary inline-flex items-center gap-1.5 shadow-sm"
          id="quick-export-excel-btn"
        >
          <span>📊 Excel yuklab olish</span>
        </button>
        <button
          @click="exportReport('word')"
          :disabled="exporting"
          class="btn-sm bg-slate-700 hover:bg-slate-600 text-white border border-slate-600 inline-flex items-center gap-1.5"
          id="quick-export-word-btn"
        >
          <span>📄 Word</span>
        </button>
      </div>
    </div>

    <!-- Date Range & Filters -->
    <div class="bg-slate-800/90 rounded-2xl p-4 sm:p-6 border border-slate-700/80 shadow-sm">
      <h2 class="font-semibold text-white text-sm sm:text-base mb-3 sm:mb-4">Sana oralig'ini tanlang</h2>
      <div class="grid grid-cols-1 sm:grid-cols-4 gap-3 sm:gap-4">
        <div>
          <label class="form-label text-slate-300 text-xs">Boshlanish sanasi</label>
          <input
            v-model="dateFrom"
            type="date"
            class="form-input bg-slate-700/80 border-slate-600 text-white focus:border-brand-500 text-xs sm:text-sm"
            id="report-date-from"
          />
        </div>
        <div>
          <label class="form-label text-slate-300 text-xs">Tugash sanasi</label>
          <input
            v-model="dateTo"
            type="date"
            class="form-input bg-slate-700/80 border-slate-600 text-white focus:border-brand-500 text-xs sm:text-sm"
            id="report-date-to"
          />
        </div>
        <div class="flex items-end">
          <button
            @click="fetchReport"
            :disabled="loading"
            class="btn-md sm:btn-lg btn-primary w-full justify-center"
            id="generate-report-btn"
          >
            <span v-if="!loading">Hisobotni ko'rish</span>
            <div v-else class="spinner" />
          </button>
        </div>
        <div class="flex items-end">
          <button
            @click="resetToMonth"
            class="btn-md sm:btn-lg btn-outline border-slate-600 text-slate-300 hover:bg-slate-700 w-full justify-center text-xs sm:text-sm"
          >
            Joriy oy
          </button>
        </div>
      </div>
    </div>

    <!-- Loading skeleton -->
    <div v-if="loading && !report" class="grid grid-cols-1 sm:grid-cols-3 gap-3 sm:gap-4">
      <div v-for="i in 3" :key="i" class="skeleton h-24 rounded-2xl bg-slate-800" />
    </div>

    <!-- Results -->
    <div v-if="report" class="space-y-5">
      <!-- Summary KPIs -->
      <div class="grid grid-cols-1 sm:grid-cols-3 gap-3 sm:gap-4">
        <div class="bg-slate-800/90 rounded-2xl p-4 sm:p-5 border border-slate-700/80 shadow-sm">
          <p class="text-slate-400 text-xs sm:text-sm mb-1.5">Jami buyurtmalar</p>
          <p class="text-2xl sm:text-3xl font-bold text-white">{{ report.total_orders || 0 }} ta</p>
        </div>
        <div class="bg-slate-800/90 rounded-2xl p-4 sm:p-5 border border-slate-700/80 shadow-sm">
          <p class="text-slate-400 text-xs sm:text-sm mb-1.5">Jami tushum</p>
          <p class="text-2xl sm:text-3xl font-bold text-emerald-400 truncate">{{ formatPrice(report.total_revenue) }}</p>
        </div>
        <div class="bg-slate-800/90 rounded-2xl p-4 sm:p-5 border border-slate-700/80 shadow-sm">
          <p class="text-slate-400 text-xs sm:text-sm mb-1.5">O'rtacha buyurtma qiymati</p>
          <p class="text-2xl sm:text-3xl font-bold text-brand-400 truncate">{{ formatPrice(report.avg_order_value) }}</p>
        </div>
      </div>

      <!-- Export Card -->
      <div class="bg-slate-800/90 rounded-2xl p-4 sm:p-6 border border-slate-700/80 shadow-sm">
        <div class="flex flex-col sm:flex-row sm:items-center justify-between gap-4">
          <div>
            <h2 class="font-semibold text-white text-sm sm:text-base">Hisobot hujjatini yuklab olish</h2>
            <p class="text-slate-400 text-xs mt-0.5">Tanlangan sana oralig'idagi barcha buyurtmalar va tushumlar jadvali</p>
          </div>
          <div class="grid grid-cols-1 sm:flex gap-3">
            <button
              @click="exportReport('excel')"
              :disabled="exporting"
              class="btn-md btn-primary justify-center px-5 shadow-sm"
              id="export-excel-btn"
            >
              <span v-if="!exporting" class="inline-flex items-center gap-2">
                <span>📊</span> Excel (.xlsx) yuklab olish
              </span>
              <div v-else class="spinner" />
            </button>
            <button
              @click="exportReport('word')"
              :disabled="exporting"
              class="btn-md bg-slate-700 hover:bg-slate-600 text-white border border-slate-600 justify-center px-5"
              id="export-word-btn"
            >
              <span v-if="!exporting" class="inline-flex items-center gap-2">
                <span>📄</span> Word (.doc) yuklab olish
              </span>
              <div v-else class="spinner" />
            </button>
          </div>
        </div>
      </div>

      <!-- Status Breakdown & Top Products -->
      <div class="grid grid-cols-1 lg:grid-cols-2 gap-4 sm:gap-6">
        <!-- Order status breakdown -->
        <div class="bg-slate-800/90 rounded-2xl p-4 sm:p-6 border border-slate-700/80 shadow-sm">
          <h3 class="font-bold text-white text-sm sm:text-base mb-4">Holatlar bo'yicha taqsimot</h3>
          <div class="space-y-3">
            <div
              v-for="(st, key) in (report.orders_by_status || {})"
              :key="key"
              class="flex items-center justify-between p-2.5 rounded-xl bg-slate-900/40 border border-slate-700/40"
            >
              <span class="text-slate-300 text-xs sm:text-sm">{{ st.label || key }}</span>
              <span class="font-bold text-white text-xs sm:text-sm">{{ st.count }} ta</span>
            </div>
          </div>
        </div>

        <!-- Top Products -->
        <div class="bg-slate-800/90 rounded-2xl p-4 sm:p-6 border border-slate-700/80 shadow-sm">
          <h3 class="font-bold text-white text-sm sm:text-base mb-4">Eng ko'p sotilgan mahsulotlar</h3>
          <div v-if="!report.top_products || !report.top_products.length" class="text-center py-8 text-slate-500 text-sm">
            Ma'lumotlar mavjud emas
          </div>
          <div v-else class="space-y-2.5">
            <div
              v-for="(tp, idx) in report.top_products"
              :key="idx"
              class="flex items-center justify-between p-2.5 rounded-xl bg-slate-900/40 border border-slate-700/40"
            >
              <div class="min-w-0 flex-1 pr-3">
                <p class="text-xs sm:text-sm font-semibold text-white truncate">{{ tp.product__name }}</p>
                <p class="text-[11px] text-slate-400">{{ tp.total_qty }} dona sotilgan</p>
              </div>
              <span class="font-bold text-emerald-400 text-xs sm:text-sm whitespace-nowrap">{{ formatPrice(tp.total_revenue) }}</span>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { adminApi } from '@/api/admin'
import { useAlertStore } from '@/stores/alert'

const alertStore = useAlertStore()
const dateFrom = ref('')
const dateTo = ref('')
const loading = ref(false)
const exporting = ref(false)
const report = ref(null)

function formatPrice(p) {
  if (!p && p !== 0) return '—'
  return new Intl.NumberFormat('uz-UZ', { style: 'currency', currency: 'UZS', maximumFractionDigits: 0 }).format(p)
}

function initDates() {
  const now = new Date()
  const firstDay = new Date(now.getFullYear(), now.getMonth(), 1)
  const yyyy = now.getFullYear()
  const mm = String(now.getMonth() + 1).padStart(2, '0')
  const dd = String(now.getDate()).padStart(2, '0')

  const fMm = String(firstDay.getMonth() + 1).padStart(2, '0')
  const fDd = String(firstDay.getDate()).padStart(2, '0')

  dateFrom.value = `${firstDay.getFullYear()}-${fMm}-${fDd}`
  dateTo.value = `${yyyy}-${mm}-${dd}`
}

function resetToMonth() {
  initDates()
  fetchReport()
}

async function fetchReport() {
  loading.value = true
  try {
    const params = {}
    if (dateFrom.value) params.date_from = dateFrom.value
    if (dateTo.value) params.date_to = dateTo.value

    const res = await adminApi.getReports(params)
    report.value = res.data
  } catch (err) {
    alertStore.error(err.response?.data?.detail || 'Hisobot olishda xatolik')
  } finally {
    loading.value = false
  }
}

async function exportReport(format) {
  exporting.value = true
  try {
    const params = {
      format,
      export_format: format,
    }
    if (dateFrom.value) params.date_from = dateFrom.value
    if (dateTo.value) params.date_to = dateTo.value

    const res = await adminApi.exportReports(params)

    // Check if the response is JSON error returned as blob
    if (res.data instanceof Blob && res.data.type === 'application/json') {
      const text = await res.data.text()
      const json = JSON.parse(text)
      throw new Error(json.detail || 'Eksportda xatolik yuz berdi')
    }

    const ext = format === 'excel' ? 'xlsx' : 'doc'
    const mime = format === 'excel'
      ? 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
      : 'application/msword'

    const blob = new Blob([res.data], { type: mime })
    const url = URL.createObjectURL(blob)
    const a = document.createElement('a')
    a.href = url
    const dFrom = dateFrom.value || 'barchasi'
    const dTo = dateTo.value || 'barchasi'
    a.download = `saramax_hisobot_${dFrom}_${dTo}.${ext}`
    document.body.appendChild(a)
    a.click()
    document.body.removeChild(a)
    URL.revokeObjectURL(url)

    alertStore.success(`Hisobot (${ext.toUpperCase()}) yuklab olindi`)
  } catch (err) {
    alertStore.error(err.message || 'Export xatolik yuz berdi')
  } finally {
    exporting.value = false
  }
}

onMounted(() => {
  initDates()
  fetchReport()
})
</script>
