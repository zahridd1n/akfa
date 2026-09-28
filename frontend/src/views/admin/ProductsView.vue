<template>
  <div class="space-y-5 max-w-full overflow-hidden">
    <div class="flex items-center justify-between flex-wrap gap-3">
      <div>
        <h1 class="text-xl sm:text-2xl font-bold text-white">Mahsulotlar</h1>
        <p class="text-slate-400 text-xs sm:text-sm mt-0.5">{{ totalCount }} ta mahsulot</p>
      </div>
      <router-link to="/admin/products/new" class="btn-sm sm:btn-md btn-primary shadow-sm" id="add-product-btn">
        <Plus class="w-4 h-4" /> <span>Yangi mahsulot</span>
      </router-link>
    </div>

    <!-- Toolbar -->
    <div class="bg-slate-800/90 rounded-2xl p-3 sm:p-4 border border-slate-700/80 flex flex-col sm:flex-row gap-3">
      <div class="flex-1 w-full relative">
        <input
          v-model="search"
          @input="debounceFetch"
          type="text"
          placeholder="Mahsulot nomi yoki kodi..."
          class="bg-slate-700/80 text-slate-200 placeholder-slate-400 border border-slate-600 rounded-xl px-4 py-2.5 pl-10 w-full text-xs sm:text-sm focus:outline-none focus:ring-2 focus:ring-brand-500"
        />
        <Search class="absolute left-3 top-1/2 -translate-y-1/2 w-4 h-4 text-slate-400" />
      </div>
      <select
        v-model="filterCategory"
        @change="fetchProducts()"
        class="bg-slate-700/80 text-slate-300 border border-slate-600 rounded-xl px-4 py-2.5 text-xs sm:text-sm focus:outline-none focus:ring-2 focus:ring-brand-500 cursor-pointer w-full sm:w-auto min-w-[180px]"
      >
        <option value="">Barcha kategoriyalar</option>
        <option v-for="cat in categories" :key="cat.slug" :value="cat.slug">{{ cat.name }}</option>
      </select>
    </div>

    <!-- Products Table -->
    <div class="bg-slate-800/90 rounded-2xl border border-slate-700/80 overflow-hidden shadow-sm">
      <div v-if="loading" class="p-4 sm:p-6 space-y-3">
        <div v-for="i in 5" :key="i" class="skeleton h-16 rounded-xl bg-slate-700" />
      </div>

      <div v-else-if="!products.length" class="py-16 text-center px-4">
        <Package class="w-12 h-12 text-slate-600 mx-auto mb-3" />
        <p class="text-slate-400 text-sm mb-4">Mahsulotlar topilmadi</p>
        <router-link to="/admin/products/new" class="btn-md btn-primary">Mahsulot qo'shish</router-link>
      </div>

      <div v-else class="overflow-x-auto w-full">
        <table class="w-full text-sm text-left min-w-[620px]">
          <thead class="bg-slate-900/60 border-b border-slate-700/80">
            <tr>
              <th class="px-4 py-3 text-slate-400 font-medium text-xs uppercase tracking-wider whitespace-nowrap">Mahsulot</th>
              <th class="px-4 py-3 text-slate-400 font-medium text-xs uppercase tracking-wider whitespace-nowrap">Kategoriya</th>
              <th class="px-4 py-3 text-slate-400 font-medium text-xs uppercase tracking-wider whitespace-nowrap">Baza Narx (m²)</th>
              <th class="px-4 py-3 text-slate-400 font-medium text-xs uppercase tracking-wider whitespace-nowrap">Ranglar</th>
              <th class="px-4 py-3 text-slate-400 font-medium text-xs uppercase tracking-wider whitespace-nowrap">Holat</th>
              <th class="px-4 py-3 text-right whitespace-nowrap" />
            </tr>
          </thead>
          <tbody class="divide-y divide-slate-700/60">
            <tr v-for="product in products" :key="product.id" class="hover:bg-slate-700/40 transition-colors">
              <td class="px-4 py-3.5">
                <div class="flex items-center gap-3 min-w-[170px]">
                  <img
                    :src="mainImage(product)"
                    :alt="product.name"
                    class="w-11 h-11 rounded-xl object-cover bg-slate-700 flex-shrink-0"
                  />
                  <div class="min-w-0">
                    <p class="font-semibold text-white truncate max-w-[160px]">{{ product.name }}</p>
                    <p class="text-xs text-slate-400 capitalize truncate max-w-[160px]">{{ product.material || 'Material' }}</p>
                  </div>
                </div>
              </td>
              <td class="px-4 py-3.5 text-slate-300 whitespace-nowrap">{{ product.category_name }}</td>
              <td class="px-4 py-3.5 font-semibold text-brand-400 whitespace-nowrap">{{ formatPrice(product.base_price) }}</td>
              <td class="px-4 py-3.5 whitespace-nowrap">
                <div class="flex items-center gap-1.5">
                  <div
                    v-for="color in (product.colors || []).slice(0, 5)"
                    :key="color.id"
                    class="w-5 h-5 rounded-full border border-slate-600/90 shadow-xs flex-shrink-0"
                    :style="{ backgroundColor: color.hex_code }"
                    :title="color.name"
                  />
                  <span v-if="(product.colors || []).length > 5" class="text-xs text-slate-400 font-medium">+{{ product.colors.length - 5 }}</span>
                </div>
              </td>
              <td class="px-4 py-3.5 whitespace-nowrap">
                <span
                  class="badge text-[10px] font-semibold"
                  :class="product.is_active ? 'badge-green' : 'badge-red'"
                >
                  {{ product.is_active ? 'Faol' : 'Nofaol' }}
                </span>
              </td>
              <td class="px-4 py-3.5 text-right whitespace-nowrap">
                <div class="flex items-center justify-end gap-1.5">
                  <router-link
                    :to="`/admin/products/${product.id}`"
                    class="p-1.5 sm:px-3 sm:py-1.5 rounded-lg bg-slate-700/80 hover:bg-brand-600 text-slate-200 hover:text-white transition-colors text-xs inline-flex items-center gap-1.5"
                    :id="`edit-product-${product.id}`"
                  >
                    <Pencil class="w-3.5 h-3.5" />
                    <span class="hidden sm:inline">Tahrirlash</span>
                  </router-link>
                  <button
                    @click="deleteProduct(product)"
                    class="p-1.5 rounded-lg text-slate-400 hover:text-red-400 hover:bg-red-950/40 transition-colors"
                    :id="`delete-product-${product.id}`"
                    title="O'chirish"
                  >
                    <Trash2 class="w-4 h-4" />
                  </button>
                </div>
              </td>
            </tr>
          </tbody>
        </table>
      </div>

      <!-- Pagination -->
      <div v-if="totalPages > 1" class="flex justify-center items-center gap-2 p-3.5 sm:p-4 border-t border-slate-700/80 bg-slate-900/40">
        <button @click="setPage(page - 1)" :disabled="page <= 1" class="px-3 py-1.5 rounded-lg bg-slate-700 text-slate-300 hover:bg-slate-600 disabled:opacity-40 text-xs sm:text-sm">‹ Oldingi</button>
        <span class="text-slate-400 text-xs sm:text-sm px-2">{{ page }} / {{ totalPages }}</span>
        <button @click="setPage(page + 1)" :disabled="page >= totalPages" class="px-3 py-1.5 rounded-lg bg-slate-700 text-slate-300 hover:bg-slate-600 disabled:opacity-40 text-xs sm:text-sm">Keyingi ›</button>
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
