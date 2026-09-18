import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import { authApi } from '@/api/auth'

export const useAuthStore = defineStore('auth', () => {
  const token = ref(localStorage.getItem('token') || null)
  const user = ref(JSON.parse(localStorage.getItem('user') || 'null'))
  const loading = ref(false)
  const error = ref(null)

  const isLoggedIn = computed(() => !!token.value)
  const isAdmin = computed(() => user.value?.role === 'admin')
  const fullName = computed(() => user.value?.full_name || 'Foydalanuvchi')

  async function login(phone, password) {
    loading.value = true
    error.value = null
    try {
      const res = await authApi.login({ phone_number: phone, password })
      token.value = res.data.token
      user.value = res.data.user
      localStorage.setItem('token', res.data.token)
      localStorage.setItem('user', JSON.stringify(res.data.user))
      return { success: true }
    } catch (err) {
      const errData = err.response?.data
      if (typeof errData === 'string') {
        error.value = errData
      } else if (errData?.detail) {
        error.value = errData.detail
      } else if (errData?.non_field_errors) {
        error.value = Array.isArray(errData.non_field_errors) ? errData.non_field_errors[0] : errData.non_field_errors
      } else if (errData?.phone_number) {
        error.value = Array.isArray(errData.phone_number) ? errData.phone_number[0] : errData.phone_number
      } else if (errData?.password) {
        error.value = Array.isArray(errData.password) ? errData.password[0] : errData.password
      } else if (typeof errData === 'object' && errData !== null) {
        const firstVal = Object.values(errData)[0]
        error.value = Array.isArray(firstVal) ? firstVal[0] : (typeof firstVal === 'string' ? firstVal : 'Login xatolik')
      } else {
        error.value = 'Telefon raqam yoki parol noto\'g\'ri'
      }
      return { success: false, error: error.value }
    } finally {
      loading.value = false
    }
  }

  async function register(data) {
    loading.value = true
    error.value = null
    try {
      const res = await authApi.register(data)
      token.value = res.data.token
      user.value = res.data.user
      localStorage.setItem('token', res.data.token)
      localStorage.setItem('user', JSON.stringify(res.data.user))
      return { success: true }
    } catch (err) {
      const errData = err.response?.data
      error.value = errData || 'Ro\'yxatdan o\'tishda xatolik'
      return { success: false, error: error.value }
    } finally {
      loading.value = false
    }
  }

  async function logout() {
    try {
      await authApi.logout()
    } catch {}
    token.value = null
    user.value = null
    localStorage.removeItem('token')
    localStorage.removeItem('user')
  }

  async function fetchProfile() {
    if (!token.value) return
    try {
      const res = await authApi.getProfile()
      user.value = res.data
      localStorage.setItem('user', JSON.stringify(res.data))
    } catch {}
  }

  async function updateProfile(data) {
    loading.value = true
    try {
      const res = await authApi.updateProfile(data)
      user.value = { ...user.value, ...res.data }
      localStorage.setItem('user', JSON.stringify(user.value))
      return { success: true }
    } catch (err) {
      return { success: false, error: err.response?.data }
    } finally {
      loading.value = false
    }
  }

  // Listen for 401 from interceptor
  window.addEventListener('auth:logout', () => {
    token.value = null
    user.value = null
  })

  return {
    token, user, loading, error,
    isLoggedIn, isAdmin, fullName,
    login, register, logout, fetchProfile, updateProfile,
  }
})
