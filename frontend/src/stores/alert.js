import { defineStore } from 'pinia'
import { ref } from 'vue'

let idCounter = 0

export const useAlertStore = defineStore('alert', () => {
  const toasts = ref([])

  function add(message, type = 'info', duration = 4000) {
    const id = ++idCounter
    toasts.value.push({ id, message, type })
    if (duration > 0) {
      setTimeout(() => remove(id), duration)
    }
    return id
  }

  function remove(id) {
    toasts.value = toasts.value.filter(t => t.id !== id)
  }

  const success = (msg, duration) => add(msg, 'success', duration)
  const error   = (msg, duration) => add(msg, 'error', duration)
  const info    = (msg, duration) => add(msg, 'info', duration)
  const warning = (msg, duration) => add(msg, 'warning', duration)

  return { toasts, add, remove, success, error, info, warning }
})
