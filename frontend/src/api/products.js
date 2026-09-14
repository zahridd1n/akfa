import api from './axios'

export const productsApi = {
  getCategories: () => api.get('/categories/'),
  getCategory: (slug) => api.get(`/categories/${slug}/`),

  getProducts: (params = {}) => api.get('/products/', { params }),
  getProduct: (slug) => api.get(`/products/${slug}/`),
  getProductColors: (slug) => api.get(`/products/${slug}/colors/`),
  calculatePrice: (slug, data) => api.post(`/products/${slug}/calculate_price/`, data),

  getBanners: () => api.get('/banners/'),
  getSiteSettings: () => api.get('/site-settings/'),
}
