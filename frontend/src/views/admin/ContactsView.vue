<template>
  <div class="space-y-5 max-w-full overflow-hidden">
    <div class="flex items-center justify-between flex-wrap gap-3">
      <div>
        <h1 class="text-xl sm:text-2xl font-bold text-white">Murojatlar</h1>
        <p class="text-xs sm:text-sm text-slate-400 mt-0.5">Foydalanuvchilardan kelgan xabarlar</p>
      </div>
      <div class="flex items-center gap-2">
        <button
          @click="filter = ''"
          :class="filter === '' ? 'btn-primary text-white' : 'bg-slate-800 text-slate-300 hover:bg-slate-700 border border-slate-700'"
          class="btn-sm text-xs"
        >
          Barchasi
        </button>
        <button
          @click="filter = 'unread'"
          :class="filter === 'unread' ? 'btn-primary text-white' : 'bg-slate-800 text-slate-300 hover:bg-slate-700 border border-slate-700'"
          class="btn-sm text-xs"
        >
          O'qilmagan
          <span v-if="unreadCount > 0" class="ml-1.5 px-1.5 py-0.5 bg-red-500 text-white text-[10px] rounded-full font-bold">{{ unreadCount }}</span>
        </button>
      </div>
    </div>

    <!-- Loading -->
    <div v-if="loading" class="space-y-3">
      <div v-for="i in 4" :key="i" class="skeleton h-20 rounded-2xl bg-slate-800" />
    </div>

    <!-- Empty -->
    <div v-else-if="!filtered.length" class="text-center py-16 bg-slate-800/80 rounded-2xl border border-slate-700/80">
      <MessageCircle class="w-12 h-12 text-slate-600 mx-auto mb-3" />
      <p class="text-slate-400 text-sm font-medium">Murojatlar yo'q</p>
    </div>

    <!-- Messages List -->
    <div v-else class="space-y-3">
      <div
        v-for="msg in filtered"
        :key="msg.id"
        class="bg-slate-800/90 rounded-2xl border p-4 transition-all shadow-sm"
        :class="msg.is_read ? 'border-slate-700/70 opacity-85' : 'border-brand-500/50 bg-slate-800/95 ring-1 ring-brand-500/30'"
      >
        <div class="flex flex-col sm:flex-row sm:items-start justify-between gap-3">
          <div class="flex items-start gap-3 flex-1 min-w-0">
            <!-- Unread dot -->
            <div
              class="w-2.5 h-2.5 rounded-full mt-1.5 flex-shrink-0 transition-colors"
              :class="msg.is_read ? 'bg-transparent' : 'bg-brand-400 shadow-glow'"
            />
            <div class="flex-1 min-w-0">
              <div class="flex flex-wrap items-center gap-x-3 gap-y-1 mb-1.5">
                <span class="font-bold text-white text-sm sm:text-base truncate">{{ msg.name }}</span>
                <a :href="`tel:${msg.phone}`" class="text-xs sm:text-sm text-brand-400 hover:text-brand-300 hover:underline flex-shrink-0">
                  {{ msg.phone }}
                </a>
                <span class="text-[11px] text-slate-400 sm:ml-auto flex-shrink-0">{{ formatDate(msg.created_at) }}</span>
              </div>
              <p v-if="msg.message" class="text-xs sm:text-sm text-slate-300 leading-relaxed break-words whitespace-pre-line bg-slate-900/40 p-3 rounded-xl border border-slate-700/40 mt-2">
                {{ msg.message }}
              </p>
            </div>
          </div>
          <!-- Actions -->
          <div class="flex items-center justify-end gap-2 flex-shrink-0 pt-2 sm:pt-0 border-t sm:border-t-0 border-slate-700/50">
            <button
              @click="toggleRead(msg)"
              class="px-3 py-1.5 rounded-xl text-xs font-medium transition-colors"
              :class="msg.is_read ? 'bg-slate-700/80 text-slate-300 hover:bg-slate-700 hover:text-white' : 'bg-brand-500/20 text-brand-300 border border-brand-500/40 hover:bg-brand-500/30'"
              :title="msg.is_read ? 'O\'qilmagan deb belgilash' : 'O\'qildi deb belgilash'"
            >
              {{ msg.is_read ? 'O\'qilmagan' : 'O\'qildi' }}
            </button>
            <button
              @click="deleteMsg(msg)"
              class="p-2 text-slate-400 hover:text-red-400 hover:bg-red-950/40 transition-colors rounded-xl"
              title="O'chirish"
            >
              <Trash2 class="w-4 h-4" />
            </button>
          </div>
        </div>
      </div>
    </div>

    <!-- Confirm Modal -->
    <Transition name="modal">
      <div v-if="confirmModal.show" class="fixed inset-0 z-50 flex items-center justify-center p-4 bg-black/75 backdrop-blur-sm">
        <div class="bg-slate-900 border border-slate-700 rounded-2xl shadow-2xl max-w-sm w-full p-6 text-white">
          <div class="w-12 h-12 bg-red-500/15 rounded-2xl flex items-center justify-center mb-4 mx-auto">
            <AlertCircle class="w-6 h-6 text-red-400" />
          </div>
          <h3 class="text-lg font-bold text-white text-center mb-2">Murojatni o'chirish</h3>
          <p class="text-slate-400 text-center text-xs sm:text-sm mb-6">Ushbu murojatni o'chirishni tasdiqlaysizmi?</p>
          <div class="flex gap-3">
            <button @click="confirmModal.show = false" class="flex-1 btn-md bg-slate-800 text-slate-300 hover:bg-slate-700 border border-slate-700">Bekor qilish</button>
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
