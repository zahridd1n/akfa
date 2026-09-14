<template>
  <div class="space-y-6">
    <div class="flex items-center justify-between flex-wrap gap-4">
      <div>
        <h1 class="text-2xl font-bold text-white">Mahsulotlar</h1>
        <p class="text-slate-400 text-sm mt-1">{{ totalCount }} ta mahsulot</p>
      </div>
      <router-link to="/admin/products/new" class="btn-md btn-primary" id="add-product-btn">
        <Plus class="w-4 h-4" /> Yangi mahsulot
      </router-link>
    </div>

    <!-- Toolbar -->
    <div class="bg-slate-800 rounded-2xl p-4 border border-slate-700 flex flex-wrap gap-3">
      <div class="flex-1 min-w-[200px] relative">
        <input v-model="search" @input="debounceFetch" type="text" placeholder="Qidirish..."
               class="bg-slate-700 text-slate-200 border border-slate-600 rounded-xl px-4 py-2.5 pl-10 w-full text-sm focus:outline-none focus:ring-2 focus:ring-brand-500" />
        <Search class="absolute left-3 top-1/2 -translate-y-1/2 w-4 h-4 text-slate-400" />
      </div>
      <select v-model="filterCategory" @change="fetchProducts()" class="bg-slate-700 text-slate-300 border border-slate-600 rounded-xl px-4 py-2.5 text-sm">
        <option value="">Barcha kategoriyalar</option>
        <option v-for="cat in categories" :key="cat.slug" :value="cat.slug">{{ cat.name }}</option>
      </select>
    </div>

    <!-- Products Table -->
    <div class="bg-slate-800 rounded-2xl border border-slate-700 overflow-hidden">
      <div v-if="loading" class="p-6 space-y-3">
        <div v-for="i in 6" :key="i" class="skeleton h-20 rounded-xl bg-slate-700" />
      </div>

      <div v-else-if="!products.length" class="py-16 text-center">
        <Package class="w-12 h-12 text-slate-600 mx-auto mb-3" />
        <p class="text-slate-400 mb-4">Mahsulotlar topilmadi</p>
        <router-link to="/admin/products/new" class="btn-md btn-primary">Mahsulot qo'shish</router-link>
      </div>

      <div v-else class="overflow-x-auto">
        <table class="w-full text-sm">
          <thead class="bg-slate-900/50">
            <tr>
              <th class="text-left px-4 py-3 text-slate-400 font-medium text-xs uppercase tracking-wider">Mahsulot</th>
              <th class="text-left px-4 py-3 text-slate-400 font-medium text-xs uppercase tracking-wider">Kategoriya</th>
              <th class="text-left px-4 py-3 text-slate-400 font-medium text-xs uppercase tracking-wider">Baza Narx (m²)</th>
              <th class="text-left px-4 py-3 text-slate-400 font-medium text-xs uppercase tracking-wider">Ranglar</th>
              <th class="text-left px-4 py-3 text-slate-400 font-medium text-xs uppercase tracking-wider">Holat</th>
              <th class="px-4 py-3" />
            </tr>
          </thead>
          <tbody class="divide-y divide-slate-700">
            <tr v-for="product in products" :key="product.id" class="hover:bg-slate-700/50 transition-colors">
              <td class="px-4 py-4">
                <div class="flex items-center gap-3">
                  <img
                    :src="mainImage(product)"
                    :alt="product.name"
                    class="w-12 h-12 rounded-xl object-cover bg-slate-700"
                  />
                  <div>
                    <p class="font-semibold text-white">{{ product.name }}</p>
                    <p class="text-xs text-slate-500">{{ product.material }}</p>
                  </div>
                </div>
              </td>
              <td class="px-4 py-4 text-slate-300">{{ product.category_name }}</td>
              <td class="px-4 py-4 font-semibold text-brand-400">{{ formatPrice(product.base_price) }}</td>
              <td class="px-4 py-4">
                <div class="flex gap-1.5">
                  <div
                    v-for="color in (product.colors || []).slice(0, 5)"
                    :key="color.id"
                    class="w-5 h-5 rounded-full border border-slate-600"
                    :style="{ backgroundColor: color.hex_code }"
                    :title="color.name"
                  />
                  <span v-if="(product.colors || []).length > 5" class="text-xs text-slate-500 self-center">+{{ product.colors.length - 5 }}</span>
                </div>
              </td>
              <td class="px-4 py-4">
                <span class="badge" :class="product.is_active ? 'badge-green' : 'badge-red'">
                  {{ product.is_active ? 'Aktiv' : 'Nofaol' }}
                </span>
              </td>
              <td class="px-4 py-4">
                <div class="flex items-center gap-2">
                  <router-link :to="`/admin/products/${product.id}`" class="btn-sm btn-secondary text-xs" :id="`edit-product-${product.id}`">
                    <Pencil class="w-3.5 h-3.5" /> Tahrirlash
                  </router-link>
                  <button @click="deleteProduct(product)" class="btn-sm btn-ghost text-red-400 hover:bg-red-900/20 text-xs" :id="`delete-product-${product.id}`">
                    <Trash2 class="w-3.5 h-3.5" />
                  </button>
                </div>
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
import { Search, Package, Plus, Pencil, Trash2 } from '@lucide/vue'
import { adminApi } from '@/api/admin'
import { productsApi } from '@/api/products'
import { useAlertStore } from '@/stores/alert'

const alertStore = useAlertStore()
const products = ref([])
const categories = ref([])
const loading = ref(true)
const search = ref('')
const filterCategory = ref('')
const page = ref(1)
const pageSize = 20
const totalCount = ref(0)
const totalPages = computed(() => Math.ceil(totalCount.value / pageSize))

function mainImage(product) {
  const img = product.images?.find(i => i.is_main) || product.images?.[0]
  return img?.image || 'https://via.placeholder.com/48/334155/94A3B8?text=R'
}
function formatPrice(p) { return p ? new Intl.NumberFormat('uz-UZ', { style: 'currency', currency: 'UZS', maximumFractionDigits: 0 }).format(p) : '—' }

async function fetchProducts() {
  loading.value = true
  try {
    const params = { page: page.value, page_size: pageSize }
    if (search.value) params.search = search.value
    if (filterCategory.value) params.category = filterCategory.value
    const res = await adminApi.getProducts(params)
    products.value = res.data.results || res.data
    totalCount.value = res.data.count || products.value.length
  } catch {}
  loading.value = false
}

async function deleteProduct(product) {
  if (!confirm(`"${product.name}"ni o'chirishni tasdiqlaysizmi?`)) return
  try {
    await adminApi.deleteProduct(product.id)
    products.value = products.value.filter(p => p.id !== product.id)
    alertStore.success('Mahsulot o\'chirildi')
  } catch { alertStore.error('Xatolik yuz berdi') }
}

function setPage(p) { page.value = p; fetchProducts() }

let debounceTimer
function debounceFetch() { clearTimeout(debounceTimer); debounceTimer = setTimeout(fetchProducts, 400) }

onMounted(async () => {
  const catsRes = await productsApi.getCategories()
  categories.value = catsRes.data.results || catsRes.data
  await fetchProducts()
})
</script>
