<template>
  <div class="min-h-screen" style="background: #EBF3F8;">

    <!-- =================== HERO BANNER =================== -->
    <section class="relative overflow-hidden">
      <!-- Mobile Hero (figmaga mos) -->
      <div class="md:hidden">
        <div class="relative min-h-[380px] flex flex-col justify-end overflow-hidden rounded-b-3xl">
          <!-- Background image -->
          <div class="absolute inset-0">
            <img
              v-if="banners.length"
              :src="banners[0].image"
              alt="Hero"
              class="w-full h-full object-cover"
            />
            <div v-else class="w-full h-full bg-gradient-to-br from-[#C7DDEA] to-[#8BB8D4]" />
          </div>

          <!-- Content card at bottom -->
          <div class="relative z-10 m-4 mb-6 bg-white rounded-2xl p-5 shadow-lg">
            <h1 class="text-xl font-bold text-slate-900 mb-2 leading-snug">
              Uyingiz uchun zamonaviy AKFA eshik va romlar
            </h1>
            <p class="text-sm text-slate-500 mb-4 leading-relaxed">
              Sifat, xavfsizlik va zamonaviy dizayn uyg'unligi.
            </p>
            <div class="flex flex-col gap-2">
              <router-link to="/catalog"
                class="block text-center py-3 bg-brand-950 hover:bg-brand-900 text-white rounded-xl font-semibold text-sm transition-colors">
                Ro'yxatdan o'tish
              </router-link>
              <button @click="openAuthModal"
                class="block text-center py-3 border-2 border-brand-950 text-brand-950 rounded-xl font-semibold text-sm transition-colors hover:bg-brand-50">
                Sotuvchi bilan bog'lanish
              </button>
            </div>
          </div>
        </div>
      </div>

      <!-- Desktop Hero -->
      <div class="hidden md:block relative min-h-[70vh] flex items-center">
        <div class="absolute inset-0">
          <img
            v-if="banners.length"
            :src="banners[0].image"
            alt="Hero"
            class="w-full h-full object-cover"
          />
          <div v-else class="w-full h-full bg-gradient-to-br from-brand-900 to-brand-700" />
          <div class="absolute inset-0 bg-gradient-to-r from-black/60 via-black/30 to-transparent" />
        </div>
        <div class="relative z-10 container-custom py-24 px-6">
          <div class="max-w-xl">
            <h1 class="text-4xl lg:text-5xl xl:text-6xl font-bold text-white leading-tight mb-5">
              Uyingiz uchun zamonaviy AKFA eshik va romlar
            </h1>
            <p class="text-base text-slate-200 mb-8 leading-relaxed">
              Sifat, xavfsizlik va zamonaviy dizayn uyg'unligi. Mukammal yechimlar bilan uyingizni yangilang.
            </p>
            <div class="flex flex-wrap gap-3">
              <router-link to="/catalog"
                class="px-8 py-3.5 bg-brand-950 hover:bg-brand-900 text-white rounded-xl font-semibold text-sm uppercase tracking-wider transition-colors">
                Katalogni ko'rish
              </router-link>
              <button @click="openAuthModal"
                class="px-8 py-3.5 border-2 border-white text-white hover:bg-white hover:text-slate-900 rounded-xl font-semibold text-sm uppercase tracking-wider transition-colors">
                Bog'lanish
              </button>
            </div>
          </div>
        </div>
      </div>
    </section>

    <!-- =================== KATEGORIYALAR =================== -->
    <section class="px-4 pt-6 pb-2 md:py-10 md:container-custom">
      <div class="flex items-center justify-between mb-4">
        <h2 class="text-lg md:text-2xl font-bold text-slate-900">Kategoriyalar</h2>
      </div>

      <!-- Loading -->
      <div v-if="categoriesLoading" class="flex gap-4 overflow-x-auto pb-2">
        <div v-for="i in 4" :key="i" class="skeleton w-24 h-24 rounded-2xl flex-shrink-0" />
      </div>

      <!-- Mobile: horizontal scroll chips -->
      <div v-else class="md:hidden flex gap-3 overflow-x-auto pb-2 scrollbar-hide -mx-4 px-4">
        <router-link
          v-for="cat in categories"
          :key="cat.slug"
          :to="`/catalog?category=${cat.slug}`"
          class="flex-shrink-0 flex flex-col items-center gap-2 group"
        >
          <div class="w-20 h-20 rounded-2xl bg-white border border-[#C7DDEA]/60 flex items-center justify-center overflow-hidden shadow-sm group-hover:border-brand-300 transition-colors">
            <img v-if="cat.icon" :src="cat.icon" :alt="cat.name" class="w-full h-full object-cover" />
            <div v-else class="w-10 h-10 text-brand-700">
              <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5"><path stroke-linecap="round" stroke-linejoin="round" d="M2.25 12l8.954-8.955c.44-.439 1.152-.439 1.591 0L21.75 12M4.5 9.75v10.125c0 .621.504 1.125 1.125 1.125H9.75v-4.875c0-.621.504-1.125 1.125-1.125h2.25c.621 0 1.125.504 1.125 1.125V21h4.125c.621 0 1.125-.504 1.125-1.125V9.75" /></svg>
            </div>
          </div>
          <span class="text-xs font-medium text-slate-700 text-center w-20 line-clamp-2 leading-tight">{{ cat.name }}</span>
        </router-link>
      </div>

      <!-- Desktop: Bento Box Layout -->
      <div v-if="!categoriesLoading" class="hidden md:grid grid-cols-2 lg:grid-cols-3 gap-6">
        
        <!-- Derazalar (Large Vertical) -->
        <router-link
          :to="`/catalog?category=${getCategoryData('Deraza').slug || 'deraza'}`"
          class="group bg-white border border-[#C7DDEA]/50 rounded-3xl p-8 flex flex-col justify-end hover:border-brand-300 hover:shadow-md transition-all duration-300 lg:col-span-1 lg:row-span-2 min-h-[400px] lg:min-h-full relative overflow-hidden"
        >
          <img v-if="getCategoryData('Deraza').icon" :src="getCategoryData('Deraza').icon" class="absolute inset-0 w-full h-full object-cover opacity-80 group-hover:scale-105 transition-transform duration-500" />
          <div v-else class="absolute inset-0 bg-gradient-to-br from-blue-400 to-indigo-600 opacity-80 group-hover:opacity-100 transition-opacity duration-500"></div>
          <div class="relative z-10 bg-white/90 backdrop-blur-sm p-5 rounded-2xl border border-white/40 shadow-sm">
            <h3 class="text-xl font-bold text-slate-900 mb-1 group-hover:text-brand-600 transition-colors">Derazalar</h3>
            <p class="text-sm text-slate-500">Energiya tejamkor va ishonchli yechimlar</p>
          </div>
        </router-link>

        <!-- Eshiklar (Wide Horizontal) -->
        <router-link
          :to="`/catalog?category=${getCategoryData('Eshik').slug || 'eshik'}`"
          class="group bg-white border border-[#C7DDEA]/50 rounded-3xl p-8 flex flex-col justify-end hover:border-brand-300 hover:shadow-md transition-all duration-300 lg:col-span-2 min-h-[250px] relative overflow-hidden"
        >
          <img v-if="getCategoryData('Eshik').icon" :src="getCategoryData('Eshik').icon" class="absolute inset-0 w-full h-full object-cover opacity-80 group-hover:scale-105 transition-transform duration-500" />
          <div v-else class="absolute inset-0 bg-gradient-to-tr from-emerald-400 to-teal-500 opacity-80 group-hover:opacity-100 transition-opacity duration-500"></div>
          <div class="relative z-10 bg-white/90 backdrop-blur-sm p-5 rounded-2xl border border-white/40 w-max shadow-sm">
            <h3 class="text-xl font-bold text-slate-900 group-hover:text-brand-600 transition-colors">Eshiklar</h3>
          </div>
        </router-link>

        <!-- Balkon romlari (Square) -->
        <router-link
          :to="`/catalog?category=${getCategoryData('Balkon').slug || 'balkon'}`"
          class="group bg-white border border-[#C7DDEA]/50 rounded-3xl p-8 flex flex-col items-center justify-center text-center hover:border-brand-300 hover:shadow-md transition-all duration-300 min-h-[250px] relative overflow-hidden"
        >
          <img v-if="getCategoryData('Balkon').icon" :src="getCategoryData('Balkon').icon" class="absolute inset-0 w-full h-full object-cover opacity-80 group-hover:scale-105 transition-transform duration-500" />
          <div v-else class="absolute inset-0 bg-gradient-to-br from-amber-400 to-orange-500 opacity-80 group-hover:opacity-100 transition-opacity duration-500"></div>
          <div class="relative z-10 bg-white/90 backdrop-blur-sm p-5 rounded-2xl border border-white/40 w-full flex flex-col items-center shadow-sm">
            <div v-if="!getCategoryData('Balkon').icon" class="w-12 h-12 mb-4 text-orange-600 group-hover:scale-110 transition-transform duration-300">
              <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M3 21h18"/><path d="M5 21V7l8-4 8 4v14"/><path d="M9 21v-4a2 2 0 0 1 2-2h2a2 2 0 0 1 2 2v4"/><path d="M8 11h8"/></svg>
            </div>
            <h3 class="text-lg font-bold text-slate-900 group-hover:text-brand-600 transition-colors">Balkon romlari</h3>
          </div>
        </router-link>

        <!-- Fasad (Square) -->
        <router-link
          :to="`/catalog?category=${getCategoryData('Fasad').slug || 'fasad'}`"
          class="group bg-white border border-[#C7DDEA]/50 rounded-3xl p-8 flex flex-col items-center justify-center text-center hover:border-brand-300 hover:shadow-md transition-all duration-300 min-h-[250px] relative overflow-hidden"
        >
          <img v-if="getCategoryData('Fasad').icon" :src="getCategoryData('Fasad').icon" class="absolute inset-0 w-full h-full object-cover opacity-80 group-hover:scale-105 transition-transform duration-500" />
          <div v-else class="absolute inset-0 bg-gradient-to-br from-purple-500 to-pink-500 opacity-80 group-hover:opacity-100 transition-opacity duration-500"></div>
          <div class="relative z-10 bg-white/90 backdrop-blur-sm p-5 rounded-2xl border border-white/40 w-full flex flex-col items-center shadow-sm">
            <div v-if="!getCategoryData('Fasad').icon" class="w-12 h-12 mb-4 text-purple-600 group-hover:scale-110 transition-transform duration-300">
              <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M5 21h14"/><path d="M7 21V5a2 2 0 0 1 2-2h6a2 2 0 0 1 2 2v16"/><path d="M14 12h1"/></svg>
            </div>
            <h3 class="text-lg font-bold text-slate-900 group-hover:text-brand-600 transition-colors">Fasad</h3>
          </div>
        </router-link>

        <!-- Maxsus konstruksiyalar (Full width bottom) -->
        <router-link
          :to="`/catalog?category=${getCategoryData('Maxsus').slug || 'maxsus'}`"
          class="group bg-white border border-[#C7DDEA]/50 rounded-3xl p-8 flex flex-col items-center justify-center text-center hover:border-brand-300 hover:shadow-md transition-all duration-300 md:col-span-2 lg:col-span-3 min-h-[200px] relative overflow-hidden"
        >
          <img v-if="getCategoryData('Maxsus').icon" :src="getCategoryData('Maxsus').icon" class="absolute inset-0 w-full h-full object-cover opacity-80 group-hover:scale-105 transition-transform duration-500" />
          <div v-else class="absolute inset-0 bg-gradient-to-r from-cyan-500 to-blue-500 opacity-80 group-hover:opacity-100 transition-opacity duration-500"></div>
          <div class="relative z-10 bg-white/90 backdrop-blur-sm p-5 rounded-2xl border border-white/40 shadow-sm">
            <div v-if="!getCategoryData('Maxsus').icon" class="w-12 h-12 mb-4 text-blue-600 group-hover:scale-110 transition-transform duration-300 mx-auto">
              <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M12 2L2 22h20L12 2z"/><path d="M12 2v20"/></svg>
            </div>
            <h3 class="text-xl font-bold text-slate-900 mb-2 group-hover:text-brand-600 transition-colors">Maxsus konstruksiyalar</h3>
            <p class="text-sm text-slate-500">Nostandart o'lchamlar va individual loyihalar</p>
          </div>
        </router-link>
      </div>
    </section>

    <!-- =================== OMMABOP MAHSULOTLAR =================== -->
    <section class="px-4 pt-6 pb-4 md:py-10 md:container-custom">
      <div class="flex items-center justify-between mb-4">
        <h2 class="text-lg md:text-2xl font-bold text-slate-900">Ommabop mahsulotlar</h2>
        <router-link to="/catalog" class="group flex items-center gap-1.5 px-4 py-2 bg-brand-50 hover:bg-brand-100 text-brand-700 text-sm font-bold rounded-full transition-all duration-300">
          Barchasi
          <ArrowRight class="w-4 h-4 group-hover:translate-x-1 transition-transform" />
        </router-link>
      </div>

      <!-- Loading -->
      <div v-if="productsLoading" class="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-3 md:gap-5">
        <div v-for="i in 4" :key="i" class="skeleton rounded-2xl h-56" />
      </div>

      <!-- Products Grid -->
      <div v-else class="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-3 md:gap-5">
        <div
          v-for="product in featuredProducts"
          :key="product.id"
          class="bg-white rounded-2xl border border-[#C7DDEA]/50 overflow-hidden hover:shadow-md hover:border-brand-200 transition-all duration-200 group"
        >
          <!-- Image -->
          <div
            class="relative bg-[#EBF3F8] aspect-[4/3] flex items-center justify-center p-3 cursor-pointer overflow-hidden"
            @click="$router.push(`/product/${product.slug}`)"
          >
            <img
              :src="product.main_image || 'https://placehold.co/200x150/EBF3F8/94A3B8?text=Rasm'"
              :alt="product.name"
              class="max-w-full max-h-full object-contain group-hover:scale-105 transition-transform duration-300"
              loading="lazy"
            />
          </div>

          <!-- Info -->
          <div class="p-3">
            <p class="text-[10px] text-slate-400 uppercase tracking-wider font-semibold mb-0.5">{{ product.category_name }}</p>
            <p class="text-sm font-bold text-slate-900 line-clamp-2 leading-snug mb-3">{{ product.name }}</p>
            <button
              @click="$router.push(`/product/${product.slug}`)"
              class="w-full flex items-center justify-center w-8 h-8 rounded-xl border-2 border-[#C7DDEA] hover:border-brand-400 hover:bg-brand-50 transition-colors"
              title="Batafsil"
            >
              <Plus class="w-4 h-4 text-slate-600" />
            </button>
          </div>
        </div>
      </div>
    </section>

    <!-- =================== CTA BANNER =================== -->
    <section class="px-4 pb-8 md:pb-16 md:container-custom">
      <div class="bg-brand-950 rounded-3xl p-6 md:p-10 text-center relative overflow-hidden">
        <!-- Decorative circles -->
        <div class="absolute -top-10 -right-10 w-40 h-40 bg-white/5 rounded-full" />
        <div class="absolute -bottom-8 -left-8 w-32 h-32 bg-white/5 rounded-full" />

        <div class="relative z-10">
          <h2 class="text-xl md:text-3xl font-bold text-white mb-2">
            Uyingiz uchun mos AKFA mahsulotini toping
          </h2>
          <p class="text-sm md:text-base text-brand-200 mb-6">
            Mutaxassislarimiz sizga yordam berishga tayyor
          </p>
          <button
            @click="scrollToContact"
            class="px-8 py-3 bg-white text-brand-950 rounded-xl font-bold text-sm hover:bg-brand-50 transition-colors"
          >
            Maslahat olish
          </button>
        </div>
      </div>
    </section>

    <!-- =================== CONTACT SECTION =================== -->
    <section id="contact" class="px-4 pb-8 md:pb-16 md:container-custom">
      <div class="bg-white rounded-3xl border border-[#C7DDEA]/60 p-6 md:p-10">
        <div class="md:flex md:items-center md:gap-12">
          <div class="mb-6 md:mb-0 md:flex-1">
            <h2 class="text-xl md:text-3xl font-bold text-slate-900 mb-3">Biz bilan bog'laning</h2>
            <p class="text-slate-500 text-sm md:text-base mb-5">
              Har qanday savol va takliflaringiz uchun quyidagi ma'lumotlar orqali murojaat qiling.
            </p>
            <div class="space-y-3">
              <div class="flex items-center gap-3 text-sm text-slate-700">
                <div class="w-9 h-9 bg-[#EBF3F8] rounded-xl flex items-center justify-center flex-shrink-0">
                  <Phone class="w-4 h-4 text-brand-700" />
                </div>
                <a href="tel:+998901234567" class="font-semibold hover:text-brand-600">+998 90 123 45 67</a>
              </div>
              <div class="flex items-center gap-3 text-sm text-slate-700">
                <div class="w-9 h-9 bg-[#EBF3F8] rounded-xl flex items-center justify-center flex-shrink-0">
                  <MapPin class="w-4 h-4 text-brand-700" />
                </div>
                <span>{{ siteStore.address || "O'zbekiston" }}</span>
              </div>
              <div class="flex items-center gap-3 text-sm text-slate-700">
                <div class="w-9 h-9 bg-[#EBF3F8] rounded-xl flex items-center justify-center flex-shrink-0">
                  <Clock class="w-4 h-4 text-brand-700" />
                </div>
                <span>Du–Sh: 9:00 – 18:00</span>
              </div>
            </div>
          </div>
          <div class="md:flex-1">
            <form @submit.prevent="submitContact" class="space-y-3">
              <input v-model="contactForm.name" type="text" placeholder="Ismingiz" class="form-input text-sm" required />
              <input v-model="contactForm.phone" type="tel" placeholder="+998 __ ___ __ __" class="form-input text-sm" required />
              <textarea v-model="contactForm.message" rows="3" placeholder="Xabaringiz..." class="form-input text-sm resize-none" />
              <button type="submit" class="w-full py-3 bg-brand-950 hover:bg-brand-900 text-white rounded-xl font-semibold text-sm transition-colors">
                Yuborish
              </button>
            </form>
          </div>
        </div>
      </div>
    </section>

  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { Plus, Phone, MapPin, Clock, ArrowRight } from '@lucide/vue'
import { productsApi } from '@/api/products'
import { useAlertStore } from '@/stores/alert'
import { useSiteStore } from '@/stores/site'

const alertStore = useAlertStore()
const siteStore = useSiteStore()

const banners           = ref([])
const categories        = ref([])
const featuredProducts  = ref([])
const categoriesLoading = ref(true)
const productsLoading   = ref(true)

const contactForm = ref({ name: '', phone: '', message: '' })

onMounted(async () => {
  try {
    siteStore.fetchSettings()
    const [bannersRes, catsRes, prodsRes] = await Promise.all([
      productsApi.getBanners(),
      productsApi.getCategories(),
      productsApi.getProducts({ page_size: 8, ordering: '-created_at' }),
    ])
    banners.value          = bannersRes.data.results || bannersRes.data
    categories.value       = catsRes.data.results   || catsRes.data
    featuredProducts.value = prodsRes.data.results  || prodsRes.data
  } catch (err) {
    console.error(err)
  } finally {
    categoriesLoading.value = false
    productsLoading.value   = false
  }
})

function openAuthModal() {
  window.dispatchEvent(new CustomEvent('auth:open-modal'))
}

// Helper to safely get category data
function getCategoryData(nameSubstring) {
  return categories.value.find(c => c.name.toLowerCase().includes(nameSubstring.toLowerCase())) || {}
}

function scrollToContact() {
  document.getElementById('contact')?.scrollIntoView({ behavior: 'smooth' })
}

async function submitContact() {
  // Placeholder — real API integration when ready
  alertStore.success("Xabaringiz yuborildi! Tez orada bog'lanamiz.")
  contactForm.value = { name: '', phone: '', message: '' }
}
</script>

<style scoped>
.scrollbar-hide::-webkit-scrollbar { display: none; }
.scrollbar-hide { -ms-overflow-style: none; scrollbar-width: none; }
</style>
