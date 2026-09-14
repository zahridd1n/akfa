<template>
  <div>
    <!-- =================== HERO BANNER =================== -->
    <section class="relative min-h-[70vh] flex items-center justify-center overflow-hidden">
      <!-- Background Image (First banner from API or fallback) -->
      <div class="absolute inset-0">
        <img
          v-if="banners.length > 0"
          :src="banners[0].image"
          alt="Hero"
          class="w-full h-full object-cover"
        />
        <div v-else class="w-full h-full bg-slate-300"></div>
        <div class="absolute inset-0 bg-black/40"></div>
      </div>

      <!-- Hero Content -->
      <div class="container-custom relative z-10 text-center py-20 px-4">
        <div class="max-w-4xl mx-auto">
          <h1 class="text-4xl md:text-5xl lg:text-6xl font-bold text-white leading-tight mb-6 tracking-tight">
            Uyingiz uchun zamonaviy AKFA eshik va romlar
          </h1>
          <p class="text-base md:text-lg text-slate-200 mb-10 max-w-2xl mx-auto leading-relaxed">
            Mukammal sifat, innovatsion dizayn va uzoq muddatli xizmat kafolati. Bizning eshik va derazalarimiz bilan uyingizni yanada shinam va zamonaviy qiling. Professional yondashuv va aniq o'rnatish.
          </p>

          <div class="flex flex-wrap items-center justify-center gap-4">
            <router-link to="/catalog" class="btn-lg bg-brand-950 hover:bg-brand-900 text-white font-medium px-8 py-3.5 rounded-lg transition-colors uppercase tracking-wider text-sm">
              Katalogni ko'rish
            </router-link>
            <button @click="openAuthModal" class="btn-lg border-2 border-white text-white hover:bg-white hover:text-slate-900 font-medium px-8 py-3.5 rounded-lg transition-colors uppercase tracking-wider text-sm">
              Ro'yxatdan o'tish
            </button>
          </div>
        </div>
      </div>
    </section>

    <!-- =================== MAHSULOT TOIFALARI (Bento Box) =================== -->
    <section class="py-20 bg-slate-50">
      <div class="container-custom">
        <h2 class="text-2xl font-bold text-slate-900 mb-10">Mahsulot toifalari</h2>

        <div v-if="categoriesLoading" class="flex justify-center py-10">
          <div class="spinner border-brand-950"></div>
        </div>

        <div v-else class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          
          <!-- Derazalar (Large Vertical) -->
          <router-link
            :to="`/catalog?category=${getCategoryData('Deraza').slug || 'deraza'}`"
            class="group bg-slate-100 rounded-3xl p-8 flex flex-col justify-end hover:bg-slate-200 transition-colors lg:col-span-1 lg:row-span-2 min-h-[400px] lg:min-h-full relative overflow-hidden"
          >
            <img v-if="getCategoryData('Deraza').icon" :src="getCategoryData('Deraza').icon" class="absolute inset-0 w-full h-full object-cover opacity-80 group-hover:scale-105 transition-transform duration-500" />
            <div class="relative z-10 bg-white/80 backdrop-blur-sm p-4 rounded-2xl">
              <h3 class="text-xl font-bold text-slate-900 mb-1 group-hover:text-brand-600 transition-colors">Derazalar</h3>
              <p class="text-sm text-slate-500">Energiya tejamkor va ishonchli yechimlar</p>
            </div>
          </router-link>

          <!-- Eshiklar (Wide Horizontal) -->
          <router-link
            :to="`/catalog?category=${getCategoryData('Eshik').slug || 'eshik'}`"
            class="group bg-slate-100 rounded-3xl p-8 flex flex-col justify-end hover:bg-slate-200 transition-colors lg:col-span-2 min-h-[250px] relative overflow-hidden"
          >
            <img v-if="getCategoryData('Eshik').icon" :src="getCategoryData('Eshik').icon" class="absolute inset-0 w-full h-full object-cover opacity-80 group-hover:scale-105 transition-transform duration-500" />
            <div class="relative z-10 bg-white/80 backdrop-blur-sm p-4 rounded-2xl w-max">
              <h3 class="text-xl font-bold text-slate-900 group-hover:text-brand-600 transition-colors">Eshiklar</h3>
            </div>
          </router-link>

          <!-- Balkon romlari (Square) -->
          <router-link
            :to="`/catalog?category=${getCategoryData('Balkon').slug || 'balkon'}`"
            class="group bg-slate-100 rounded-3xl p-8 flex flex-col items-center justify-center text-center hover:bg-slate-200 transition-colors min-h-[250px] relative overflow-hidden"
          >
            <img v-if="getCategoryData('Balkon').icon" :src="getCategoryData('Balkon').icon" class="absolute inset-0 w-full h-full object-cover opacity-80 group-hover:scale-105 transition-transform duration-500" />
            <div class="relative z-10 bg-white/80 backdrop-blur-sm p-4 rounded-2xl w-full flex flex-col items-center">
              <div v-if="!getCategoryData('Balkon').icon" class="w-12 h-12 mb-4 text-brand-950 group-hover:text-brand-600 transition-colors">
                <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M3 21h18"/><path d="M5 21V7l8-4 8 4v14"/><path d="M9 21v-4a2 2 0 0 1 2-2h2a2 2 0 0 1 2 2v4"/><path d="M8 11h8"/></svg>
              </div>
              <h3 class="text-lg font-bold text-slate-900 group-hover:text-brand-600 transition-colors">Balkon romlari</h3>
            </div>
          </router-link>

          <!-- Fasad (Square) -->
          <router-link
            :to="`/catalog?category=${getCategoryData('Fasad').slug || 'fasad'}`"
            class="group bg-slate-100 rounded-3xl p-8 flex flex-col items-center justify-center text-center hover:bg-slate-200 transition-colors min-h-[250px] relative overflow-hidden"
          >
            <img v-if="getCategoryData('Fasad').icon" :src="getCategoryData('Fasad').icon" class="absolute inset-0 w-full h-full object-cover opacity-80 group-hover:scale-105 transition-transform duration-500" />
            <div class="relative z-10 bg-white/80 backdrop-blur-sm p-4 rounded-2xl w-full flex flex-col items-center">
              <div v-if="!getCategoryData('Fasad').icon" class="w-12 h-12 mb-4 text-brand-950 group-hover:text-brand-600 transition-colors">
                <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M5 21h14"/><path d="M7 21V5a2 2 0 0 1 2-2h6a2 2 0 0 1 2 2v16"/><path d="M14 12h1"/></svg>
              </div>
              <h3 class="text-lg font-bold text-slate-900 group-hover:text-brand-600 transition-colors">Fasad</h3>
            </div>
          </router-link>

          <!-- Maxsus konstruksiyalar (Full width bottom) -->
          <router-link
            :to="`/catalog?category=${getCategoryData('Maxsus').slug || 'maxsus'}`"
            class="group bg-slate-100 rounded-3xl p-8 flex flex-col items-center justify-center text-center hover:bg-slate-200 transition-colors lg:col-span-3 min-h-[200px] relative overflow-hidden"
          >
            <img v-if="getCategoryData('Maxsus').icon" :src="getCategoryData('Maxsus').icon" class="absolute inset-0 w-full h-full object-cover opacity-80 group-hover:scale-105 transition-transform duration-500" />
            <div class="relative z-10 bg-white/80 backdrop-blur-sm p-4 rounded-2xl">
              <div v-if="!getCategoryData('Maxsus').icon" class="w-12 h-12 mb-4 text-brand-950 group-hover:text-brand-600 transition-colors mx-auto">
                <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M12 2L2 22h20L12 2z"/><path d="M12 2v20"/></svg>
              </div>
              <h3 class="text-xl font-bold text-slate-900 mb-2 group-hover:text-brand-600 transition-colors">Maxsus konstruksiyalar</h3>
              <p class="text-sm text-slate-500">Nostandart o'lchamlar va individual loyihalar</p>
            </div>
          </router-link>

        </div>
      </div>
    </section>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { productsApi } from '@/api/products'

const banners = ref([])
const categories = ref([])
const categoriesLoading = ref(true)

// API fetches
onMounted(async () => {
  try {
    const [bannersRes, catsRes] = await Promise.all([
      productsApi.getBanners(),
      productsApi.getCategories()
    ])
    banners.value = bannersRes.data.results || bannersRes.data
    categories.value = catsRes.data.results || catsRes.data
  } catch (error) {
    console.error(error)
  } finally {
    categoriesLoading.value = false
  }
})

// Helper to safely get category data
function getCategoryData(nameSubstring) {
  return categories.value.find(c => c.name.toLowerCase().includes(nameSubstring.toLowerCase())) || {}
}

// Global auth modal trigger
function openAuthModal() {
  window.dispatchEvent(new CustomEvent('auth:open-modal'))
}
</script>
