<template>
  <div class="space-y-6">
    <h1 class="text-2xl font-bold text-white">Mijozlar Ro'yxati</h1>

    <div class="bg-slate-800 rounded-2xl p-4 border border-slate-700 flex gap-3">
      <div class="flex-1 relative">
        <input v-model="search" @input="debounceFetch" type="text" placeholder="Ism yoki telefon..."
               class="bg-slate-700 text-slate-200 border border-slate-600 rounded-xl px-4 py-2.5 pl-10 w-full text-sm focus:outline-none focus:ring-2 focus:ring-brand-500" />
        <Search class="absolute left-3 top-1/2 -translate-y-1/2 w-4 h-4 text-slate-400" />
      </div>
    </div>

    <div class="bg-slate-800 rounded-2xl border border-slate-700 overflow-hidden">
      <div v-if="loading" class="p-6 space-y-3">
        <div v-for="i in 6" :key="i" class="skeleton h-16 rounded-xl bg-slate-700" />
      </div>
      <div v-else-if="!customers.length" class="py-16 text-center">
        <Users class="w-12 h-12 text-slate-600 mx-auto mb-3" />
        <p class="text-slate-400">Mijozlar topilmadi</p>
      </div>
      <div v-else class="overflow-x-auto">
        <table class="w-full text-sm">
          <thead class="bg-slate-900/50">
            <tr>
              <th v-for="col in columns" :key="col" class="text-left px-4 py-3 text-slate-400 font-medium text-xs uppercase tracking-wider">{{ col }}</th>
            </tr>
          </thead>
          <tbody class="divide-y divide-slate-700">
            <tr v-for="c in customers" :key="c.id" class="hover:bg-slate-700/50 transition-colors">
              <td class="px-4 py-4">
                <div class="flex items-center gap-3">
                  <div class="w-9 h-9 bg-brand-900 rounded-xl flex items-center justify-center text-brand-400 font-bold text-sm flex-shrink-0">
                    {{ c.full_name?.charAt(0)?.toUpperCase() || '?' }}
                  </div>
                  <span class="font-medium text-white">{{ c.full_name }}</span>
                </div>
              </td>
              <td class="px-4 py-4 text-slate-300">{{ c.phone_number }}</td>
              <td class="px-4 py-4 text-slate-300">{{ c.orders_count || 0 }}</td>
              <td class="px-4 py-4 font-semibold text-brand-400">{{ formatPrice(c.total_spent) }}</td>
              <td class="px-4 py-4 text-slate-400 text-xs">{{ formatDate(c.date_joined) }}</td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { Search, Users } from '@lucide/vue'
import { adminApi } from '@/api/admin'

const customers = ref([])
const loading = ref(true)
const search = ref('')
const columns = ['Mijoz', 'Telefon', 'Buyurtmalar', 'Jami xarid', 'Qo\'shilgan sana']

function formatPrice(p) { return p ? new Intl.NumberFormat('uz-UZ', { style: 'currency', currency: 'UZS', maximumFractionDigits: 0 }).format(p) : '—' }
function formatDate(d) { return d ? new Date(d).toLocaleDateString('uz-UZ', { day: '2-digit', month: 'short', year: 'numeric' }) : '—' }

async function fetchCustomers() {
  loading.value = true
  try {
    const params = {}
    if (search.value) params.search = search.value
    const res = await adminApi.getCustomers(params)
    customers.value = res.data.results || res.data
  } catch {}
  loading.value = false
}

let debounceTimer
function debounceFetch() { clearTimeout(debounceTimer); debounceTimer = setTimeout(fetchCustomers, 400) }

onMounted(fetchCustomers)
</script>
