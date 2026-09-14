import api from './axios'

export const adminApi = {
  // Dashboard
  getDashboard: (params = {}) => api.get('/admin-panel/dashboard/', { params }),

  // Products
  getProducts: (params = {}) => api.get('/admin-panel/products/', { params }),
  getProduct: (id) => api.get(`/admin-panel/products/${id}/`),
  createProduct: (data) => api.post('/admin-panel/products/', data, {
    headers: { 'Content-Type': 'multipart/form-data' }
  }),
  updateProduct: (id, data) => api.patch(`/admin-panel/products/${id}/`, data, {
    headers: { 'Content-Type': 'multipart/form-data' }
  }),
  deleteProduct: (id) => api.delete(`/admin-panel/products/${id}/`),
  addProductImage: (id, data) => api.post(`/admin-panel/products/${id}/images/`, data, {
    headers: { 'Content-Type': 'multipart/form-data' }
  }),
  deleteProductImage: (id, imgId) => api.delete(`/admin-panel/products/${id}/images/${imgId}/`),
  setProductMainImage: (id, imgId) => api.put(`/admin-panel/products/${id}/images/${imgId}/set_main/`),
  addProductColor: (id, data) => api.post(`/admin-panel/products/${id}/colors/`, data),
  deleteProductColor: (id, colorId) => api.delete(`/admin-panel/products/${id}/colors/${colorId}/`),

  // Orders
  getOrders: (params = {}) => api.get('/admin-panel/orders/', { params }),
  getOrder: (id) => api.get(`/admin-panel/orders/${id}/`),
  updateOrderStatus: (id, data) => api.put(`/admin-panel/orders/${id}/status/`, data),

  // Customers
  getCustomers: (params = {}) => api.get('/admin-panel/customers/', { params }),

  // Reports
  getReports: (params = {}) => api.get('/admin-panel/reports/', { params }),
  exportReports: (params = {}) => api.get('/admin-panel/reports/export/', {
    params,
    responseType: 'blob',
  }),

  // Site settings
  getSiteSettings: () => api.get('/admin-panel/site-settings/'),
  updateSiteSettings: (id, data) => api.patch(`/admin-panel/site-settings/${id}/`, data),

  // Banners
  getBanners: () => api.get('/admin-panel/banners/'),
  createBanner: (data) => api.post('/admin-panel/banners/', data, {
    headers: { 'Content-Type': 'multipart/form-data' }
  }),
  updateBanner: (id, data) => api.patch(`/admin-panel/banners/${id}/`, data),
  deleteBanner: (id) => api.delete(`/admin-panel/banners/${id}/`),
}
