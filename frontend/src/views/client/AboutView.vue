<template>
  <div class="min-h-screen" style="background: #EBF3F8;">

    <!-- Breadcrumb & Header -->
    <div class="bg-white/80 backdrop-blur border-b border-[#C7DDEA]/60 px-4 pt-5 pb-4">
      <div class="max-w-5xl mx-auto">
        <div class="flex items-center gap-2 text-sm text-slate-400 mb-2">
          <router-link to="/" class="hover:text-brand-600">Bosh sahifa</router-link>
          <span>/</span>
          <span class="text-slate-700 font-medium">Biz haqimizda</span>
        </div>
        <h1 class="text-2xl md:text-3xl font-bold text-slate-900">
          {{ about.title || "Biz haqimizda" }}
        </h1>
        <p v-if="about.subtitle" class="text-slate-500 text-sm mt-1">
          {{ about.subtitle }}
        </p>
      </div>
    </div>

    <!-- Main Container -->
    <div class="max-w-5xl mx-auto px-4 py-6 md:py-10 space-y-8">

      <!-- Loading skeleton -->
      <div v-if="loading" class="space-y-6">
        <div class="skeleton h-80 rounded-3xl" />
        <div class="grid grid-cols-2 md:grid-cols-4 gap-4">
          <div v-for="i in 4" :key="i" class="skeleton h-24 rounded-2xl" />
        </div>
      </div>

      <template v-else>
        <!-- Top Hero Card: Image + Content in Bento Layout -->
        <div class="bg-white rounded-3xl border border-[#C7DDEA]/50 overflow-hidden shadow-sm">
          <div class="grid grid-cols-1 lg:grid-cols-12 gap-0 items-stretch">
            
            <!-- Left: Text content -->
            <div class="lg:col-span-7 p-6 sm:p-8 md:p-10 flex flex-col justify-center space-y-4">
              <div class="inline-flex items-center gap-2 px-3 py-1.5 rounded-full bg-brand-50 border border-brand-200/60 text-brand-800 text-xs font-semibold w-fit">
                <Building2 class="w-3.5 h-3.5 text-brand-600" />
                <span>Kompaniya haqida</span>
              </div>

              <h2 class="text-xl sm:text-2xl md:text-3xl font-extrabold text-slate-900 leading-snug">
                {{ about.title || "Saramax haqida" }}
              </h2>

              <div class="text-slate-600 text-sm sm:text-base leading-relaxed whitespace-pre-line space-y-3">
                <p>{{ about.content }}</p>
              </div>

              <!-- Mission quote / highlight -->
              <div v-if="about.mission" class="mt-4 p-4 rounded-2xl bg-[#EBF3F8]/60 border-l-4 border-brand-600">
                <p class="text-xs font-semibold uppercase tracking-wider text-brand-700 mb-1">Bizning maqsad va missiyamiz</p>
                <p class="text-xs sm:text-sm text-slate-700 leading-relaxed italic">
                  "{{ about.mission }}"
                </p>
              </div>
            </div>

            <!-- Right: Image with Badge -->
            <div class="lg:col-span-5 relative bg-gradient-to-br from-slate-100 to-slate-200 min-h-[280px] lg:min-h-[420px] flex items-center justify-center overflow-hidden">
              <img
                v-if="about.image"
                :src="about.image"
                :alt="about.title"
                class="w-full h-full object-cover object-center absolute inset-0"
              />
              <!-- Fallback placeholder visual if no image uploaded -->
              <div v-else class="flex flex-col items-center justify-center p-8 text-center text-slate-400">
                <Building2 class="w-16 h-16 text-slate-300 mb-2" />
                <span class="text-xs font-medium text-slate-500">Saramax rasmiy do'koni</span>
              </div>

              <!-- Experience Float Badge -->
              <div
                v-if="about.experience_years"
                class="absolute bottom-4 left-4 bg-white/95 backdrop-blur-md border border-white/50 shadow-lg rounded-2xl px-4 py-3 flex items-center gap-3 z-10"
              >
                <div class="w-10 h-10 rounded-xl bg-brand-950 text-white flex items-center justify-center font-extrabold text-sm">
                  {{ about.experience_years }}
                </div>
                <div>
                  <p class="text-xs font-bold text-slate-900">Muvaffaqiyatli tajriba</p>
                  <p class="text-[11px] text-slate-500">Mijozlar ishonchi</p>
                </div>
              </div>
            </div>

          </div>
        </div>

        <!-- Dynamic Stats Grid from Database -->
        <div class="grid grid-cols-2 md:grid-cols-4 gap-3 md:gap-4">
          <div v-if="about.stat_1_number" class="bg-white rounded-2xl border border-[#C7DDEA]/50 p-4 sm:p-5 text-center shadow-sm">
            <p class="text-2xl sm:text-3xl font-extrabold text-brand-900 mb-1">{{ about.stat_1_number }}</p>
            <p class="text-xs text-slate-500 font-medium">{{ about.stat_1_label || "Mahsulotlar" }}</p>
          </div>
          <div v-if="about.stat_2_number" class="bg-white rounded-2xl border border-[#C7DDEA]/50 p-4 sm:p-5 text-center shadow-sm">
            <p class="text-2xl sm:text-3xl font-extrabold text-emerald-600 mb-1">{{ about.stat_2_number }}</p>
            <p class="text-xs text-slate-500 font-medium">{{ about.stat_2_label || "Mijozlar" }}</p>
          </div>
          <div v-if="about.stat_3_number" class="bg-white rounded-2xl border border-[#C7DDEA]/50 p-4 sm:p-5 text-center shadow-sm">
            <p class="text-2xl sm:text-3xl font-extrabold text-blue-600 mb-1">{{ about.stat_3_number }}</p>
            <p class="text-xs text-slate-500 font-medium">{{ about.stat_3_label || "Sifat kafolati" }}</p>
          </div>
          <div v-if="about.stat_4_number" class="bg-white rounded-2xl border border-[#C7DDEA]/50 p-4 sm:p-5 text-center shadow-sm">
            <p class="text-2xl sm:text-3xl font-extrabold text-purple-600 mb-1">{{ about.stat_4_number }}</p>
            <p class="text-xs text-slate-500 font-medium">{{ about.stat_4_label || "Qo'llab-quvvatlash" }}</p>
          </div>
        </div>

        <!-- Core Values / Why Us Grid -->
        <div class="bg-white rounded-3xl border border-[#C7DDEA]/50 p-6 md:p-8 shadow-sm">
          <h3 class="text-lg md:text-xl font-bold text-slate-900 mb-5">Nega aynan Saramax?</h3>

          <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
            <div class="flex items-start gap-3.5 p-4 rounded-2xl bg-[#EBF3F8]/50 border border-[#C7DDEA]/40">
              <div class="w-10 h-10 rounded-xl bg-blue-100 flex items-center justify-center flex-shrink-0">
                <ShieldCheck class="w-5 h-5 text-blue-700" />
              </div>
              <div>
                <h4 class="text-sm font-bold text-slate-900 mb-1">Kafolatlangan sifat</h4>
                <p class="text-xs text-slate-500 leading-relaxed">Faqat sinovdan o'tgan va sertifikatlangan asl mahsulotlar taqdim etiladi.</p>
              </div>
            </div>

            <div class="flex items-start gap-3.5 p-4 rounded-2xl bg-[#EBF3F8]/50 border border-[#C7DDEA]/40">
              <div class="w-10 h-10 rounded-xl bg-emerald-100 flex items-center justify-center flex-shrink-0">
                <Truck class="w-5 h-5 text-emerald-700" />
              </div>
              <div>
                <h4 class="text-sm font-bold text-slate-900 mb-1">Tezkor yetkazib berish</h4>
                <p class="text-xs text-slate-500 leading-relaxed">Buyurtmalaringizni qisqa muddat ichida ishonchli manzilga yetkazamiz.</p>
              </div>
            </div>

            <div class="flex items-start gap-3.5 p-4 rounded-2xl bg-[#EBF3F8]/50 border border-[#C7DDEA]/40">
              <div class="w-10 h-10 rounded-xl bg-amber-100 flex items-center justify-center flex-shrink-0">
                <Sparkles class="w-5 h-5 text-amber-700" />
              </div>
              <div>
                <h4 class="text-sm font-bold text-slate-900 mb-1">Qulay narxlar</h4>
                <p class="text-xs text-slate-500 leading-relaxed">To'g'ridan-to'g'ri ta'minotchilar bilan ishlash orqali hamyonbop narxlar.</p>
              </div>
            </div>

            <div class="flex items-start gap-3.5 p-4 rounded-2xl bg-[#EBF3F8]/50 border border-[#C7DDEA]/40">
              <div class="w-10 h-10 rounded-xl bg-purple-100 flex items-center justify-center flex-shrink-0">
                <Headphones class="w-5 h-5 text-purple-700" />
              </div>
              <div>
                <h4 class="text-sm font-bold text-slate-900 mb-1">Professional yordam</h4>
                <p class="text-xs text-slate-500 leading-relaxed">Mutaxassislarimiz barcha savollaringizga tez va aniq javob berishadi.</p>
              </div>
            </div>
          </div>
        </div>

        <!-- Contact / Catalog Action Card -->
        <div class="bg-gradient-to-r from-brand-950 to-slate-900 text-white rounded-3xl p-6 md:p-8 flex flex-col md:flex-row items-center justify-between gap-6 shadow-sm">
          <div>
            <h3 class="text-lg md:text-xl font-bold mb-1">Savollaringiz yoki takliflaringiz bormi?</h3>
            <p class="text-xs md:text-sm text-slate-300">Biz bilan bog'laning yoki butun katalogimizdagi mahsulotlarni ko'rib chiqing.</p>
          </div>
          <div class="flex items-center gap-3 w-full md:w-auto">
            <router-link
              to="/catalog"
              class="flex-1 md:flex-none text-center px-5 py-3 bg-white text-slate-900 rounded-xl text-xs font-bold hover:bg-slate-100 transition-colors shadow"
            >
              Katalogga o'tish
            </router-link>
            <router-link
              to="/contact"
              class="flex-1 md:flex-none text-center px-5 py-3 bg-white/10 border border-white/20 text-white rounded-xl text-xs font-bold hover:bg-white/20 transition-colors"
            >
              Aloqa sahifasi
            </router-link>
          </div>
        </div>

      </template>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { Building2, ShieldCheck, Truck, Sparkles, Headphones } from '@lucide/vue'
import { siteApi } from '@/api/site'

const about = ref({})
const loading = ref(true)

onMounted(async () => {
  try {
    const res = await siteApi.getAbout()
    about.value = res.data
  } catch (err) {
    console.error("About data fetch error:", err)
  } finally {
    loading.value = false
  }
})
</script>
