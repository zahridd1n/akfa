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
      error.value = err.response?.data?.detail || 'Login xatolik'
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
      error.value = err.response?.data || 'Ro\'yxatdan o\'tishda xatolik'
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
