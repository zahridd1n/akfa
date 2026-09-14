<template>
  <div class="bg-white rounded-2xl border border-slate-100 hover:border-slate-200 hover:shadow-lg transition-all duration-300 flex flex-col overflow-hidden group">
    <!-- Image Area -->
    <div class="relative bg-slate-50 p-4 flex items-center justify-center aspect-[4/3] overflow-hidden">
      <img
        :src="mainImage"
        :alt="product.name"
        class="max-w-full max-h-full object-contain group-hover:scale-105 transition-transform duration-500 cursor-pointer"
        loading="lazy"
        @error="handleImgError"
        @click="goToDetail"
      />
      <!-- Badges -->
      <div class="absolute top-4 right-4 flex flex-col gap-2">
        <span v-if="product.badge" class="px-2.5 py-1 bg-brand-50 text-brand-600 text-[10px] font-bold uppercase tracking-wider rounded">{{ product.badge }}</span>
      </div>
    </div>

    <!-- Content Area -->
    <div class="p-5 flex flex-col flex-1">
      <!-- Category -->
      <p class="text-[10px] font-semibold text-slate-400 uppercase tracking-widest mb-1">{{ product.category_name }}</p>
      
      <!-- Title -->
      <h3 class="text-lg font-bold text-slate-900 mb-3">{{ product.name }}</h3>

      <!-- Features (Example: Iqlim) -->
      <div class="flex items-center gap-1.5 mb-4 text-xs text-slate-500">
        <svg class="w-3.5 h-3.5" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z"></path></svg>
        <span>Iqlim: Issiq/Sovuq</span>
      </div>

      <!-- Colors -->
      <div v-if="product.colors?.length" class="flex items-center gap-2 mb-6">
        <div
          v-for="color in product.colors.slice(0, 3)"
          :key="color.id"
          class="w-5 h-5 rounded-full border border-slate-200"
          :style="{ backgroundColor: color.hex_code }"
          :title="color.name"
        />
        <span v-if="product.colors.length > 3" class="text-[10px] font-medium text-slate-500 ml-1">+{{ product.colors.length - 3 }}</span>
      </div>

      <!-- Buttons -->
      <div class="mt-auto flex items-center gap-3">
        <router-link :to="`/product/${product.slug}`" class="flex-1 btn-md bg-brand-950 hover:bg-brand-900 text-white font-medium text-xs uppercase tracking-wider text-center py-2.5 rounded-lg transition-colors">
          Batafsil
        </router-link>
        <button class="w-10 h-10 rounded-lg bg-slate-100 hover:bg-slate-200 flex items-center justify-center text-slate-600 hover:text-slate-900 transition-colors">
          <svg class="w-4 h-4" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M3 3h2l.4 2M7 13h10l4-8H5.4M7 13L5.4 5M7 13l-2.293 2.293c-.63.63-.184 1.707.707 1.707H17m0 0a2 2 0 100 4 2 2 0 000-4zm-8 2a2 2 0 11-4 0 2 2 0 014 0z"></path></svg>
        </button>
      </div>
    </div>
  </div>
</template>

<script setup>
import { computed } from 'vue'
import { useRouter } from 'vue-router'

const router = useRouter()

function goToDetail() {
  router.push(`/product/${props.product.slug}`)
}

const props = defineProps({
  product: { type: Object, required: true }
})

const mainImage = computed(() => {
  // Use main_image if available (from ProductListSerializer)
  if (props.product.main_image) return props.product.main_image;
  // Fallback for ProductDetailSerializer where images list is available
  const mainImg = props.product.images?.find(i => i.is_main) || props.product.images?.[0]
  return mainImg?.image || 'https://via.placeholder.com/400x300/F1F5F9/94A3B8?text=Rasm'
})

function handleImgError(e) {
  e.target.src = 'https://via.placeholder.com/400x300/F1F5F9/94A3B8?text=Rasm'
}
</script>
