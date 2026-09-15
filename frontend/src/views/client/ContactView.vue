<template>
  <div class="min-h-screen" style="background: #EBF3F8;">

    <!-- Header -->
    <div class="bg-white/80 backdrop-blur border-b border-[#C7DDEA]/60 px-4 pt-5 pb-4">
      <div class="max-w-4xl mx-auto">
        <div class="flex items-center gap-2 text-sm text-slate-400 mb-2">
          <router-link to="/" class="hover:text-brand-600">Bosh sahifa</router-link>
          <span>/</span>
          <span class="text-slate-700 font-medium">Aloqa</span>
        </div>
        <h1 class="text-2xl md:text-3xl font-bold text-slate-900">Biz bilan bog'laning</h1>
        <p class="text-slate-500 text-sm mt-1">Har qanday savol va takliflaringizga tayyor javob beramiz</p>
      </div>
    </div>

    <div class="max-w-4xl mx-auto px-4 py-6 md:py-10">
      <div class="md:grid md:grid-cols-5 md:gap-8 space-y-5 md:space-y-0">

        <!-- LEFT: Info Cards -->
        <div class="md:col-span-2 space-y-4">

          <!-- Loading -->
          <div v-if="loading" class="space-y-3">
            <div v-for="i in 4" :key="i" class="skeleton h-16 rounded-xl" />
          </div>

          <template v-else>
            <!-- Phone -->
            <div v-if="settings.phone_main" class="bg-white rounded-2xl border border-[#C7DDEA]/50 p-4 flex items-center gap-4 shadow-sm">
              <div class="w-10 h-10 bg-brand-50 rounded-xl flex items-center justify-center flex-shrink-0">
                <Phone class="w-5 h-5 text-brand-700" />
              </div>
              <div>
                <p class="text-xs text-slate-400 font-medium mb-0.5">Telefon</p>
                <a :href="`tel:${settings.phone_main}`" class="text-sm font-bold text-slate-900 hover:text-brand-600">{{ settings.phone_main }}</a>
                <div v-if="settings.phone_extra">
                  <a :href="`tel:${settings.phone_extra}`" class="text-xs text-slate-500 hover:text-brand-500">{{ settings.phone_extra }}</a>
                </div>
              </div>
            </div>

            <!-- WhatsApp -->
            <div v-if="settings.phone_whatsapp" class="bg-white rounded-2xl border border-[#C7DDEA]/50 p-4 flex items-center gap-4 shadow-sm">
              <div class="w-10 h-10 bg-emerald-50 rounded-xl flex items-center justify-center flex-shrink-0">
                <MessageCircle class="w-5 h-5 text-emerald-600" />
              </div>
              <div>
                <p class="text-xs text-slate-400 font-medium mb-0.5">WhatsApp</p>
                <a :href="`https://wa.me/${settings.phone_whatsapp.replace(/\D/g,'')}`" target="_blank" class="text-sm font-bold text-slate-900 hover:text-emerald-600">{{ settings.phone_whatsapp }}</a>
              </div>
            </div>

            <!-- Email -->
            <div v-if="settings.email" class="bg-white rounded-2xl border border-[#C7DDEA]/50 p-4 flex items-center gap-4 shadow-sm">
              <div class="w-10 h-10 bg-blue-50 rounded-xl flex items-center justify-center flex-shrink-0">
                <Mail class="w-5 h-5 text-blue-600" />
              </div>
              <div>
                <p class="text-xs text-slate-400 font-medium mb-0.5">Email</p>
                <a :href="`mailto:${settings.email}`" class="text-sm font-bold text-slate-900 hover:text-blue-600">{{ settings.email }}</a>
              </div>
            </div>

            <!-- Address -->
            <div v-if="settings.address" class="bg-white rounded-2xl border border-[#C7DDEA]/50 p-4 flex items-start gap-4 shadow-sm">
              <div class="w-10 h-10 bg-amber-50 rounded-xl flex items-center justify-center flex-shrink-0 mt-0.5">
                <MapPin class="w-5 h-5 text-amber-600" />
              </div>
              <div>
                <p class="text-xs text-slate-400 font-medium mb-0.5">Manzil</p>
                <p class="text-sm font-semibold text-slate-900 leading-relaxed">{{ settings.address }}</p>
              </div>
            </div>

            <!-- Work Hours -->
            <div v-if="settings.work_hours" class="bg-white rounded-2xl border border-[#C7DDEA]/50 p-4 flex items-center gap-4 shadow-sm">
              <div class="w-10 h-10 bg-purple-50 rounded-xl flex items-center justify-center flex-shrink-0">
                <Clock class="w-5 h-5 text-purple-600" />
              </div>
              <div>
                <p class="text-xs text-slate-400 font-medium mb-0.5">Ish vaqti</p>
                <p class="text-sm font-bold text-slate-900">{{ settings.work_hours }}</p>
              </div>
            </div>

            <!-- Social Links -->
            <div v-if="settings.telegram_url || settings.instagram_url || settings.facebook_url || settings.youtube_url"
                 class="bg-white rounded-2xl border border-[#C7DDEA]/50 p-4 shadow-sm">
              <p class="text-xs text-slate-400 font-medium mb-3">Ijtimoiy tarmoqlar</p>
              <div class="flex items-center gap-3">
                <a v-if="settings.telegram_url" :href="settings.telegram_url" target="_blank"
                   class="w-10 h-10 rounded-xl bg-[#EBF3F8] hover:bg-blue-100 flex items-center justify-center transition-colors group">
                  <!-- Telegram icon -->
                  <svg class="w-5 h-5 text-blue-500" viewBox="0 0 24 24" fill="currentColor"><path d="M11.944 0A12 12 0 0 0 0 12a12 12 0 0 0 12 12 12 12 0 0 0 12-12A12 12 0 0 0 12 0a12 12 0 0 0-.056 0zm4.962 7.224c.1-.002.321.023.465.14a.506.506 0 0 1 .171.325c.016.093.036.306.02.472-.18 1.898-.962 6.502-1.36 8.627-.168.9-.499 1.201-.82 1.23-.696.065-1.225-.46-1.9-.902-1.056-.693-1.653-1.124-2.678-1.8-1.185-.78-.417-1.21.258-1.91.177-.184 3.247-2.977 3.307-3.23.007-.032.014-.15-.056-.212s-.174-.041-.249-.024c-.106.024-1.793 1.14-5.061 3.345-.48.33-.913.49-1.302.48-.428-.008-1.252-.241-1.865-.44-.752-.245-1.349-.374-1.297-.789.027-.216.325-.437.893-.663 3.498-1.524 5.83-2.529 6.998-3.014 3.332-1.386 4.025-1.627 4.476-1.635z"/></svg>
                </a>
                <a v-if="settings.instagram_url" :href="settings.instagram_url" target="_blank"
                   class="w-10 h-10 rounded-xl bg-[#EBF3F8] hover:bg-pink-50 flex items-center justify-center transition-colors">
                  <svg class="w-5 h-5 text-pink-500" viewBox="0 0 24 24" fill="currentColor"><path d="M12 2.163c3.204 0 3.584.012 4.85.07 3.252.148 4.771 1.691 4.919 4.919.058 1.265.069 1.645.069 4.849 0 3.205-.012 3.584-.069 4.849-.149 3.225-1.664 4.771-4.919 4.919-1.266.058-1.644.07-4.85.07-3.204 0-3.584-.012-4.849-.07-3.26-.149-4.771-1.699-4.919-4.92-.058-1.265-.07-1.644-.07-4.849 0-3.204.013-3.583.07-4.849.149-3.227 1.664-4.771 4.919-4.919 1.266-.057 1.645-.069 4.849-.069zm0-2.163c-3.259 0-3.667.014-4.947.072-4.358.2-6.78 2.618-6.98 6.98-.059 1.281-.073 1.689-.073 4.948 0 3.259.014 3.668.072 4.948.2 4.358 2.618 6.78 6.98 6.98 1.281.058 1.689.072 4.948.072 3.259 0 3.668-.014 4.948-.072 4.354-.2 6.782-2.618 6.979-6.98.059-1.28.073-1.689.073-4.948 0-3.259-.014-3.667-.072-4.947-.196-4.354-2.617-6.78-6.979-6.98-1.281-.059-1.69-.073-4.949-.073zm0 5.838c-3.403 0-6.162 2.759-6.162 6.162s2.759 6.163 6.162 6.163 6.162-2.759 6.162-6.163c0-3.403-2.759-6.162-6.162-6.162zm0 10.162c-2.209 0-4-1.79-4-4 0-2.209 1.791-4 4-4s4 1.791 4 4c0 2.21-1.791 4-4 4zm6.406-11.845c-.796 0-1.441.645-1.441 1.44s.645 1.44 1.441 1.44c.795 0 1.439-.645 1.439-1.44s-.644-1.44-1.439-1.44z"/></svg>
                </a>
                <a v-if="settings.facebook_url" :href="settings.facebook_url" target="_blank"
                   class="w-10 h-10 rounded-xl bg-[#EBF3F8] hover:bg-blue-50 flex items-center justify-center transition-colors">
                  <svg class="w-5 h-5 text-blue-700" viewBox="0 0 24 24" fill="currentColor"><path d="M24 12.073c0-6.627-5.373-12-12-12s-12 5.373-12 12c0 5.99 4.388 10.954 10.125 11.854v-8.385H7.078v-3.47h3.047V9.43c0-3.007 1.792-4.669 4.533-4.669 1.312 0 2.686.235 2.686.235v2.953H15.83c-1.491 0-1.956.925-1.956 1.874v2.25h3.328l-.532 3.47h-2.796v8.385C19.612 23.027 24 18.062 24 12.073z"/></svg>
                </a>
                <a v-if="settings.youtube_url" :href="settings.youtube_url" target="_blank"
                   class="w-10 h-10 rounded-xl bg-[#EBF3F8] hover:bg-red-50 flex items-center justify-center transition-colors">
                  <svg class="w-5 h-5 text-red-600" viewBox="0 0 24 24" fill="currentColor"><path d="M23.498 6.186a3.016 3.016 0 0 0-2.122-2.136C19.505 3.545 12 3.545 12 3.545s-7.505 0-9.377.505A3.017 3.017 0 0 0 .502 6.186C0 8.07 0 12 0 12s0 3.93.502 5.814a3.016 3.016 0 0 0 2.122 2.136c1.871.505 9.376.505 9.376.505s7.505 0 9.377-.505a3.015 3.015 0 0 0 2.122-2.136C24 15.93 24 12 24 12s0-3.93-.502-5.814zM9.545 15.568V8.432L15.818 12l-6.273 3.568z"/></svg>
                </a>
              </div>
            </div>

          </template>
        </div>

        <!-- RIGHT: Contact Form -->
        <div class="md:col-span-3">
          <div class="bg-white rounded-2xl border border-[#C7DDEA]/50 p-5 md:p-8 shadow-sm">
            <h2 class="text-xl font-bold text-slate-900 mb-1">Murojat yuborish</h2>
            <p class="text-sm text-slate-400 mb-6">Xabaringizni qoldiring — tez orada bog'lanamiz</p>

            <form @submit.prevent="submitForm" class="space-y-4">
              <div>
                <label class="form-label">Ismingiz *</label>
                <input v-model="form.name" type="text" class="form-input" placeholder="Ism Familiya" required />
              </div>
              <div>
                <label class="form-label">Telefon raqam *</label>
                <input v-model="form.phone" type="tel" class="form-input" placeholder="+998 90 123 45 67" required />
              </div>
              <div>
                <label class="form-label">Xabaringiz</label>
                <textarea v-model="form.message" rows="5" class="form-input resize-none"
                  placeholder="Savol, taklif yoki muammoingizni yozing..."></textarea>
              </div>

              <!-- Success state -->
              <div v-if="submitted" class="flex items-center gap-3 p-4 bg-emerald-50 border border-emerald-200 rounded-xl">
                <CheckCircle class="w-5 h-5 text-emerald-500 flex-shrink-0" />
                <div>
                  <p class="text-sm font-semibold text-emerald-700">Xabaringiz yuborildi!</p>
                  <p class="text-xs text-emerald-600">Tez orada siz bilan bog'lanamiz.</p>
                </div>
              </div>

              <button
                v-else
                type="submit"
                :disabled="submitting"
                class="w-full py-3.5 bg-brand-950 hover:bg-brand-900 text-white rounded-xl font-semibold text-sm transition-colors disabled:opacity-60"
              >
                <span v-if="!submitting">Yuborish</span>
                <div v-else class="spinner mx-auto" />
              </button>
            </form>
          </div>
        </div>

      </div>

      <!-- Full-width Map Section -->
      <div class="mt-6 md:mt-8 bg-white rounded-2xl border border-[#C7DDEA]/50 overflow-hidden shadow-sm">
        <!-- Map header with directions button -->
        <div class="flex items-center justify-between px-4 py-3 border-b border-[#C7DDEA]/40">
          <div class="flex items-center gap-2">
            <MapPin class="w-4 h-4 text-brand-600" />
            <span class="text-sm font-semibold text-slate-800">{{ settings.address || "Manzilimiz" }}</span>
          </div>
          <a
            :href="directionsUrl"
            target="_blank"
            rel="noopener noreferrer"
            class="flex items-center gap-1.5 px-3 py-1.5 bg-brand-950 hover:bg-brand-900 text-white text-xs font-semibold rounded-lg transition-colors"
          >
            <Navigation class="w-3.5 h-3.5" />
            Marshrut olish
          </a>
        </div>
        <!-- Map iframe — full width, taller on desktop -->
        <iframe
          :src="mapEmbedUrl"
          width="100%"
          class="w-full h-56 md:h-[420px] block"
          style="border:0;"
          allowfullscreen=""
          loading="lazy"
        ></iframe>
      </div>

    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { Phone, MessageCircle, Mail, MapPin, Clock, CheckCircle, Navigation } from '@lucide/vue'
import { siteApi } from '@/api/site'
import { useAlertStore } from '@/stores/alert'

const alertStore = useAlertStore()
const settings   = ref({})
const loading    = ref(true)
const submitting = ref(false)
const submitted  = ref(false)

const form = ref({ name: '', phone: '', message: '' })

// Map computed — use address from settings or fallback
const MAP_FALLBACK = "O'zbekiston"
const mapEmbedUrl = computed(() => {
  const query = settings.value.map_location || settings.value.address || MAP_FALLBACK
  return `https://maps.google.com/maps?q=${encodeURIComponent(query)}&t=&z=13&ie=UTF8&iwloc=&output=embed`
})

const directionsUrl = computed(() => {
  const query = settings.value.map_location || settings.value.address || MAP_FALLBACK
  return `https://www.google.com/maps/dir/?api=1&destination=${encodeURIComponent(query)}`
})

onMounted(async () => {
  try {
    const res = await siteApi.getSettings()
    settings.value = res.data
  } catch {}
  loading.value = false
})

async function submitForm() {
  submitting.value = true
  try {
    await siteApi.submitContact(form.value)
    submitted.value = true
    form.value = { name: '', phone: '', message: '' }
    alertStore.success("Murojatingiz yuborildi!")
    setTimeout(() => { submitted.value = false }, 5000)
  } catch (err) {
    alertStore.error(err.response?.data?.detail || "Xatolik yuz berdi, qayta urinib ko'ring")
  }
  submitting.value = false
}
</script>
