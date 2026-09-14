<template>
  <div class="min-h-screen flex flex-col">
    <Navbar />
    <main class="flex-1 pb-16 md:pb-0">
      <RouterView v-slot="{ Component }">
        <Transition name="page" mode="out-in">
          <component :is="Component" :key="route.fullPath" />
        </Transition>
      </RouterView>
    </main>
    <Footer />
  </div>
</template>

<script setup>
import { useRoute } from 'vue-router'
import Navbar from '@/components/client/Navbar.vue'
import Footer from '@/components/client/Footer.vue'

const route = useRoute()
</script>
