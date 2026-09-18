<template>
  <Teleport to="body">
    <Transition name="modal">
      <div v-if="open" class="overlay" @click.self="$emit('close')" id="auth-modal-overlay">
        <div class="bg-white rounded-3xl shadow-2xl w-full max-w-md p-8 relative animate-slide-up" @click.stop>

          <!-- Close -->
          <button @click="$emit('close')" class="absolute top-5 right-5 btn-ghost btn-sm rounded-xl p-2">
            <X class="w-5 h-5" />
          </button>

          <!-- Logo -->
          <div class="text-center mb-8">
            <div class="w-14 h-14 bg-gradient-to-br from-brand-500 to-brand-700 rounded-2xl flex items-center justify-center shadow-glow mx-auto mb-4">
              <span class="text-white font-bold text-2xl">S</span>
            </div>
            <h2 class="text-2xl font-bold text-slate-900">
              {{ mode === 'login' ? 'Kirish' : 'Ro\'yxatdan o\'tish' }}
            </h2>
            <p class="text-slate-500 text-sm mt-1">
              {{ mode === 'login' ? 'Akkauntingizga kiring' : 'Yangi akkaunt yarating' }}
            </p>
          </div>

          <!-- Login Form -->
          <form v-if="mode === 'login'" @submit.prevent="handleLogin" class="space-y-4">
            <div>
              <label class="form-label">Telefon raqam</label>
              <input
                v-model="loginForm.phone"
                type="tel"
                placeholder="+998901234567"
                class="form-input"
                :class="{ 'form-input-error': errors.phone }"
                id="login-phone"
                required
              />
              <p v-if="errors.phone" class="form-error">{{ errors.phone }}</p>
            </div>
            <div>
              <label class="form-label">Parol</label>
              <div class="relative">
                <input
                  v-model="loginForm.password"
                  :type="showPassword ? 'text' : 'password'"
                  placeholder="Parolingizni kiriting"
                  class="form-input pr-12"
                  id="login-password"
                  required
                />
                <button type="button" @click="showPassword = !showPassword" class="absolute right-3 top-1/2 -translate-y-1/2 text-slate-400 hover:text-slate-600">
                  <Eye v-if="!showPassword" class="w-4.5 h-4.5" />
                  <EyeOff v-else class="w-4.5 h-4.5" />
                </button>
              </div>
              <p v-if="errors.password" class="form-error">{{ errors.password }}</p>
            </div>

            <p v-if="errors.general" class="text-sm text-red-600 bg-red-50 rounded-xl px-4 py-3 flex items-center gap-2">
              <AlertCircle class="w-4 h-4 flex-shrink-0" /> {{ errors.general }}
            </p>

            <button type="submit" class="btn-xl btn-primary w-full mt-2" :disabled="authStore.loading" id="login-submit-btn">
              <span v-if="!authStore.loading">Kirish</span>
              <div v-else class="spinner" />
            </button>
          </form>

          <!-- Register Form -->
          <form v-else @submit.prevent="handleRegister" class="space-y-4">
            <div>
              <label class="form-label">Ism va Familiya</label>
              <input
                v-model="registerForm.full_name"
                type="text"
                placeholder="Ism Familiyangiz"
                class="form-input"
                :class="{ 'form-input-error': errors.full_name }"
                id="register-name"
                required
              />
              <p v-if="errors.full_name" class="form-error">
                {{ Array.isArray(errors.full_name) ? errors.full_name[0] : errors.full_name }}
              </p>
            </div>
            <div>
              <label class="form-label">Telefon raqam</label>
              <input
                v-model="registerForm.phone_number"
                type="tel"
                placeholder="+998 90 123 45 67"
                class="form-input"
                :class="{ 'form-input-error': errors.phone_number }"
                id="register-phone"
                required
              />
              <p v-if="errors.phone_number" class="form-error">
                {{ Array.isArray(errors.phone_number) ? errors.phone_number[0] : errors.phone_number }}
              </p>
            </div>
            <div>
              <label class="form-label">Parol</label>
              <div class="relative">
                <input
                  v-model="registerForm.password"
                  :type="showPassword ? 'text' : 'password'"
                  placeholder="Kamida 6 ta belgi"
                  class="form-input pr-12"
                  id="register-password"
                  required
                />
                <button type="button" @click="showPassword = !showPassword" class="absolute right-3 top-1/2 -translate-y-1/2 text-slate-400 hover:text-slate-600">
                  <Eye v-if="!showPassword" class="w-4.5 h-4.5" />
                  <EyeOff v-else class="w-4.5 h-4.5" />
                </button>
              </div>
              <p v-if="errors.password" class="form-error">
                {{ Array.isArray(errors.password) ? errors.password[0] : errors.password }}
              </p>
            </div>

            <p v-if="errors.general" class="text-sm text-red-600 bg-red-50 rounded-xl px-4 py-3 flex items-center gap-2">
              <AlertCircle class="w-4 h-4 flex-shrink-0" /> {{ errors.general }}
            </p>

            <button type="submit" class="btn-xl btn-primary w-full mt-2" :disabled="authStore.loading" id="register-submit-btn">
              <span v-if="!authStore.loading">Ro'yxatdan o'tish</span>
              <div v-else class="spinner" />
            </button>
          </form>

          <!-- Mode Toggle -->
          <p class="text-center text-sm text-slate-500 mt-6">
            <template v-if="mode === 'login'">
              Akkauntingiz yo'qmi?
              <button @click="switchMode" class="text-brand-600 font-semibold hover:underline ml-1">
                Ro'yxatdan o'ting
              </button>
            </template>
            <template v-else>
              Akkauntingiz bormi?
              <button @click="switchMode" class="text-brand-600 font-semibold hover:underline ml-1">
                Kirish
              </button>
            </template>
          </p>
        </div>
      </div>
    </Transition>
  </Teleport>
</template>

<script setup>
import { ref, watch } from 'vue'
import { X, Eye, EyeOff, AlertCircle } from '@lucide/vue'
import { useAuthStore } from '@/stores/auth'
import { useCartStore } from '@/stores/cart'
import { useAlertStore } from '@/stores/alert'

const props = defineProps({ open: Boolean })
const emit = defineEmits(['close', 'success'])

const authStore  = useAuthStore()
const cartStore  = useCartStore()
const alertStore = useAlertStore()

const mode = ref('login')
const showPassword = ref(false)
const errors = ref({})

const loginForm = ref({ phone: '', password: '' })
const registerForm = ref({ full_name: '', phone_number: '', password: '' })

watch(() => props.open, (val) => {
  if (val) {
    mode.value = 'login'
    errors.value = {}
    loginForm.value = { phone: '', password: '' }
    registerForm.value = { full_name: '', phone_number: '', password: '' }
    showPassword.value = false
  }
})

function switchMode() {
  mode.value = mode.value === 'login' ? 'register' : 'login'
  errors.value = {}
}

async function handleLogin() {
  errors.value = {}
  const result = await authStore.login(loginForm.value.phone.trim(), loginForm.value.password)
  if (result.success) {
    await cartStore.fetchCart()
    alertStore.success(`Xush kelibsiz, ${authStore.fullName}!`)
    emit('success')
  } else {
    errors.value.general = result.error || 'Telefon raqam yoki parol noto\'g\'ri'
  }
}

async function handleRegister() {
  errors.value = {}
  const payload = {
    full_name: registerForm.value.full_name.trim(),
    phone_number: registerForm.value.phone_number.trim(),
    password: registerForm.value.password,
  }
  const result = await authStore.register(payload)
  if (result.success) {
    await cartStore.fetchCart()
    alertStore.success('Muvaffaqiyatli ro\'yxatdan o\'tdingiz!')
    emit('success')
  } else {
    if (typeof result.error === 'object' && result.error !== null) {
      errors.value = { ...result.error }
      const knownKeys = ['full_name', 'phone_number', 'password']
      const unhandled = Object.entries(result.error)
        .filter(([k]) => !knownKeys.includes(k))
        .map(([k, v]) => Array.isArray(v) ? v.join(', ') : v)
      if (unhandled.length > 0) {
        errors.value.general = unhandled.join('. ')
      }
    } else {
      errors.value.general = result.error || 'Xatolik yuz berdi'
    }
  }
}
</script>
