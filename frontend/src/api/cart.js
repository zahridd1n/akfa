import api from './axios'

export const cartApi = {
  getCart: () => api.get('/cart/'),
  addItem: (data) => api.post('/cart/add/', data),
  updateItem: (id, data) => api.put(`/cart/items/${id}/`, data),
  removeItem: (id) => api.delete(`/cart/items/${id}/`),
  clearCart: () => api.delete('/cart/clear/'),
}
