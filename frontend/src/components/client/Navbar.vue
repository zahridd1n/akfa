<template>
  <!-- Desktop Navbar (md+) -->
  <header class="sticky top-0 z-50 bg-white/95 backdrop-blur-md border-b border-slate-100 shadow-sm">
    <div class="container-custom">
      <div class="flex items-center justify-between h-16">

        <!-- Logo -->
        <router-link to="/" class="flex items-center gap-2 flex-shrink-0">
          <span class="font-extrabold text-2xl text-brand-950 tracking-tight">Saramax</span>
        </router-link>

        <!-- Desktop Navigation -->
        <nav class="hidden md:flex items-center gap-6">
          <router-link to="/" class="nav-link" :class="{ active: route.path === '/' }">Bosh sahifa</router-link>
          <router-link to="/catalog" class="nav-link" :class="{ active: route.path.startsWith('/catalog') }">Katalog</router-link>
          <router-link to="/profile?tab=orders" class="nav-link">Buyurtmalarim</router-link>
          <a href="/#contact" class="nav-link">Bog'lanish</a>
        </nav>

        <!-- Right Actions -->
        <div class="flex items-center gap-2">

          <!-- Search (desktop only) -->
          <div class="hidden lg:flex items-center relative">
            <input
              v-model="searchQuery"
              @keyup.enter="doSearch"
              type="text"
              placeholder="Qidirish..."
              class="pl-9 pr-4 py-2 rounded-xl border border-slate-200 bg-slate-50 text-sm text-slate-700 placeholder-slate-400 focus:outline-none focus:ring-2 focus:ring-brand-400 focus:bg-white transition-all w-48 focus:w-64"
            />
            <Search class="absolute left-3 w-4 h-4 text-slate-400" />
          </div>

          <!-- Cart Icon -->
          <router-link to="/cart" class="relative p-2 text-slate-700 hover:text-brand-600 transition-colors">
            <ShoppingCart class="w-6 h-6" />
            <span v-if="cartStore.itemCount > 0" class="absolute top-0 right-0 w-5 h-5 bg-red-500 text-white text-[11px] font-bold rounded-full flex items-center justify-center border-2 border-white transform translate-x-1 -translate-y-1">
              {{ cartStore.itemCount }}
            </span>
          </router-link>

          <!-- Contact Button (desktop) -->
          <a href="/#contact" class="hidden sm:inline-flex btn-md btn-outline border-slate-200 text-slate-700 hover:bg-slate-50">
            Aloqa
          </a>

          <!-- User Menu (desktop) -->
          <div v-if="authStore.isLoggedIn" class="hidden md:block relative" ref="userMenuRef">
            <button @click="userMenuOpen = !userMenuOpen" class="flex items-center gap-2 btn-md bg-brand-950 text-white hover:bg-brand-900">
              <User class="w-4 h-4" />
              <span class="hidden sm:block text-sm font-medium">Profil</span>
            </button>
            <Transition name="modal">
              <div v-if="userMenuOpen" class="absolute right-0 mt-2 w-52 bg-white rounded-2xl shadow-xl border border-slate-100 py-2 z-50">
                <router-link to="/profile" @click="userMenuOpen = false" class="dropdown-item">
                  <User class="w-4 h-4" /> Profilim
                </router-link>
                <router-link to="/profile?tab=orders" @click="userMenuOpen = false" class="dropdown-item">
                  <Package class="w-4 h-4" /> Buyurtmalarim
                </router-link>
                <router-link to="/profile?tab=addresses" @click="userMenuOpen = false" class="dropdown-item">
                  <MapPin class="w-4 h-4" /> Manzillarim
                </router-link>
                <template v-if="authStore.isAdmin">
                  <div class="h-px bg-slate-100 my-1 mx-3" />
                  <router-link to="/admin/dashboard" @click="userMenuOpen = false" class="dropdown-item text-brand-600">
                    <LayoutDashboard class="w-4 h-4" /> Admin Panel
                  </router-link>
                </template>
                <div class="h-px bg-slate-100 my-1 mx-3" />
                <button @click="handleLogout" class="dropdown-item w-full text-red-500 hover:bg-red-50">
                  <LogOut class="w-4 h-4" /> Chiqish
                </button>
              </div>
            </Transition>
          </div>

          <!-- Login Button (desktop) -->
          <button v-if="!authStore.isLoggedIn" @click="authModalOpen = true" class="hidden md:inline-flex btn-md bg-brand-950 text-white hover:bg-brand-900" id="navbar-login-btn">
            <User class="w-4 h-4" />
            <span class="hidden sm:inline">Kirish</span>
          </button>

          <!-- Hamburger (mobile only) - still available -->
          <button @click="mobileMenuOpen = !mobileMenuOpen" class="md:hidden btn-ghost btn-sm rounded-xl p-2">
            <Menu v-if="!mobileMenuOpen" class="w-5 h-5" />
            <X v-else class="w-5 h-5" />
          </button>
        </div>
      </div>
    </div>

    <!-- Mobile Hamburger Drawer (slide from top) -->
    <Transition name="slide-down">
      <div v-if="mobileMenuOpen" class="md:hidden border-t border-slate-100 bg-white px-4 py-4 flex flex-col gap-2 shadow-lg">
        <!-- Search -->
        <div class="relative mb-1">
          <input v-model="searchQuery" @keyup.enter="doSearch" type="text" placeholder="Qidirish..." class="form-input text-sm pl-9" />
          <Search class="absolute left-3 top-1/2 -translate-y-1/2 w-4 h-4 text-slate-400" />
        </div>
        <router-link to="/" @click="mobileMenuOpen = false" class="mobile-nav-link" :class="{ 'text-brand-600 bg-brand-50': route.path === '/' }">
          <Home class="w-4 h-4" /> Bosh sahifa
        </router-link>
        <router-link to="/catalog" @click="mobileMenuOpen = false" class="mobile-nav-link" :class="{ 'text-brand-600 bg-brand-50': route.path.startsWith('/catalog') }">
          <Grid class="w-4 h-4" /> Katalog
        </router-link>
        <router-link to="/profile?tab=orders" @click="mobileMenuOpen = false" class="mobile-nav-link">
          <Package class="w-4 h-4" /> Buyurtmalarim
        </router-link>
        <a href="/#contact" @click="mobileMenuOpen = false" class="mobile-nav-link">
          <Phone class="w-4 h-4" /> Bog'lanish
        </a>
        <template v-if="authStore.isLoggedIn">
          <div class="h-px bg-slate-100 my-1" />
          <router-link to="/profile" @click="mobileMenuOpen = false" class="mobile-nav-link">
            <User class="w-4 h-4" /> Profilim
          </router-link>
          <template v-if="authStore.isAdmin">
            <router-link to="/admin/dashboard" @click="mobileMenuOpen = false" class="mobile-nav-link text-brand-600">
              <LayoutDashboard class="w-4 h-4" /> Admin Panel
            </router-link>
          </template>
          <button @click="handleLogout; mobileMenuOpen = false" class="mobile-nav-link text-red-500 w-full text-left">
            <LogOut class="w-4 h-4" /> Chiqish
          </button>
        </template>
        <template v-else>
          <div class="h-px bg-slate-100 my-1" />
          <button @click="authModalOpen = true; mobileMenuOpen = false" class="btn-md btn-primary w-full">
            <User class="w-4 h-4" /> Kirish / Ro'yxatdan o'tish
          </button>
        </template>
      </div>
    </Transition>
  </header>

  <!-- ─── Mobile Bottom Tab Bar (md dan kichik ekranlar uchun) ─── -->
  <nav class="md:hidden fixed bottom-0 left-0 right-0 z-50 bg-white border-t border-slate-200 safe-area-bottom">
    <div class="grid grid-cols-5 h-16">

      <!-- Bosh sahifa -->
      <router-link to="/" class="bottom-tab" :class="{ active: route.path === '/' }">
        <Home class="w-5 h-5" />
        <span>Bosh sahifa</span>
      </router-link>

      <!-- Katalog -->
      <router-link to="/catalog" class="bottom-tab" :class="{ active: route.path.startsWith('/catalog') }">
        <Grid class="w-5 h-5" />
        <span>Katalog</span>
      </router-link>

      <!-- Buyurtmalarim -->
      <router-link to="/profile?tab=orders" class="bottom-tab" :class="{ active: route.path === '/profile' && route.query.tab === 'orders' }">
        <Package class="w-5 h-5" />
        <span>Buyurtma</span>
      </router-link>

      <!-- Savat -->
      <router-link to="/cart" class="bottom-tab relative" :class="{ active: route.path === '/cart' }">
        <div class="relative">
          <ShoppingCart class="w-5 h-5" />
          <span v-if="cartStore.itemCount > 0" class="absolute -top-1.5 -right-2 w-4 h-4 bg-red-500 text-white text-[10px] font-bold rounded-full flex items-center justify-center">
            {{ cartStore.itemCount > 9 ? '9+' : cartStore.itemCount }}
          </span>
        </div>
        <span>Savat</span>
      </router-link>

      <!-- Profil -->
      <button
        v-if="!authStore.isLoggedIn"
        @click="authModalOpen = true"
        class="bottom-tab"
      >
        <User class="w-5 h-5" />
        <span>Kirish</span>
      </button>
      <router-link v-else to="/profile" class="bottom-tab" :class="{ active: route.path === '/profile' && !route.query.tab }">
        <User class="w-5 h-5" />
        <span>Profil</span>
      </router-link>

    </div>
  </nav>

  <!-- Auth Modal -->
  <AuthModal :open="authModalOpen" @close="authModalOpen = false" @success="authModalOpen = false" />
</template>

<script setup>
import { ref, onMounted, onUnmounted } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import { Search, ShoppingCart, User, Package, MapPin, LogOut, Menu, X, LayoutDashboard, Home, Grid, Phone } from '@lucide/vue'
import { useAuthStore } from '@/stores/auth'
import { useCartStore } from '@/stores/cart'
import { useAlertStore } from '@/stores/alert'
import AuthModal from '@/components/client/AuthModal.vue'

const router = useRouter()
const route  = useRoute()
const authStore  = useAuthStore()
const cartStore  = useCartStore()
const alertStore = useAlertStore()

const searchQuery    = ref('')
const mobileMenuOpen = ref(false)
const userMenuOpen   = ref(false)
const authModalOpen  = ref(false)
const userMenuRef    = ref(null)

function doSearch() {
  if (searchQuery.value.trim()) {
    router.push({ name: 'catalog', query: { search: searchQuery.value.trim() } })
    searchQuery.value = ''
    mobileMenuOpen.value = false
  }
}

async function handleLogout() {
  userMenuOpen.value = false
  await authStore.logout()
  cartStore.resetCart()
  alertStore.success('Tizimdan chiqdingiz')
  router.push('/')
}

function handleClickOutside(e) {
  if (userMenuRef.value && !userMenuRef.value.contains(e.target)) {
    userMenuOpen.value = false
  }
}

function openAuthModal() { authModalOpen.value = true }

onMounted(() => {
  document.addEventListener('click', handleClickOutside)
  window.addEventListener('auth:open-modal', openAuthModal)
})
onUnmounted(() => {
  document.removeEventListener('click', handleClickOutside)
  window.removeEventListener('auth:open-modal', openAuthModal)
})
</script>

<style scoped>
/* Desktop nav links */
.nav-link {
  @apply px-1 py-2 text-sm font-medium text-slate-600 hover:text-brand-600 transition-colors duration-200 border-b-2 border-transparent;
}
.nav-link.active { @apply text-brand-600 border-brand-600; }

/* Dropdown items */
.dropdown-item {
  @apply flex items-center gap-2.5 px-4 py-2.5 text-sm text-slate-700 hover:bg-slate-50 hover:text-slate-900 transition-colors duration-150 w-full text-left;
}

/* Hamburger drawer links */
.mobile-nav-link {
  @apply flex items-center gap-3 px-4 py-3 rounded-xl text-sm font-medium text-slate-700 hover:bg-slate-50 hover:text-slate-900 transition-colors;
}

/* Bottom Tab Bar items */
.bottom-tab {
  @apply flex flex-col items-center justify-center gap-0.5 text-slate-400 text-[10px] font-medium transition-all duration-200 w-full;
}
.bottom-tab.active {
  @apply text-brand-600;
}
.bottom-tab.active svg {
  @apply text-brand-600;
}

/* Slide down animation for hamburger menu */
.slide-down-enter-active,
.slide-down-leave-active {
  transition: all 0.25s ease;
}
.slide-down-enter-from,
.slide-down-leave-to {
  opacity: 0;
  transform: translateY(-10px);
}

/* Safe area for iOS notch */
.safe-area-bottom {
  padding-bottom: env(safe-area-inset-bottom, 0px);
}
</style>
