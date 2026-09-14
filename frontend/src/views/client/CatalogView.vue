<template>
  <div class="min-h-screen" style="background: #EBF3F8;">

    <!-- Page Header -->
    <div class="bg-white/80 backdrop-blur border-b border-[#C7DDEA]/60 px-4 pt-4 pb-3">
      <h1 class="text-2xl font-bold text-slate-900">Katalog</h1>

      <!-- Mobile Filter Chips Row -->
      <div class="flex items-center gap-2 mt-3 overflow-x-auto scrollbar-hide -mx-4 px-4 pb-1">
        <!-- Filter Toggle -->
        <button
          @click="showMobileFilters = true"
          class="flex-shrink-0 flex items-center gap-1.5 px-3 py-1.5 rounded-full border text-sm font-medium transition-colors"
          :class="hasActiveFilters ? 'border-brand-500 bg-brand-50 text-brand-700' : 'border-slate-200 bg-white text-slate-600'"
        >
          <Filter class="w-3.5 h-3.5" />
          Filtr
          <span v-if="hasActiveFilters" class="w-4 h-4 bg-brand-500 text-white text-[10px] font-bold rounded-full flex items-center justify-center">!</span>
        </button>

        <!-- Sort -->
        <button
          @click="showSortMenu = !showSortMenu"
          class="flex-shrink-0 flex items-center gap-1.5 px-3 py-1.5 rounded-full border border-slate-200 bg-white text-slate-600 text-sm font-medium"
        >
          <ArrowUpDown class="w-3.5 h-3.5" />
          Saralash
        </button>

        <!-- Category Quick Chips -->
        <button
          class="flex-shrink-0 px-3 py-1.5 rounded-full text-sm font-medium transition-colors"
          :class="!filters.category ? 'bg-brand-950 text-white' : 'border border-slate-200 bg-white text-slate-600'"
          @click="setCategory('')"
        >Barchasi</button>
        <button
          v-for="cat in categories.slice(0, 5)"
          :key="cat.slug"
          @click="setCategory(cat.slug)"
          class="flex-shrink-0 px-3 py-1.5 rounded-full text-sm font-medium transition-colors whitespace-nowrap"
          :class="filters.category === cat.slug ? 'bg-brand-950 text-white' : 'border border-slate-200 bg-white text-slate-600'"
        >{{ cat.name }}</button>
      </div>

      <!-- Sort Dropdown -->
      <Transition name="fade">
        <div v-if="showSortMenu" class="mt-2 bg-white border border-slate-200 rounded-xl shadow-lg p-1">
          <button
            v-for="opt in sortOptions"
            :key="opt.value"
            @click="filters.ordering = opt.value; fetchProducts(true); showSortMenu = false"
            class="block w-full text-left px-4 py-2.5 rounded-lg text-sm font-medium transition-colors"
            :class="filters.ordering === opt.value ? 'bg-brand-50 text-brand-700' : 'text-slate-700 hover:bg-slate-50'"
          >{{ opt.label }}</button>
        </div>
      </Transition>
    </div>

    <!-- Active Filters -->
    <div v-if="hasActiveFilters" class="flex items-center gap-2 px-4 py-2 bg-white border-b border-slate-100 overflow-x-auto scrollbar-hide">
      <span v-if="filters.search" class="flex items-center gap-1 px-2.5 py-1 bg-slate-100 rounded-full text-xs text-slate-700">
        "{{ filters.search }}"
        <button @click="filters.search = ''; fetchProducts(true)"><X class="w-3 h-3" /></button>
      </span>
      <span v-if="filters.category" class="flex items-center gap-1 px-2.5 py-1 bg-brand-50 text-brand-700 rounded-full text-xs">
        {{ categories.find(c => c.slug === filters.category)?.name }}
        <button @click="setCategory('')"><X class="w-3 h-3" /></button>
      </span>
      <span v-if="filters.material" class="flex items-center gap-1 px-2.5 py-1 bg-slate-100 rounded-full text-xs text-slate-700">
        {{ filters.material }}
        <button @click="toggleFilter('material', '')"><X class="w-3 h-3" /></button>
      </span>
      <button @click="resetFilters" class="flex-shrink-0 text-xs text-red-500 underline ml-auto">Tozalash</button>
    </div>

    <!-- Content -->
    <div class="p-4">

      <!-- Desktop Sidebar + Grid layout -->
      <div class="hidden lg:flex gap-8">
        <!-- Desktop Sidebar -->
        <aside class="w-64 flex-shrink-0">
          <div class="bg-white rounded-xl shadow-sm border border-slate-100 p-6 sticky top-24">
            <div class="flex items-center justify-between mb-5">
              <h2 class="font-bold text-slate-900 text-base">Filtrlar</h2>
              <button v-if="hasActiveFilters" @click="resetFilters" class="text-xs text-brand-600 font-medium">Tozalash</button>
            </div>
            <!-- Categories -->
            <div class="mb-5">
              <p class="text-[10px] font-bold text-slate-500 uppercase tracking-wider mb-3">Mahsulot turi</p>
              <div class="space-y-1.5">
                <label v-for="cat in categories" :key="cat.slug" class="flex items-center gap-3 cursor-pointer group py-0.5">
                  <div class="w-4 h-4 rounded border flex items-center justify-center transition-colors flex-shrink-0"
                       :class="filters.category === cat.slug ? 'bg-brand-600 border-brand-600' : 'border-slate-300 bg-white'">
                    <Check v-if="filters.category === cat.slug" class="w-2.5 h-2.5 text-white" />
                  </div>
                  <span class="text-sm text-slate-600 group-hover:text-slate-900">{{ cat.name }}</span>
                  <input type="checkbox" class="hidden" :checked="filters.category === cat.slug" @change="setCategory(cat.slug)" />
                </label>
              </div>
            </div>
            <div class="h-px bg-slate-100 my-4" />
            <!-- Material -->
            <div class="mb-5">
              <p class="text-[10px] font-bold text-slate-500 uppercase tracking-wider mb-3">Material</p>
              <div class="space-y-1.5">
                <label v-for="mat in materials" :key="mat.value" class="flex items-center gap-3 cursor-pointer group py-0.5">
                  <div class="w-4 h-4 rounded border flex items-center justify-center transition-colors flex-shrink-0"
                       :class="filters.material === mat.value ? 'bg-brand-600 border-brand-600' : 'border-slate-300 bg-white'">
                    <Check v-if="filters.material === mat.value" class="w-2.5 h-2.5 text-white" />
                  </div>
                  <span class="text-sm text-slate-600 group-hover:text-slate-900">{{ mat.label }}</span>
                  <input type="checkbox" class="hidden" :checked="filters.material === mat.value" @change="toggleFilter('material', mat.value)" />
                </label>
              </div>
            </div>
            <!-- Sort Desktop -->
            <div class="h-px bg-slate-100 my-4" />
            <div>
              <p class="text-[10px] font-bold text-slate-500 uppercase tracking-wider mb-3">Saralash</p>
              <select v-model="filters.ordering" @change="fetchProducts(true)" class="w-full text-sm border border-slate-200 rounded-lg px-3 py-2 text-slate-700 bg-white focus:outline-none focus:ring-2 focus:ring-brand-400">
                <option v-for="opt in sortOptions" :key="opt.value" :value="opt.value">{{ opt.label }}</option>
              </select>
            </div>
          </div>
        </aside>

        <!-- Desktop Products Grid -->
        <div class="flex-1 min-w-0">
          <div class="flex items-center justify-between mb-5 text-sm text-slate-500">
            <span><strong class="text-slate-900">{{ totalCount }}</strong> ta mahsulot</span>
          </div>
          <div v-if="loading" class="grid grid-cols-2 xl:grid-cols-3 gap-5">
            <div v-for="i in 9" :key="i" class="skeleton rounded-2xl h-80" />
          </div>
          <div v-else-if="!products.length" class="text-center py-20">
            <div class="w-20 h-20 bg-slate-100 rounded-full flex items-center justify-center mx-auto mb-4">
              <Package class="w-10 h-10 text-slate-300" />
            </div>
            <h3 class="text-xl font-bold text-slate-700 mb-2">Mahsulot topilmadi</h3>
            <p class="text-slate-500 mb-5">Filterlarni o'zgartirib ko'ring</p>
            <button @click="resetFilters" class="btn-md btn-outline">Filterlarni tozalash</button>
          </div>
          <div v-else class="grid grid-cols-2 xl:grid-cols-3 gap-5">
            <ProductCard v-for="product in products" :key="product.id" :product="product" />
          </div>
          <!-- Pagination (desktop) -->
          <div v-if="totalPages > 1" class="flex justify-center items-center gap-2 mt-10">
            <button @click="setPage(page - 1)" :disabled="page <= 1" class="btn-md btn-secondary"><ChevronLeft class="w-4 h-4" /></button>
            <button v-for="p in visiblePages" :key="p" @click="setPage(p)"
              class="w-10 h-10 rounded-xl text-sm font-medium transition-all"
              :class="p === page ? 'bg-brand-500 text-white' : 'bg-white text-slate-700 border border-slate-200'">
              {{ p }}
            </button>
            <button @click="setPage(page + 1)" :disabled="page >= totalPages" class="btn-md btn-secondary"><ChevronRight class="w-4 h-4" /></button>
          </div>
        </div>
      </div>

      <!-- Mobile Products Grid -->
      <div class="lg:hidden">
        <!-- Loading -->
        <div v-if="loading" class="grid grid-cols-2 gap-3">
          <div v-for="i in 6" :key="i" class="skeleton rounded-xl h-64" />
        </div>

        <!-- Empty -->
        <div v-else-if="!products.length" class="text-center py-20">
          <div class="w-16 h-16 bg-slate-100 rounded-full flex items-center justify-center mx-auto mb-4">
            <Package class="w-8 h-8 text-slate-300" />
          </div>
          <h3 class="font-bold text-slate-700 mb-2">Mahsulot topilmadi</h3>
          <p class="text-slate-500 text-sm mb-4">Filterlarni o'zgartirib ko'ring</p>
          <button @click="resetFilters" class="btn-sm btn-outline">Tozalash</button>
        </div>

        <!-- Mobile Grid -->
        <div v-else class="grid grid-cols-2 gap-3">
          <div
            v-for="product in products"
            :key="product.id"
            class="bg-white rounded-xl border border-slate-100 overflow-hidden"
          >
            <!-- Image -->
            <div
              class="relative bg-slate-50 aspect-[4/3] flex items-center justify-center p-3 cursor-pointer"
              @click="$router.push(`/product/${product.slug}`)"
            >
              <img
                :src="product.main_image || 'https://placehold.co/200x150/F1F5F9/94A3B8?text=Rasm'"
                :alt="product.name"
                class="max-w-full max-h-full object-contain"
                loading="lazy"
              />
              <div v-if="product.badge" class="absolute top-2 left-2 px-1.5 py-0.5 bg-brand-500 text-white text-[9px] font-bold rounded uppercase">{{ product.badge }}</div>
            </div>
            <!-- Info -->
            <div class="p-3">
              <p class="text-[9px] font-semibold text-slate-400 uppercase tracking-wider mb-0.5">{{ product.category_name }}</p>
              <p class="text-sm font-bold text-slate-900 line-clamp-2 leading-snug mb-3">{{ product.name }}</p>
              <router-link
                :to="`/product/${product.slug}`"
                class="block w-full text-center py-2 bg-brand-950 hover:bg-brand-900 text-white text-xs font-semibold rounded-lg transition-colors"
              >
                Batafsil
              </router-link>
            </div>
          </div>
        </div>

        <!-- Mobile Load More -->
        <div v-if="page < totalPages" class="mt-6 text-center">
          <button @click="loadMore" :disabled="loading" class="btn-md btn-outline w-full">
            <span v-if="!loading">Ko'proq ko'rish</span>
            <div v-else class="spinner" />
          </button>
        </div>
      </div>
    </div>

    <!-- Mobile Filter Sheet (Bottom Drawer) -->
    <Teleport to="body">
      <Transition name="fade">
        <div v-if="showMobileFilters" class="fixed inset-0 z-50 bg-slate-900/50 backdrop-blur-sm" @click.self="showMobileFilters = false">
          <Transition name="slide-up">
            <div v-if="showMobileFilters" class="absolute bottom-0 left-0 right-0 bg-white rounded-t-2xl max-h-[80vh] overflow-y-auto">
              <div class="sticky top-0 bg-white flex items-center justify-between px-5 py-4 border-b border-slate-100">
                <h3 class="font-bold text-slate-900 text-base">Filtrlar</h3>
                <div class="flex items-center gap-3">
                  <button v-if="hasActiveFilters" @click="resetFilters" class="text-sm text-red-500 font-medium">Tozalash</button>
                  <button @click="showMobileFilters = false" class="p-1.5 rounded-xl bg-slate-100"><X class="w-4 h-4" /></button>
                </div>
              </div>
              <div class="p-5 space-y-6">
                <!-- Categories -->
                <div>
                  <p class="text-xs font-bold text-slate-500 uppercase tracking-wider mb-3">Mahsulot turi</p>
                  <div class="flex flex-wrap gap-2">
                    <button
                      @click="setCategory('')"
                      class="px-3 py-1.5 rounded-full text-sm font-medium transition-colors border"
                      :class="!filters.category ? 'bg-brand-950 text-white border-brand-950' : 'border-slate-200 text-slate-700'"
                    >Barchasi</button>
                    <button
                      v-for="cat in categories"
                      :key="cat.slug"
                      @click="setCategory(cat.slug)"
                      class="px-3 py-1.5 rounded-full text-sm font-medium transition-colors border"
                      :class="filters.category === cat.slug ? 'bg-brand-950 text-white border-brand-950' : 'border-slate-200 text-slate-700'"
                    >{{ cat.name }}</button>
                  </div>
                </div>
                <!-- Material -->
                <div>
                  <p class="text-xs font-bold text-slate-500 uppercase tracking-wider mb-3">Material</p>
                  <div class="flex flex-wrap gap-2">
                    <button
                      v-for="mat in materials"
                      :key="mat.value"
                      @click="toggleFilter('material', mat.value)"
                      class="px-3 py-1.5 rounded-full text-sm font-medium transition-colors border"
                      :class="filters.material === mat.value ? 'bg-brand-950 text-white border-brand-950' : 'border-slate-200 text-slate-700'"
                    >{{ mat.label }}</button>
                  </div>
                </div>
                <!-- Sort -->
                <div>
                  <p class="text-xs font-bold text-slate-500 uppercase tracking-wider mb-3">Saralash</p>
                  <div class="space-y-1">
                    <button
                      v-for="opt in sortOptions"
                      :key="opt.value"
                      @click="filters.ordering = opt.value; fetchProducts(true)"
                      class="flex items-center gap-3 w-full px-3 py-2.5 rounded-lg text-sm font-medium transition-colors"
                      :class="filters.ordering === opt.value ? 'bg-brand-50 text-brand-700' : 'text-slate-700 hover:bg-slate-50'"
                    >
                      <div class="w-4 h-4 rounded-full border-2 flex items-center justify-center flex-shrink-0"
                           :class="filters.ordering === opt.value ? 'border-brand-600' : 'border-slate-300'">
                        <div v-if="filters.ordering === opt.value" class="w-2 h-2 rounded-full bg-brand-600" />
                      </div>
                      {{ opt.label }}
                    </button>
                  </div>
                </div>
                <button @click="showMobileFilters = false" class="btn-lg btn-primary w-full">
                  Natijalarni ko'rish ({{ totalCount }})
                </button>
              </div>
            </div>
          </Transition>
        </div>
      </Transition>
    </Teleport>

  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { Filter, ArrowUpDown, X, Package, ChevronLeft, ChevronRight, Check } from '@lucide/vue'
import { productsApi } from '@/api/products'
import ProductCard from '@/components/client/ProductCard.vue'

const route  = useRoute()
const router = useRouter()

const products    = ref([])
const categories  = ref([])
const loading     = ref(true)
const totalCount  = ref(0)
const page        = ref(1)
const pageSize    = 12

const showMobileFilters = ref(false)
const showSortMenu      = ref(false)

const totalPages = computed(() => Math.ceil(totalCount.value / pageSize))
const visiblePages = computed(() => {
  const pages = []
  const start = Math.max(1, page.value - 2)
  const end   = Math.min(totalPages.value, page.value + 2)
  for (let i = start; i <= end; i++) pages.push(i)
  return pages
})

const filters = ref({
  search:   route.query.search || '',
  category: route.query.category || '',
  material: '',
  ordering: '-created_at',
})

const hasActiveFilters = computed(() =>
  filters.value.category || filters.value.material || filters.value.search
)

const materials = [
  { label: 'Alyuminiy', value: 'alyuminiy' },
  { label: 'PVX (Plastik)', value: 'pvx' },
  { label: "Yog'och", value: 'yogoch' },
]

const sortOptions = [
  { label: 'Eng yangi',         value: '-created_at' },
  { label: 'Arzondan qimmatga', value: 'base_price' },
  { label: 'Qimmatdan arzonga', value: '-base_price' },
]

async function fetchProducts(reset = false) {
  if (reset) page.value = 1
  loading.value = true
  try {
    const params = { page: page.value, page_size: pageSize, ordering: filters.value.ordering }
    if (filters.value.search)   params.search   = filters.value.search
    if (filters.value.category) params.category = filters.value.category
    if (filters.value.material) params.material = filters.value.material
    const res = await productsApi.getProducts(params)
    products.value  = res.data.results || res.data
    totalCount.value = res.data.count || products.value.length
  } catch {}
  loading.value = false
}

async function loadMore() {
  if (page.value >= totalPages.value) return
  page.value++
  loading.value = true
  try {
    const params = { page: page.value, page_size: pageSize, ordering: filters.value.ordering }
    if (filters.value.search)   params.search   = filters.value.search
    if (filters.value.category) params.category = filters.value.category
    if (filters.value.material) params.material = filters.value.material
    const res = await productsApi.getProducts(params)
    products.value.push(...(res.data.results || []))
    totalCount.value = res.data.count || products.value.length
  } catch {}
  loading.value = false
}

function setCategory(slug) {
  filters.value.category = filters.value.category === slug ? '' : slug
  fetchProducts(true)
}

function toggleFilter(key, value) {
  filters.value[key] = filters.value[key] === value ? '' : value
  fetchProducts(true)
}

function resetFilters() {
  filters.value = { search: '', category: '', material: '', ordering: '-created_at' }
  fetchProducts(true)
  showMobileFilters.value = false
}

function setPage(p) {
  if (p < 1 || p > totalPages.value) return
  page.value = p
  fetchProducts()
  window.scrollTo({ top: 0, behavior: 'smooth' })
}

onMounted(async () => {
  const catsRes = await productsApi.getCategories()
  categories.value = catsRes.data.results || catsRes.data
  await fetchProducts()
})
</script>

<style scoped>
.scrollbar-hide::-webkit-scrollbar { display: none; }
.scrollbar-hide { -ms-overflow-style: none; scrollbar-width: none; }

.slide-up-enter-active, .slide-up-leave-active { transition: transform 0.3s ease; }
.slide-up-enter-from, .slide-up-leave-to { transform: translateY(100%); }
</style>
