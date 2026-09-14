<template>
  <div class="space-y-6">
    <h1 class="text-2xl font-bold text-white">Hisobotlar & Export</h1>

    <!-- Date Range -->
    <div class="bg-slate-800 rounded-2xl p-6 border border-slate-700">
      <h2 class="font-semibold text-white mb-4">Sana oralig'ini tanlang</h2>
      <div class="grid grid-cols-1 sm:grid-cols-3 gap-4">
        <div>
          <label class="form-label text-slate-300">Boshlanish sanasi</label>
          <input v-model="dateFrom" type="date" class="form-input bg-slate-700 border-slate-600 text-white focus:border-brand-500" id="report-date-from" />
        </div>
        <div>
          <label class="form-label text-slate-300">Tugash sanasi</label>
          <input v-model="dateTo" type="date" class="form-input bg-slate-700 border-slate-600 text-white focus:border-brand-500" id="report-date-to" />
        </div>
        <div class="flex items-end">
          <button @click="fetchReport" :disabled="loading" class="btn-lg btn-primary w-full" id="generate-report-btn">
            <span v-if="!loading">Hisobot yaratish</span>
            <div v-else class="spinner" />
          </button>
        </div>
      </div>
    </div>

    <!-- Results -->
    <div v-if="report" class="space-y-6">
      <!-- Summary KPIs -->
      <div class="grid grid-cols-1 sm:grid-cols-3 gap-4">
        <div class="bg-slate-800 rounded-2xl p-5 border border-slate-700">
          <p class="text-slate-400 text-sm mb-2">Jami buyurtmalar</p>
          <p class="text-3xl font-bold text-white">{{ report.total_orders || 0 }}</p>
        </div>
        <div class="bg-slate-800 rounded-2xl p-5 border border-slate-700">
          <p class="text-slate-400 text-sm mb-2">Jami tushum</p>
          <p class="text-3xl font-bold text-emerald-400">{{ formatPrice(report.total_revenue) }}</p>
        </div>
        <div class="bg-slate-800 rounded-2xl p-5 border border-slate-700">
          <p class="text-slate-400 text-sm mb-2">O'rtacha buyurtma</p>
          <p class="text-3xl font-bold text-brand-400">{{ formatPrice(report.avg_order_value) }}</p>
        </div>
      </div>

      <!-- Export Buttons -->
      <div class="bg-slate-800 rounded-2xl p-6 border border-slate-700">
        <h2 class="font-semibold text-white mb-4">Yuklab olish</h2>
        <div class="flex flex-wrap gap-3">
          <button @click="exportReport('excel')" :disabled="exporting" class="btn-md btn-primary" id="export-excel-btn">
            <span v-if="!exporting">📊 Excel (.xlsx)</span>
            <div v-else class="spinner" />
          </button>
          <button @click="exportReport('word')" :disabled="exporting" class="btn-md btn-secondary" id="export-word-btn">
            📄 Word (.docx)
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { adminApi } from '@/api/admin'
import { useAlertStore } from '@/stores/alert'

const alertStore = useAlertStore()
const dateFrom = ref('')
const dateTo = ref('')
const loading = ref(false)
const exporting = ref(false)
const report = ref(null)

function formatPrice(p) { return p ? new Intl.NumberFormat('uz-UZ', { style: 'currency', currency: 'UZS', maximumFractionDigits: 0 }).format(p) : '—' }

async function fetchReport() {
  if (!dateFrom.value || !dateTo.value) { alertStore.warning('Sanalarni to\'liq kiriting'); return }
  loading.value = true
  try {
    const res = await adminApi.getReports({ date_from: dateFrom.value, date_to: dateTo.value })
    report.value = res.data
  } catch { alertStore.error('Hisobot olishda xatolik') }
  loading.value = false
}

async function exportReport(format) {
  exporting.value = true
  try {
    const res = await adminApi.exportReports({ date_from: dateFrom.value, date_to: dateTo.value, format })
    const url = URL.createObjectURL(new Blob([res.data]))
    const a = document.createElement('a')
    a.href = url
    a.download = `saramax_hisobot_${dateFrom.value}_${dateTo.value}.${format === 'excel' ? 'xlsx' : 'docx'}`
    a.click()
    URL.revokeObjectURL(url)
    alertStore.success('Fayl yuklab olindi')
  } catch { alertStore.error('Export xatolik') }
  exporting.value = false
}
</script>
