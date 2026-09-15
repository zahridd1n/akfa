<template>
  <div class="min-h-screen bg-slate-950 flex">

    <!-- Sidebar -->
    <aside
      class="fixed inset-y-0 left-0 z-50 flex flex-col w-64 bg-slate-900 border-r border-slate-800 transition-transform duration-300 lg:translate-x-0"
      :class="sidebarOpen ? 'translate-x-0' : '-translate-x-full'"
    >
      <!-- Logo -->
      <div class="flex items-center gap-3 px-6 py-5 border-b border-slate-800">
        <div class="w-9 h-9 bg-gradient-to-br from-brand-500 to-brand-700 rounded-xl flex items-center justify-center shadow-glow flex-shrink-0">
          <span class="text-white font-bold">S</span>
        </div>
        <div>
          <span class="font-bold text-white text-base">Saramax</span>
          <p class="text-[10px] text-slate-500 -mt-0.5">Admin Panel</p>
        </div>
      </div>

      <!-- Navigation -->
      <nav class="flex-1 px-3 py-4 overflow-y-auto">
        <p class="text-[10px] font-semibold text-slate-500 uppercase tracking-widest px-4 mb-3">Asosiy</p>
        <ul class="space-y-1">
          <li v-for="item in navItems" :key="item.to">
            <router-link
              :to="item.to"
              class="admin-sidebar-link"
              :class="{ active: route.path.startsWith(item.to) }"
              @click="sidebarOpen = false"
            >
              <component :is="item.icon" class="w-4.5 h-4.5 flex-shrink-0" />
              {{ item.label }}
              <span v-if="item.badge" class="ml-auto badge badge-amber text-[10px]">{{ item.badge }}</span>
            </router-link>
          </li>
        </ul>

        <div class="h-px bg-slate-800 mx-4 my-4" />

        <p class="text-[10px] font-semibold text-slate-500 uppercase tracking-widest px-4 mb-3">Boshqa</p>
        <ul class="space-y-1">
          <li>
            <router-link to="/" class="admin-sidebar-link">
              <Globe class="w-4.5 h-4.5" /> Saytni ko'rish
            </router-link>
          </li>
          <li>
            <button @click="handleLogout" class="admin-sidebar-link w-full text-red-400 hover:text-red-300 hover:bg-red-900/20">
              <LogOut class="w-4.5 h-4.5" /> Chiqish
            </button>
          </li>
        </ul>
      </nav>

      <!-- Admin User -->
      <div class="border-t border-slate-800 px-4 py-3 flex items-center gap-3">
        <div class="w-8 h-8 bg-brand-600 rounded-xl flex items-center justify-center text-white font-semibold text-sm flex-shrink-0">
          {{ authStore.fullName.charAt(0).toUpperCase() }}
        </div>
        <div class="min-w-0">
          <p class="text-sm font-medium text-white truncate">{{ authStore.fullName }}</p>
          <p class="text-[11px] text-slate-500">Administrator</p>
        </div>
      </div>
    </aside>

    <!-- Main Content -->
    <div class="flex-1 lg:ml-64 flex flex-col min-h-screen">
      <!-- Top Bar -->
      <header class="sticky top-0 z-40 bg-slate-900/95 backdrop-blur border-b border-slate-800 px-4 sm:px-6 h-14 flex items-center gap-4">
        <button @click="sidebarOpen = !sidebarOpen" class="lg:hidden btn-ghost btn-sm rounded-xl p-2 text-slate-400">
          <Menu class="w-5 h-5" />
        </button>
        <div class="flex-1">
          <h1 class="text-sm font-semibold text-white">{{ pageTitle }}</h1>
        </div>
        <div class="flex items-center gap-2 text-slate-400 text-xs">
          <Clock class="w-3.5 h-3.5" />
          {{ currentTime }}
        </div>
      </header>

      <!-- Page Content -->
      <main class="flex-1 p-4 sm:p-6 text-white">
        <RouterView v-slot="{ Component }">
          <Transition name="page" mode="out-in">
            <component :is="Component" :key="route.fullPath" />
          </Transition>
        </RouterView>
      </main>
    </div>

    <!-- Mobile overlay -->
    <div
      v-if="sidebarOpen"
      @click="sidebarOpen = false"
      class="fixed inset-0 bg-black/60 z-40 lg:hidden"
    />
  </div>
</template>

<script setup>
import { ref, computed, onMounted, onUnmounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { LayoutDashboard, Package, ShoppingBag, Users, BarChart3, Menu, LogOut, Globe, Clock, MessageCircle } from '@lucide/vue'
import { useAuthStore } from '@/stores/auth'
import { useAlertStore } from '@/stores/alert'
import { useCartStore } from '@/stores/cart'

const route = useRoute()
const router = useRouter()
const authStore = useAuthStore()
const alertStore = useAlertStore()
const cartStore = useCartStore()

const sidebarOpen = ref(false)
const currentTime = ref('')

const navItems = [
  { to: '/admin/dashboard',  label: 'Dashboard',   icon: LayoutDashboard },
  { to: '/admin/products',   label: 'Mahsulotlar', icon: Package },
  { to: '/admin/orders',     label: 'Buyurtmalar', icon: ShoppingBag },
  { to: '/admin/customers',  label: 'Mijozlar',    icon: Users },
  { to: '/admin/contacts',   label: 'Murojatlar',  icon: MessageCircle },
  { to: '/admin/reports',    label: 'Hisobotlar',  icon: BarChart3 },
]

const pageTitle = computed(() => {
  const found = navItems.find(i => route.path.startsWith(i.to))
  return found?.label || 'Admin Panel'
})

function updateTime() {
  currentTime.value = new Date().toLocaleTimeString('uz-UZ', { hour: '2-digit', minute: '2-digit' })
}

let timer
onMounted(() => {
  updateTime()
  timer = setInterval(updateTime, 60000)
})
onUnmounted(() => clearInterval(timer))

async function handleLogout() {
  await authStore.logout()
  cartStore.resetCart()
  alertStore.success('Tizimdan chiqdingiz')
  router.push('/')
}
</script>
