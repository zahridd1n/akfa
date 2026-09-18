<template>
  <div class="min-h-screen bg-slate-950 flex flex-col justify-center items-center px-4 py-12 relative overflow-hidden">
    <!-- Subtle background glowing accents -->
    <div class="absolute -top-40 -left-40 w-96 h-96 bg-brand-600/15 rounded-full blur-3xl pointer-events-none" />
    <div class="absolute -bottom-40 -right-40 w-96 h-96 bg-blue-600/15 rounded-full blur-3xl pointer-events-none" />

    <div class="w-full max-w-md relative z-10">

      <!-- Logo & Brand Header -->
      <div class="text-center mb-8">
        <div class="inline-flex items-center justify-center w-14 h-14 bg-gradient-to-br from-brand-500 to-brand-700 rounded-2xl shadow-glow mb-4">
          <ShieldCheck class="w-8 h-8 text-white" />
        </div>
        <h1 class="text-2xl sm:text-3xl font-extrabold text-white tracking-tight">Saramax Admin</h1>
        <p class="text-slate-400 text-sm mt-1.5">Boshqaruv paneliga kirish</p>
      </div>

      <!-- Login Card -->
      <div class="bg-slate-900 border border-slate-800 rounded-3xl p-6 sm:p-8 shadow-2xl backdrop-blur-xl">

        <!-- Error Alert -->
        <div v-if="errorMessage" class="mb-5 p-3.5 bg-red-950/60 border border-red-800/80 rounded-2xl flex items-center gap-3 text-red-200 text-xs sm:text-sm">
          <AlertCircle class="w-5 h-5 text-red-400 flex-shrink-0" />
          <span>{{ errorMessage }}</span>
        </div>

        <form @submit.prevent="handleAdminLogin" class="space-y-4">
          <!-- Phone / Login -->
          <div>
            <label class="block text-xs font-semibold text-slate-300 uppercase tracking-wider mb-2">
              Telefon raqam *
            </label>
            <div class="relative">
              <input
                v-model="phone"
                type="tel"
                required
                placeholder="+998 90 123 45 67"
                class="w-full pl-10 pr-4 py-3 bg-slate-950 border border-slate-800 rounded-xl text-white placeholder-slate-500 text-sm focus:outline-none focus:ring-2 focus:ring-brand-500 focus:border-brand-500 transition-all"
              />
              <Phone class="w-4 h-4 text-slate-500 absolute left-3.5 top-1/2 -translate-y-1/2 pointer-events-none" />
            </div>
          </div>

          <!-- Password -->
          <div>
            <div class="flex items-center justify-between mb-2">
              <label class="block text-xs font-semibold text-slate-300 uppercase tracking-wider">
                Maxfiy parol *
              </label>
            </div>
            <div class="relative">
              <input
                v-model="password"
                :type="showPassword ? 'text' : 'password'"
                required
                placeholder="Parolingizni kiriting"
                class="w-full pl-10 pr-10 py-3 bg-slate-950 border border-slate-800 rounded-xl text-white placeholder-slate-500 text-sm focus:outline-none focus:ring-2 focus:ring-brand-500 focus:border-brand-500 transition-all"
              />
              <Lock class="w-4 h-4 text-slate-500 absolute left-3.5 top-1/2 -translate-y-1/2 pointer-events-none" />
              <button
                type="button"
                @click="showPassword = !showPassword"
                class="absolute right-3.5 top-1/2 -translate-y-1/2 text-slate-500 hover:text-slate-300 transition-colors"
                tabindex="-1"
              >
                <EyeOff v-if="showPassword" class="w-4 h-4" />
                <Eye v-else class="w-4 h-4" />
              </button>
            </div>
          </div>

          <!-- Submit Button -->
          <button
            type="submit"
            :disabled="loading"
            class="w-full mt-2 py-3.5 bg-gradient-to-r from-brand-600 to-brand-700 hover:from-brand-500 hover:to-brand-600 text-white font-bold rounded-xl text-sm transition-all shadow-lg shadow-brand-900/40 disabled:opacity-60 disabled:cursor-not-allowed flex items-center justify-center gap-2"
          >
            <div v-if="loading" class="w-4 h-4 border-2 border-white border-t-transparent rounded-full animate-spin" />
            <span v-else>Dashboardga kirish</span>
          </button>
        </form>

        <!-- Security Note -->
        <div class="mt-6 pt-5 border-t border-slate-800/80 flex items-center justify-center gap-2 text-slate-500 text-xs">
          <Lock class="w-3.5 h-3.5" />
          <span>Faqat vakolatli administratorlar uchun</span>
        </div>

      </div>

      <!-- Back to site link -->
      <div class="text-center mt-6">
        <router-link to="/" class="inline-flex items-center gap-1.5 text-xs text-slate-400 hover:text-white transition-colors">
          <ArrowLeft class="w-3.5 h-3.5" />
          <span>Asosiy saytga qaytish</span>
        </router-link>
      </div>

    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import { ShieldCheck, Phone, Lock, Eye, EyeOff, AlertCircle, ArrowLeft } from '@lucide/vue'
import { useAuthStore } from '@/stores/auth'
import { useAlertStore } from '@/stores/alert'

const router = useRouter()
const route = useRoute()
const authStore = useAuthStore()
const alertStore = useAlertStore()

const phone = ref('')
const password = ref('')
const showPassword = ref(false)
const loading = ref(false)
const errorMessage = ref('')

async function handleAdminLogin() {
  errorMessage.value = ''
  if (!phone.value.trim() || !password.value) {
    errorMessage.value = "Telefon raqam va parolni to'liq kiriting"
    return
  }

  loading.value = true
  try {
    const res = await authStore.login(phone.value.trim(), password.value)
    if (!res.success) {
      errorMessage.value = res.error || "Telefon raqam yoki parol noto'g'ri"
      loading.value = false
      return
    }

    // Verify admin role
    if (!authStore.isAdmin) {
      await authStore.logout()
      errorMessage.value = "Kechirasiz, ushbu hisob Administrator huquqiga ega emas!"
      loading.value = false
      return
    }

    alertStore.success('Xush kelibsiz, Administrator!')
    const redirectPath = route.query.redirect || '/admin/dashboard'
    router.push(redirectPath)
  } catch (err) {
    errorMessage.value = "Tizimga kirishda xatolik yuz berdi"
  } finally {
    loading.value = false
  }
}
</script>
