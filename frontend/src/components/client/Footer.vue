<template>
  <footer class="bg-brand-950 text-white pt-16 pb-8">
    <div class="container-custom">
      <div class="grid grid-cols-1 md:grid-cols-4 gap-10 mb-16">
        
        <!-- Brand -->
        <div class="col-span-1">
          <h3 class="font-bold text-2xl mb-4">Saramax</h3>
          <p class="text-sm text-slate-300/80 leading-relaxed max-w-[200px]">
            Sifatli deraza va eshiklar bilan kelajakni quramiz.
          </p>
        </div>

        <!-- Links 1 -->
        <div class="col-span-1 flex flex-col gap-3 text-sm">
          <router-link to="/catalog" class="text-slate-300/80 hover:text-white transition-colors">Katalog</router-link>
          <a href="/#about" class="text-slate-300/80 hover:text-white transition-colors">Biz haqimizda</a>
          <a href="/#contact" class="text-slate-300/80 hover:text-white transition-colors">Bog'lanish</a>
        </div>

        <!-- Contacts -->
        <div class="col-span-1 flex flex-col gap-3 text-sm">
          <a href="#" class="text-slate-300/80 hover:text-white transition-colors">Telegram</a>
          <p class="text-slate-300/80">Manzil: Yaypan Shaharchasi</p>
        </div>

        <!-- Terms -->
        <div class="col-span-1 flex flex-col gap-3 text-sm">
          <a href="#" class="text-slate-300/80 hover:text-white transition-colors">Maxfiylik siyosati</a>
          <a href="#" class="text-slate-300/80 hover:text-white transition-colors">Foydalanish shartlari</a>
        </div>
      </div>

      <!-- Copyright -->
      <div class="text-center text-xs text-slate-300/60 pt-8 border-t border-white/10">
        © {{ new Date().getFullYear() }} Saramax. Barcha huquqlar himoyalangan.
      </div>
    </div>
  </footer>
</template>

<script setup>
// Minimal footer
</script>
