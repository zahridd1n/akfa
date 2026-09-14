<template>
  <router-view />
  <!-- Global Toast Notifications -->
  <Teleport to="body">
    <div class="fixed top-4 right-4 z-[9999] flex flex-col gap-2 pointer-events-none">
      <TransitionGroup name="toast">
        <div
          v-for="toast in alertStore.toasts"
          :key="toast.id"
          class="flex items-center gap-3 px-4 py-3.5 rounded-xl shadow-xl text-sm font-medium min-w-[280px] max-w-sm pointer-events-auto cursor-pointer select-none"
          :class="{
            'toast-success': toast.type === 'success',
            'toast-error':   toast.type === 'error',
            'toast-info':    toast.type === 'info',
            'toast-warning': toast.type === 'warning',
          }"
          @click="alertStore.remove(toast.id)"
        >
          <span class="text-lg flex-shrink-0">
            {{ toast.type === 'success' ? '✓' : toast.type === 'error' ? '✕' : toast.type === 'warning' ? '⚠' : 'ℹ' }}
          </span>
          <span class="flex-1">{{ toast.message }}</span>
        </div>
      </TransitionGroup>
    </div>
  </Teleport>
</template>

<script setup>
import { useAlertStore } from '@/stores/alert'
import { useAuthStore } from '@/stores/auth'
import { useCartStore } from '@/stores/cart'
import { onMounted } from 'vue'

const alertStore = useAlertStore()
const authStore  = useAuthStore()
const cartStore  = useCartStore()

onMounted(async () => {
  if (authStore.isLoggedIn) {
    await authStore.fetchProfile()
    await cartStore.fetchCart()
  }
})
</script>
