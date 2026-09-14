import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import { cartApi } from '@/api/cart'
import { useAuthStore } from './auth'

export const useCartStore = defineStore('cart', () => {
  const cart = ref(null)
  const loading = ref(false)

  const items = computed(() => cart.value?.items || [])
  const itemCount = computed(() => items.value.reduce((sum, i) => sum + i.quantity, 0))
  const subtotal = computed(() => cart.value?.total_amount || 0)

  async function fetchCart() {
    const auth = useAuthStore()
    if (!auth.isLoggedIn) return
    loading.value = true
    try {
      const res = await cartApi.getCart()
      cart.value = res.data
    } catch {} finally {
      loading.value = false
    }
  }

  async function addItem(data) {
    loading.value = true
    try {
      await cartApi.addItem(data)
      await fetchCart()
      return { success: true }
    } catch (err) {
      return { success: false, error: err.response?.data }
    } finally {
      loading.value = false
    }
  }

  async function updateItem(id, data) {
    try {
      await cartApi.updateItem(id, data)
      await fetchCart()
      return { success: true }
    } catch (err) {
      return { success: false, error: err.response?.data }
    }
  }

  async function removeItem(id) {
    try {
      await cartApi.removeItem(id)
      await fetchCart()
    } catch {}
  }

  async function clearCart() {
    try {
      await cartApi.clearCart()
      cart.value = null
    } catch {}
  }

  function resetCart() {
    cart.value = null
  }

  return {
    cart, loading,
    items, itemCount, subtotal,
    fetchCart, addItem, updateItem, removeItem, clearCart, resetCart,
  }
})
