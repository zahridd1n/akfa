<template>
  <div class="relative w-full" ref="searchContainerRef">
    <!-- Search Input Wrapper -->
    <div class="relative flex items-center">
      <input
        ref="inputRef"
        v-model="query"
        @input="onInput"
        @focus="onFocus"
        @keydown.down.prevent="onArrowDown"
        @keydown.up.prevent="onArrowUp"
        @keydown.enter.prevent="onEnter"
        @keydown.esc="closeDropdown"
        type="text"
        :placeholder="placeholder || 'Mahsulotlarni qidirish...'"
        class="w-full pl-10 pr-10 py-2.5 rounded-2xl border text-sm transition-all focus:outline-none focus:ring-2 focus:ring-brand-400 focus:bg-white"
        :class="[
          customInputClass || 'border-[#C7DDEA]/80 bg-white/90 text-slate-800 placeholder-slate-400 shadow-sm',
          isOpen ? 'ring-2 ring-brand-400 bg-white' : ''
        ]"
      />

      <!-- Search Icon (Left) -->
      <Search class="absolute left-3.5 w-4 h-4 text-slate-400 pointer-events-none" />

      <!-- Right Action: Loading or Clear Button -->
      <div class="absolute right-3 flex items-center">
        <div v-if="loading" class="w-4 h-4 border-2 border-brand-600 border-t-transparent rounded-full animate-spin" />
        <button
          v-else-if="query"
          @click="clearQuery"
          class="p-1 rounded-full text-slate-400 hover:text-slate-600 hover:bg-slate-100 transition-colors"
          type="button"
        >
          <X class="w-3.5 h-3.5" />
        </button>
      </div>
    </div>

    <!-- Live Results Dropdown -->
    <Transition name="search-dropdown">
      <div
        v-if="isOpen && (query.trim().length > 0 || results.length > 0)"
        class="absolute left-0 right-0 top-full mt-2 bg-white rounded-2xl shadow-2xl border border-slate-100 overflow-hidden z-50 divide-y divide-slate-100 max-h-[420px] flex flex-col"
        :style="{ minWidth: minDropdownWidth ? `${minDropdownWidth}px` : '100%' }"
      >

        <!-- Loading state -->
        <div v-if="loading && results.length === 0" class="p-4 space-y-3">
          <div v-for="i in 3" :key="i" class="flex items-center gap-3 animate-pulse">
            <div class="w-12 h-12 bg-slate-100 rounded-xl flex-shrink-0" />
            <div class="flex-1 space-y-1.5">
              <div class="h-3.5 bg-slate-100 rounded w-3/4" />
              <div class="h-3 bg-slate-100 rounded w-1/2" />
            </div>
          </div>
        </div>

        <!-- Results list -->
        <div v-else-if="results.length > 0" class="overflow-y-auto flex-1 p-2 space-y-1">
          <div class="px-3 py-1.5 text-[11px] font-bold uppercase tracking-wider text-slate-400 flex items-center justify-between">
            <span>Mahsulotlar ({{ totalCount }})</span>
            <span class="text-[10px] lowercase font-normal">tezkor o'tish</span>
          </div>

          <div
            v-for="(product, idx) in results"
            :key="product.id"
            @click="selectProduct(product)"
            @mouseenter="selectedIndex = idx"
            class="flex items-center gap-3 p-2.5 rounded-xl cursor-pointer transition-all duration-150 group"
            :class="selectedIndex === idx ? 'bg-brand-50 text-slate-900' : 'hover:bg-slate-50 text-slate-700'"
          >
            <!-- Thumbnail Image -->
            <div class="w-12 h-12 rounded-xl bg-slate-100 overflow-hidden flex-shrink-0 border border-slate-200/60 flex items-center justify-center">
              <img
                v-if="product.main_image"
                :src="product.main_image"
                :alt="product.name"
                class="w-full h-full object-cover group-hover:scale-105 transition-transform"
              />
              <Package v-else class="w-5 h-5 text-slate-300" />
            </div>

            <!-- Title, Category & Badge -->
            <div class="flex-1 min-w-0">
              <div class="flex items-center gap-2">
                <p class="text-sm font-semibold truncate group-hover:text-brand-900" :class="selectedIndex === idx ? 'text-brand-950 font-bold' : 'text-slate-800'">
                  {{ product.name }}
                </p>
                <span
                  v-if="product.badge"
                  class="px-1.5 py-0.5 rounded text-[10px] font-bold uppercase"
                  :class="getBadgeClass(product.badge)"
                >
                  {{ getBadgeLabel(product.badge) }}
                </span>
              </div>
              <p class="text-xs text-slate-400 truncate mt-0.5">
                {{ product.category_name || "Boshqa" }}
              </p>
            </div>

            <!-- Price -->
            <div class="text-right flex-shrink-0">
              <p class="text-sm font-extrabold text-brand-950">
                {{ formatPrice(product.base_price) }}
              </p>
              <p class="text-[10px] text-slate-400">
                {{ product.price_type === 'per_sqm' ? 'm² uchun' : 'dona' }}
              </p>
            </div>
          </div>
        </div>

        <!-- Empty state -->
        <div v-else-if="!loading && query.trim().length > 0" class="p-6 text-center">
          <div class="w-10 h-10 bg-slate-100 rounded-full flex items-center justify-center mx-auto mb-2 text-slate-400">
            <Search class="w-5 h-5" />
          </div>
          <p class="text-sm font-semibold text-slate-800">Hech qanday mahsulot topilmadi</p>
          <p class="text-xs text-slate-400 mt-1">
            "{{ query }}" so'rovi bo'yicha mahsulot topilmadi. Boshqa so'z bilan qidirib ko'ring.
          </p>
        </div>

        <!-- Footer / View all button -->
        <div v-if="results.length > 0" class="p-2 bg-slate-50 border-t border-slate-100 flex items-center justify-between">
          <button
            @click="goToCatalogSearch"
            class="w-full py-2 px-3 text-center text-xs font-bold text-brand-800 hover:text-brand-950 hover:bg-brand-100/60 rounded-xl transition-colors flex items-center justify-center gap-1.5"
          >
            <span>Barcha natijalarni ko'rish ({{ totalCount }} ta)</span>
            <ArrowRight class="w-3.5 h-3.5" />
          </button>
        </div>

      </div>
    </Transition>
  </div>
</template>

<script setup>
import { ref, watch, onMounted, onUnmounted } from 'vue'
import { useRouter } from 'vue-router'
import { Search, X, Package, ArrowRight } from '@lucide/vue'
import { productsApi } from '@/api/products'

const props = defineProps({
  placeholder: { type: String, default: '' },
  customInputClass: { type: String, default: '' },
  minDropdownWidth: { type: [Number, String], default: null },
  autofocus: { type: Boolean, default: false },
})

const emit = defineEmits(['select', 'search-submit'])

const router = useRouter()
const searchContainerRef = ref(null)
const inputRef = ref(null)

const query = ref('')
const results = ref([])
const totalCount = ref(0)
const loading = ref(false)
const isOpen = ref(false)
const selectedIndex = ref(-1)

let debounceTimer = null

function formatPrice(val) {
  if (!val) return "0 so'm"
  return Number(val).toLocaleString('uz-UZ') + " so'm"
}

function getBadgeLabel(badge) {
  const map = { new: 'Yangi', warm: 'Issiq', sale: 'Chegirma' }
  return map[badge] || badge
}

function getBadgeClass(badge) {
  const map = {
    new: 'bg-emerald-100 text-emerald-700',
    warm: 'bg-amber-100 text-amber-700',
    sale: 'bg-red-100 text-red-600',
  }
  return map[badge] || 'bg-slate-100 text-slate-600'
}

function onInput() {
  selectedIndex.value = -1
  if (!query.value.trim()) {
    results.value = []
    totalCount.value = 0
    loading.value = false
    isOpen.value = false
    return
  }

  isOpen.value = true
  loading.value = true

  clearTimeout(debounceTimer)
  debounceTimer = setTimeout(async () => {
    try {
      const res = await productsApi.getProducts({
        search: query.value.trim(),
        page_size: 6,
      })
      results.value = res.data.results || []
      totalCount.value = res.data.count || 0
    } catch (err) {
      console.error("Search error:", err)
      results.value = []
    } finally {
      loading.value = false
    }
  }, 250)
}

function onFocus() {
  if (query.value.trim() && results.value.length > 0) {
    isOpen.value = true
  }
}

function clearQuery() {
  query.value = ''
  results.value = []
  totalCount.value = 0
  isOpen.value = false
  selectedIndex.value = -1
}

function closeDropdown() {
  isOpen.value = false
  selectedIndex.value = -1
}

function selectProduct(product) {
  closeDropdown()
  emit('select', product)
  router.push(`/product/${product.slug}`)
}

function goToCatalogSearch() {
  if (!query.value.trim()) return
  const q = query.value.trim()
  closeDropdown()
  emit('search-submit', q)
  router.push({ name: 'catalog', query: { search: q } })
}

function onArrowDown() {
  if (!isOpen.value || results.value.length === 0) return
  selectedIndex.value = (selectedIndex.value + 1) % results.value.length
}

function onArrowUp() {
  if (!isOpen.value || results.value.length === 0) return
  selectedIndex.value = (selectedIndex.value - 1 + results.value.length) % results.value.length
}

function onEnter() {
  if (selectedIndex.value >= 0 && selectedIndex.value < results.value.length) {
    selectProduct(results.value[selectedIndex.value])
  } else {
    goToCatalogSearch()
  }
}

function handleClickOutside(e) {
  if (searchContainerRef.value && !searchContainerRef.value.contains(e.target)) {
    closeDropdown()
  }
}

function focus() {
  inputRef.value?.focus()
}

defineExpose({ focus, clearQuery })

onMounted(() => {
  document.addEventListener('click', handleClickOutside)
  if (props.autofocus) {
    setTimeout(() => { inputRef.value?.focus() }, 100)
  }
})

onUnmounted(() => {
  document.removeEventListener('click', handleClickOutside)
  clearTimeout(debounceTimer)
})
</script>

<style scoped>
.search-dropdown-enter-active,
.search-dropdown-leave-active {
  transition: all 0.2s cubic-bezier(0.16, 1, 0.3, 1);
}
.search-dropdown-enter-from,
.search-dropdown-leave-to {
  opacity: 0;
  transform: translateY(-8px) scale(0.98);
}
</style>
