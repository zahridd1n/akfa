<template>
  <div class="min-h-screen bg-slate-950 flex w-full max-w-full overflow-x-hidden text-slate-100 antialiased selection:bg-brand-500/30 selection:text-white">

    <!-- Sidebar Drawer -->
    <aside
      class="fixed inset-y-0 left-0 z-50 flex flex-col w-72 sm:w-64 bg-slate-900 border-r border-slate-800 shadow-2xl lg:shadow-none transition-transform duration-300 ease-in-out lg:translate-x-0"
      :class="sidebarOpen ? 'translate-x-0' : '-translate-x-full'"
    >
      <!-- Logo & Close (Mobile) -->
      <div class="flex items-center justify-between px-5 py-4 border-b border-slate-800">
        <div class="flex items-center gap-3">
          <div class="w-9 h-9 bg-gradient-to-br from-brand-500 to-brand-700 rounded-xl flex items-center justify-center shadow-glow flex-shrink-0">
            <span class="text-white font-bold">S</span>
          </div>
          <div>
            <span class="font-bold text-white text-base tracking-tight">Saramax</span>
            <p class="text-[10px] text-slate-400 -mt-0.5">Admin Panel</p>
          </div>
        </div>
        <button
          @click="sidebarOpen = false"
          class="lg:hidden p-2 rounded-xl text-slate-400 hover:text-white hover:bg-slate-800 transition-colors"
          title="Yopish"
        >
          <X class="w-5 h-5" />
        </button>
      </div>

      <!-- Navigation -->
      <nav class="flex-1 px-3 py-4 overflow-y-auto space-y-4">
        <div>
          <p class="text-[10px] font-semibold text-slate-400 uppercase tracking-widest px-3 mb-2">Boshqaruv</p>
          <ul class="space-y-1">
            <li v-for="item in navItems" :key="item.to">
              <router-link
                :to="item.to"
                class="admin-sidebar-link"
                :class="{ active: route.path.startsWith(item.to) }"
                @click="sidebarOpen = false"
              >
                <component :is="item.icon" class="w-4.5 h-4.5 flex-shrink-0" />
                <span class="truncate">{{ item.label }}</span>
                <span v-if="item.badge" class="ml-auto badge badge-amber text-[10px]">{{ item.badge }}</span>
              </router-link>
            </li>
          </ul>
        </div>

        <div class="h-px bg-slate-800/80 mx-2" />

        <div>
          <p class="text-[10px] font-semibold text-slate-400 uppercase tracking-widest px-3 mb-2">Tizim</p>
          <ul class="space-y-1">
            <li>
              <router-link to="/" class="admin-sidebar-link" @click="sidebarOpen = false">
                <Globe class="w-4.5 h-4.5 flex-shrink-0" /> Saytga o'tish
              </router-link>
            </li>
            <li>
              <button @click="handleLogout" class="admin-sidebar-link w-full text-red-400 hover:text-red-300 hover:bg-red-950/40">
                <LogOut class="w-4.5 h-4.5 flex-shrink-0" /> Chiqish
              </button>
            </li>
          </ul>
        </div>
      </nav>

      <!-- Admin User Profile Footer -->
      <div class="border-t border-slate-800 px-4 py-3.5 flex items-center gap-3 bg-slate-900/60">
        <div class="w-9 h-9 bg-gradient-to-tr from-brand-600 to-brand-400 rounded-xl flex items-center justify-center text-white font-semibold text-sm flex-shrink-0 shadow-sm">
          {{ (authStore.fullName || 'A').charAt(0).toUpperCase() }}
        </div>
        <div class="min-w-0 flex-1">
          <p class="text-sm font-medium text-white truncate">{{ authStore.fullName || 'Administrator' }}</p>
          <p class="text-[11px] text-emerald-400 flex items-center gap-1.5">
            <span class="w-1.5 h-1.5 rounded-full bg-emerald-400 animate-pulse"></span>
            Online
          </p>
        </div>
      </div>
    </aside>

    <!-- Main Content Container -->
    <div class="flex-1 lg:ml-64 flex flex-col min-h-screen min-w-0 w-full overflow-x-hidden">
      <!-- Top Bar -->
      <header class="sticky top-0 z-30 bg-slate-900/90 backdrop-blur-md border-b border-slate-800 px-3.5 sm:px-6 h-14 flex items-center justify-between gap-3">
        <div class="flex items-center gap-3 min-w-0">
          <button
            @click="sidebarOpen = !sidebarOpen"
            class="lg:hidden p-2 rounded-xl text-slate-300 hover:text-white hover:bg-slate-800 transition-colors focus:outline-none focus:ring-2 focus:ring-brand-500/40"
            title="Menyuni ochish"
          >
            <Menu class="w-5 h-5" />
          </button>
          <div class="min-w-0">
            <h1 class="text-sm sm:text-base font-semibold text-white truncate">{{ pageTitle }}</h1>
          </div>
        </div>

        <div class="flex items-center gap-3 text-slate-400 text-xs">
          <div class="hidden sm:flex items-center gap-1.5 bg-slate-800/80 px-3 py-1.5 rounded-xl border border-slate-700/60">
            <Clock class="w-3.5 h-3.5 text-brand-400" />
            <span class="font-medium text-slate-200">{{ currentTime }}</span>
          </div>
          <router-link
            to="/"
            class="hidden md:flex items-center gap-1 text-slate-400 hover:text-white px-2.5 py-1.5 rounded-lg hover:bg-slate-800 transition-colors text-xs"
          >
            <Globe class="w-3.5 h-3.5" />
            <span>Sayt</span>
          </router-link>
        </div>
      </header>

      <!-- Page Content View -->
      <main class="flex-1 p-3.5 sm:p-6 text-white pb-24 lg:pb-8 w-full min-w-0 max-w-full overflow-x-hidden">
        <RouterView v-slot="{ Component }">
          <Transition name="page" mode="out-in">
            <component :is="Component" :key="route.fullPath" />
          </Transition>
        </RouterView>
      </main>
    </div>

    <!-- Mobile Floating Bottom Navigation Dock -->
    <div class="fixed bottom-3 inset-x-3 z-40 lg:hidden pointer-events-none flex justify-center">
      <nav class="w-full max-w-md bg-slate-900/95 backdrop-blur-xl border border-slate-700/80 shadow-2xl rounded-2xl p-1.5 flex items-center justify-around pointer-events-auto">
        <router-link
          v-for="tab in mobileQuickTabs"
          :key="tab.to"
          :to="tab.to"
          class="flex flex-col items-center justify-center py-1.5 px-2 rounded-xl transition-all relative flex-1 text-center"
          :class="route.path.startsWith(tab.to)
            ? 'text-brand-400 bg-brand-500/15 font-semibold'
            : 'text-slate-400 hover:text-slate-200'"
          @click="sidebarOpen = false"
        >
          <component :is="tab.icon" class="w-5 h-5" />
          <span class="text-[10px] mt-0.5 tracking-tight leading-tight truncate max-w-[64px]">{{ tab.label }}</span>
        </router-link>

        <!-- Menu Drawer Button -->
        <button
          @click="sidebarOpen = !sidebarOpen"
          class="flex flex-col items-center justify-center py-1.5 px-2 rounded-xl transition-all relative flex-1 text-center"
          :class="sidebarOpen ? 'text-brand-400 bg-brand-500/15 font-semibold' : 'text-slate-400 hover:text-slate-200'"
          title="Ko'proq menyu"
        >
          <Menu class="w-5 h-5" />
          <span class="text-[10px] mt-0.5 tracking-tight leading-tight">Menyu</span>
        </button>
      </nav>
    </div>

    <!-- Mobile Sidebar Backdrop Overlay -->
    <Transition name="fade">
      <div
        v-if="sidebarOpen"
        @click="sidebarOpen = false"
        class="fixed inset-0 bg-black/75 backdrop-blur-sm z-40 lg:hidden transition-opacity"
      />
    </Transition>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, onUnmounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import {
  LayoutDashboard,
  Package,
  ShoppingBag,
  Users,
  BarChart3,
  Menu,
  X,
  LogOut,
  Globe,
  Clock,
  MessageCircle
} from '@lucide/vue'
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

const mobileQuickTabs = [
  { to: '/admin/dashboard', label: 'Bosh sahifa', icon: LayoutDashboard },
  { to: '/admin/products',  label: 'Mahsulotlar', icon: Package },
  { to: '/admin/orders',    label: 'Buyurtma',    icon: ShoppingBag },
  { to: '/admin/customers', label: 'Mijozlar',    icon: Users },
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
  router.push('/admin/login')
}
</script>
