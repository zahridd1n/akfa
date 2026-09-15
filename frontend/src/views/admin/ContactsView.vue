<template>
  <div>
    <div class="flex items-center justify-between mb-6">
      <div>
        <h1 class="text-2xl font-bold text-slate-900">Murojatlar</h1>
        <p class="text-sm text-slate-500 mt-1">Foydalanuvchilardan kelgan xabarlar</p>
      </div>
      <div class="flex items-center gap-3">
        <button @click="filter = ''" :class="filter === '' ? 'btn-primary' : 'btn-outline'" class="btn-sm">Barchasi</button>
        <button @click="filter = 'unread'" :class="filter === 'unread' ? 'btn-primary' : 'btn-outline'" class="btn-sm">
          O'qilmagan
          <span v-if="unreadCount > 0" class="ml-1 px-1.5 py-0.5 bg-red-500 text-white text-[10px] rounded-full">{{ unreadCount }}</span>
        </button>
      </div>
    </div>

    <!-- Loading -->
    <div v-if="loading" class="space-y-3">
      <div v-for="i in 5" :key="i" class="skeleton h-20 rounded-xl" />
    </div>

    <!-- Empty -->
    <div v-else-if="!filtered.length" class="text-center py-20 bg-white rounded-2xl border border-slate-100">
      <MessageCircle class="w-12 h-12 text-slate-200 mx-auto mb-3" />
      <p class="text-slate-500 font-medium">Murojatlar yo'q</p>
    </div>

    <!-- Messages List -->
    <div v-else class="space-y-3">
      <div
        v-for="msg in filtered"
        :key="msg.id"
        class="bg-white rounded-xl border p-4 transition-all"
        :class="msg.is_read ? 'border-slate-100' : 'border-brand-200 shadow-sm'"
      >
        <div class="flex items-start justify-between gap-3">
          <div class="flex items-start gap-3 flex-1 min-w-0">
            <!-- Unread dot -->
            <div class="w-2 h-2 rounded-full mt-2 flex-shrink-0 transition-colors" :class="msg.is_read ? 'bg-transparent' : 'bg-brand-500'" />
            <div class="flex-1 min-w-0">
              <div class="flex items-center gap-3 mb-1">
                <span class="font-bold text-slate-900 text-sm">{{ msg.name }}</span>
                <a :href="`tel:${msg.phone}`" class="text-sm text-brand-600 hover:underline">{{ msg.phone }}</a>
                <span class="text-xs text-slate-400 ml-auto flex-shrink-0">{{ formatDate(msg.created_at) }}</span>
              </div>
              <p v-if="msg.message" class="text-sm text-slate-600 leading-relaxed">{{ msg.message }}</p>
            </div>
          </div>
          <!-- Actions -->
          <div class="flex items-center gap-2 flex-shrink-0">
            <button
              @click="toggleRead(msg)"
              class="px-2.5 py-1.5 rounded-lg text-xs font-medium transition-colors"
              :class="msg.is_read ? 'bg-slate-100 text-slate-600 hover:bg-slate-200' : 'bg-brand-50 text-brand-700 hover:bg-brand-100'"
              :title="msg.is_read ? 'O\'qilmagan deb belgilash' : 'O\'qildi deb belgilash'"
            >
              {{ msg.is_read ? 'O\'qilmagan' : 'O\'qildi' }}
            </button>
            <button @click="deleteMsg(msg)" class="p-1.5 text-slate-400 hover:text-red-500 transition-colors rounded-lg hover:bg-red-50">
              <Trash2 class="w-4 h-4" />
            </button>
          </div>
        </div>
      </div>
    </div>

    <!-- Confirm Modal -->
    <Transition name="fade">
      <div v-if="confirmModal.show" class="fixed inset-0 z-50 flex items-center justify-center p-4 bg-slate-900/50 backdrop-blur-sm">
        <div class="bg-white rounded-2xl shadow-xl max-w-sm w-full p-6">
          <div class="w-12 h-12 bg-red-100 rounded-full flex items-center justify-center mb-4 mx-auto">
            <AlertCircle class="w-6 h-6 text-red-500" />
          </div>
          <h3 class="text-lg font-bold text-slate-900 text-center mb-2">Murojatni o'chirish</h3>
          <p class="text-slate-500 text-center text-sm mb-6">Ushbu murojatni o'chirishni tasdiqlaysizmi?</p>
          <div class="flex gap-3">
            <button @click="confirmModal.show = false" class="flex-1 btn-md btn-outline border-slate-200">Bekor qilish</button>
            <button @click="confirmDelete" class="flex-1 btn-md btn-danger">O'chirish</button>
          </div>
        </div>
      </div>
    </Transition>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { MessageCircle, Trash2, AlertCircle } from '@lucide/vue'
import { siteApi } from '@/api/site'
import { useAlertStore } from '@/stores/alert'

const alertStore = useAlertStore()
const messages   = ref([])
const loading    = ref(true)
const filter     = ref('')
const confirmModal = ref({ show: false, msg: null })

const filtered = computed(() => {
  if (filter.value === 'unread') return messages.value.filter(m => !m.is_read)
  return messages.value
})

const unreadCount = computed(() => messages.value.filter(m => !m.is_read).length)

async function fetchMessages() {
  loading.value = true
  try {
    const res = await siteApi.getContacts()
    messages.value = res.data
  } catch {}
  loading.value = false
}

async function toggleRead(msg) {
  const newVal = !msg.is_read
  try {
    await siteApi.markRead(msg.id, newVal)
    msg.is_read = newVal
  } catch { alertStore.error('Xatolik yuz berdi') }
}

function deleteMsg(msg) {
  confirmModal.value = { show: true, msg }
}

async function confirmDelete() {
  try {
    await siteApi.deleteContact(confirmModal.value.msg.id)
    messages.value = messages.value.filter(m => m.id !== confirmModal.value.msg.id)
    alertStore.info("Murojat o'chirildi")
  } catch { alertStore.error('Xatolik yuz berdi') }
  confirmModal.value.show = false
}

function formatDate(d) {
  return new Date(d).toLocaleString('uz-UZ', {
    day: '2-digit', month: 'short', year: 'numeric', hour: '2-digit', minute: '2-digit'
  })
}

onMounted(fetchMessages)
</script>
