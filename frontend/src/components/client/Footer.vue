<template>
  <footer class="bg-brand-950 text-white pt-16 pb-8">
    <div class="container-custom">
      <div class="grid grid-cols-1 md:grid-cols-4 gap-10 mb-16">
        
        <!-- Brand -->
        <div class="col-span-1">
          <h3 class="font-bold text-2xl mb-4">Saramax</h3>
          <p class="text-sm text-slate-300/80 leading-relaxed max-w-[200px]">
            {{ siteStore.footerAbout }}
          </p>
        </div>

        <!-- Links 1 -->
        <div class="col-span-1 flex flex-col gap-3 text-sm">
          <router-link to="/catalog" class="text-slate-300/80 hover:text-white transition-colors">Katalog</router-link>
          <router-link to="/about" class="text-slate-300/80 hover:text-white transition-colors">Biz haqimizda</router-link>
          <router-link to="/contact" class="text-slate-300/80 hover:text-white transition-colors">Bog'lanish</router-link>
        </div>

        <!-- Contacts -->
        <div class="col-span-1 flex flex-col gap-3 text-sm">
          <a v-if="siteStore.telegramUrl" :href="siteStore.telegramUrl" target="_blank" class="text-slate-300/80 hover:text-white transition-colors">Telegram</a>
          <a v-if="siteStore.instagramUrl" :href="siteStore.instagramUrl" target="_blank" class="text-slate-300/80 hover:text-white transition-colors">Instagram</a>
          <p class="text-slate-300/80">
            <span class="font-semibold">Manzil:</span> {{ siteStore.address || "O'zbekiston" }}
          </p>
          <a v-if="siteStore.phoneMain" :href="`tel:${siteStore.phoneMain}`" class="text-slate-300/80 hover:text-white transition-colors">{{ siteStore.phoneMain }}</a>
        </div>

        <!-- Terms -->
        <div class="col-span-1 flex flex-col gap-3 text-sm">
          <a href="#" class="text-slate-300/80 hover:text-white transition-colors">Maxfiylik siyosati</a>
          <a href="#" class="text-slate-300/80 hover:text-white transition-colors">Foydalanish shartlari</a>
        </div>
      </div>

      <!-- Copyright -->
      <div class="text-center text-xs text-slate-300/60 pt-8 border-t border-white/10">
        © {{ new Date().getFullYear() }} {{ siteStore.footerCopyright }}
      </div>
    </div>
  </footer>
</template>

<script setup>
import { onMounted } from 'vue'
import { useSiteStore } from '@/stores/site'

const siteStore = useSiteStore()

onMounted(() => {
  siteStore.fetchSettings()
})
</script>
