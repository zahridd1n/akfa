<template>
  <div class="max-w-3xl space-y-6">
    <div class="flex items-center gap-3">
      <router-link to="/admin/products" class="btn-sm btn-ghost text-slate-400 p-2">
        <ChevronLeft class="w-5 h-5" />
      </router-link>
      <h1 class="text-2xl font-bold text-white">{{ isEdit ? 'Mahsulotni Tahrirlash' : 'Yangi Mahsulot' }}</h1>
    </div>

    <form @submit.prevent="submit" class="space-y-6">
      <!-- Basic Info -->
      <div class="bg-slate-800 rounded-2xl p-6 border border-slate-700 space-y-4">
        <h2 class="font-semibold text-white mb-2">Asosiy ma'lumotlar</h2>

        <div class="grid grid-cols-1 sm:grid-cols-2 gap-4">
          <div>
            <label class="form-label text-slate-300">Mahsulot nomi *</label>
            <input v-model="form.name" type="text" class="form-input bg-slate-700 border-slate-600 text-white placeholder-slate-500 focus:border-brand-500" id="product-form-name" required />
          </div>
          <div>
            <label class="form-label text-slate-300">Kategoriya *</label>
            <select v-model="form.category" class="form-select bg-slate-700 border-slate-600 text-white focus:border-brand-500" id="product-form-category" required>
              <option value="">Tanlang...</option>
              <option v-for="cat in categories" :key="cat.id" :value="cat.id">{{ cat.name }}</option>
            </select>
          </div>
          <div>
            <label class="form-label text-slate-300">Material</label>
            <select v-model="form.material" class="form-select bg-slate-700 border-slate-600 text-white focus:border-brand-500">
              <option value="aluminium">Alyuminiy</option>
              <option value="pvc">PVX (Plastik)</option>
              <option value="wood">Yog'och</option>
              <option value="steel">Po'lat</option>
            </select>
          </div>
          <div>
            <label class="form-label text-slate-300">Baza Narx (m² uchun UZS) *</label>
            <input v-model.number="form.base_price" type="number" min="0" step="1000" class="form-input bg-slate-700 border-slate-600 text-white placeholder-slate-500 focus:border-brand-500" id="product-form-price" required />
          </div>
          <div>
            <label class="form-label text-slate-300">Badge (ixtiyoriy)</label>
            <select v-model="form.badge" class="form-select bg-slate-700 border-slate-600 text-white focus:border-brand-500">
              <option value="">Yo'q</option>
              <option value="new">Yangi</option>
              <option value="warm">Iliq-Issiq</option>
              <option value="sale">Sotuvda</option>
            </select>
          </div>
          <div>
            <label class="form-label text-slate-300">Dizayn uslubi</label>
            <select v-model="form.design_style" class="form-select bg-slate-700 border-slate-600 text-white focus:border-brand-500">
              <option value="modern">Zamonaviy</option>
              <option value="classic">Klassik</option>
              <option value="minimalist">Minimalist</option>
            </select>
          </div>
        </div>

        <div>
          <label class="form-label text-slate-300">Tavsif</label>
          <textarea v-model="form.description" rows="3" class="form-input bg-slate-700 border-slate-600 text-white placeholder-slate-500 focus:border-brand-500 resize-none" />
        </div>

        <div class="grid grid-cols-1 sm:grid-cols-3 gap-4">
          <div>
            <label class="form-label text-slate-300">Profil qalinligi (mm)</label>
            <input v-model="form.profile_thickness" type="text" placeholder="72mm" class="form-input bg-slate-700 border-slate-600 text-white placeholder-slate-500" />
          </div>
          <div>
            <label class="form-label text-slate-300">Shisha qavati (mm)</label>
            <input v-model="form.max_glass" type="text" placeholder="54mm" class="form-input bg-slate-700 border-slate-600 text-white placeholder-slate-500" />
          </div>
          <div>
            <label class="form-label text-slate-300">Ovoz izolyatsiyasi</label>
            <input v-model="form.sound_insulation" type="text" placeholder="43dB" class="form-input bg-slate-700 border-slate-600 text-white placeholder-slate-500" />
          </div>
        </div>

        <label class="flex items-center gap-2 cursor-pointer">
          <input v-model="form.is_active" type="checkbox" class="w-4 h-4" />
          <span class="text-slate-300 text-sm">Aktiv (saytda ko'rsatiladi)</span>
        </label>
      </div>

      <!-- Images -->
      <div class="bg-slate-800 rounded-2xl p-6 border border-slate-700">
        <h2 class="font-semibold text-white mb-1">Mahsulot Rasmlari</h2>
        <p class="text-slate-400 text-xs mb-4">Rasm qo'shish, o'chirish va asosiy rasmni belgilash</p>

        <!-- Yangi rasm yuklash -->
        <label
          class="flex flex-col items-center justify-center gap-2 w-full h-28 border-2 border-dashed border-slate-600 rounded-xl cursor-pointer hover:border-brand-500/60 hover:bg-brand-500/5 transition-colors mb-5"
        >
          <ImagePlus class="w-6 h-6 text-slate-500" />
          <span class="text-sm text-slate-400">Rasm tanlash / yuklash</span>
          <input ref="fileInputRef" type="file" accept="image/*" multiple class="hidden" @change="handleFileSelect" />
        </label>

        <!-- Boshqa/yangi rasmlar grid -->
        <div v-if="uploadFiles.length || existingImages.length" class="grid grid-cols-3 sm:grid-cols-4 md:grid-cols-5 gap-3">
          <!-- Mavjud rasmlar -->
          <div v-for="img in existingImages" :key="img.id" class="relative group rounded-xl overflow-hidden border border-slate-700 aspect-square bg-slate-700">
            <img :src="img.image" alt="Mahsulot rasmi" class="w-full h-full object-cover" />
            <div class="absolute top-1 right-1 flex gap-1">
              <button
                v-if="!img.is_main"
                type="button"
                @click="setMainImage(img)"
                title="Asosiy qilish"
                class="bg-slate-900/80 hover:bg-brand-600 text-white rounded-lg p-1.5 transition-colors"
              >
                <Star class="w-3.5 h-3.5" />
              </button>
              <button
                type="button"
                @click="removeExistingImage(img)"
                title="O'chirish"
                class="bg-slate-900/80 hover:bg-red-600 text-white rounded-lg p-1.5 transition-colors"
              >
                <Trash2 class="w-3.5 h-3.5" />
              </button>
            </div>
            <span
              v-if="img.is_main"
              class="absolute bottom-1 left-1 text-[10px] font-bold uppercase tracking-wide bg-brand-600/90 text-white px-2 py-0.5 rounded-md"
            >
              Asosiy
            </span>
          </div>

          <!-- Yangi tanlangan rasmlar -->
          <div v-for="(file, i) in uploadFiles" :key="'new-' + i" class="relative group rounded-xl overflow-hidden border border-slate-700 aspect-square bg-slate-700">
            <img :src="file.preview" alt="Yangi rasm" class="w-full h-full object-cover" />
            <button
              type="button"
              @click="uploadFiles.splice(i, 1)"
              title="O'chirish"
              class="absolute top-1 right-1 bg-slate-900/80 hover:bg-red-600 text-white rounded-lg p-1.5 transition-colors"
            >
              <X class="w-3.5 h-3.5" />
            </button>
          </div>
        </div>

        <p v-else class="text-slate-500 text-sm text-center py-4 border border-dashed border-slate-700 rounded-xl">
          Hozircha rasm yo'q. Yuqoridan rasm yuklang.
        </p>
        <div v-if="existingImages.length === 0 && uploadFiles.length > 0" class="mt-3 text-xs text-slate-500">
          Birinchi yuklangan rasm asosiy rasm bo'ladi.
        </div>
      </div>

      <!-- Colors -->
      <div class="bg-slate-800 rounded-2xl p-6 border border-slate-700">
        <h2 class="font-semibold text-white mb-4">Rang Variantlari</h2>
        <p class="text-slate-400 text-xs mb-4">Har bir rang uchun narx modifikatorini kiriting. 0 = baza narx, musbat = qo'shimcha narx</p>

        <div class="space-y-3 mb-4">
          <div v-for="(color, i) in form.colors" :key="i" class="flex items-center gap-3 bg-slate-700 rounded-xl p-3">
            <div class="w-8 h-8 rounded-lg border border-slate-600 flex-shrink-0" :style="{ backgroundColor: color.hex_code || '#888' }" />
            <input v-model="color.name" type="text" placeholder="Rang nomi" class="form-input bg-slate-600 border-slate-500 text-white text-sm py-1.5 flex-1" />
            <input v-model="color.hex_code" type="color" class="w-10 h-10 rounded-lg cursor-pointer bg-transparent border-0 p-0.5 flex-shrink-0" />
            <input v-model.number="color.price_modifier" type="number" step="1000" placeholder="Narx modif." class="form-input bg-slate-600 border-slate-500 text-white text-sm py-1.5 w-36" />
            <button type="button" @click="form.colors.splice(i, 1)" class="text-red-400 hover:text-red-300 flex-shrink-0">
              <X class="w-4 h-4" />
            </button>
          </div>
        </div>

        <button type="button" @click="addColor" class="btn-sm btn-outline border-slate-600 text-slate-300 hover:bg-slate-700">
          <Plus class="w-4 h-4" /> Rang qo'shish
        </button>
      </div>

      <!-- Submit -->
      <div class="flex gap-3">
        <button type="submit" :disabled="submitting" class="btn-lg btn-primary" id="product-form-submit">
          <span v-if="!submitting">{{ isEdit ? 'Saqlash' : 'Mahsulot qo\'shish' }}</span>
          <div v-else class="spinner" />
        </button>
        <router-link to="/admin/products" class="btn-lg btn-secondary">Bekor qilish</router-link>
      </div>
    </form>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { ChevronLeft, Plus, X, ImagePlus, Star, Trash2 } from '@lucide/vue'
import { adminApi } from '@/api/admin'
import { productsApi } from '@/api/products'
import { useAlertStore } from '@/stores/alert'

const route = useRoute()
const router = useRouter()
const alertStore = useAlertStore()

const isEdit = computed(() => !!route.params.id && route.params.id !== 'new')
const categories = ref([])
const submitting = ref(false)

const existingImages = ref([])
const uploadFiles = ref([])
const fileInputRef = ref(null)

const form = ref({
  name: '', description: '', category: '', material: 'aluminium',
  base_price: '', badge: '', design_style: 'modern',
  profile_thickness: '', max_glass: '', sound_insulation: '',
  is_active: true, colors: [],
})

function addColor() {
  form.value.colors.push({ name: '', hex_code: '#FFFFFF', price_modifier: 0 })
}

function handleFileSelect(e) {
  const files = Array.from(e.target.files || [])
  for (const file of files) {
    if (!file.type.startsWith('image/')) continue
    uploadFiles.value.push({
      file,
      preview: URL.createObjectURL(file),
    })
  }
  e.target.value = ''
}

async function setMainImage(img) {
  try {
    await adminApi.setProductMainImage(savedProductId(), img.id)
    existingImages.value.forEach(i => i.is_main = false)
    img.is_main = true
    alertStore.success('Asosiy rasm o\'rnatildi')
  } catch {
    alertStore.error('Xatolik yuz berdi')
  }
}

async function removeExistingImage(img) {
  try {
    await adminApi.deleteProductImage(savedProductId(), img.id)
    existingImages.value = existingImages.value.filter(i => i.id !== img.id)
    alertStore.success('Rasm o\'chirildi')
  } catch {
    alertStore.error('Xatolik yuz berdi')
  }
}

function savedProductId() {
  return isEdit.value ? route.params.id : null
}

async function submit() {
  submitting.value = true
  try {
    const data = new FormData()
    Object.entries(form.value).forEach(([key, val]) => {
      if (key !== 'colors') data.append(key, val)
    })

    let savedProduct
    if (isEdit.value) {
      const res = await adminApi.updateProduct(route.params.id, data)
      savedProduct = res.data
    } else {
      const res = await adminApi.createProduct(data)
      savedProduct = res.data
    }

    // Save colors (faqat yangilarini qo'shish, eskilari saqlanib qoladi)
    for (const color of form.value.colors) {
      if (!color.id && color.name && color.hex_code) {
        await adminApi.addProductColor(savedProduct.id, color)
      }
    }

    // Yangi rasmlarni yuklash
    const hasExistingMain = existingImages.value.some(i => i.is_main)
    for (let i = 0; i < uploadFiles.value.length; i++) {
      const item = uploadFiles.value[i]
      const imgData = new FormData()
      imgData.append('image', item.file)
      imgData.append('is_main', (!hasExistingMain && i === 0) ? 'true' : 'false')
      await adminApi.addProductImage(savedProduct.id, imgData)
      URL.revokeObjectURL(item.preview)
    }

    alertStore.success(isEdit.value ? 'Mahsulot yangilandi!' : 'Mahsulot qo\'shildi!')
    router.push('/admin/products')
  } catch (err) {
    alertStore.error(err.response?.data?.detail || 'Xatolik yuz berdi')
  }
  submitting.value = false
}

onMounted(async () => {
  const res = await productsApi.getCategories()
  categories.value = res.data.results || res.data

  if (isEdit.value) {
    try {
      const productRes = await adminApi.getProduct(route.params.id)
      const p = productRes.data
      existingImages.value = p.images || []
      form.value = {
        name: p.name, description: p.description, category: p.category?.id ?? p.category,
        material: p.material, base_price: p.base_price, badge: p.badge || '',
        design_style: p.design_style, profile_thickness: p.profile_thickness || '',
        max_glass: p.max_glass || '', sound_insulation: p.sound_insulation || '',
        is_active: p.is_active, colors: p.colors || [],
      }
    } catch { alertStore.error('Mahsulot topilmadi') }
  }
})
</script>
