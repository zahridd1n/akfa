import { defineStore } from 'pinia'
import { siteApi } from '@/api/site'

export const useSiteStore = defineStore('site', {
  state: () => ({
    settings: {},
    loading: false,
    fetched: false
  }),
  actions: {
    async fetchSettings() {
      if (this.fetched) return
      this.loading = true
      try {
        const res = await siteApi.getSettings()
        this.settings = res.data
        this.fetched = true
      } catch (e) {
        console.error('Failed to fetch site settings', e)
      } finally {
        this.loading = false
      }
    }
  },
  getters: {
    address: (state) => state.settings.address || '',
    phoneMain: (state) => state.settings.phone_main || '',
    telegramUrl: (state) => state.settings.telegram_url || '',
    instagramUrl: (state) => state.settings.instagram_url || '',
    facebookUrl: (state) => state.settings.facebook_url || '',
    youtubeUrl: (state) => state.settings.youtube_url || '',
    footerAbout: (state) => state.settings.footer_about || 'Sifatli deraza va eshiklar bilan kelajakni quramiz.',
    footerCopyright: (state) => state.settings.footer_copyright || 'Saramax. Barcha huquqlar himoyalangan.'
  }
})
