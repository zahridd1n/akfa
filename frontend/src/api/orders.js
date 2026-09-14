import api from './axios'

export const ordersApi = {
  getOrders: () => api.get('/orders/'),
  createOrder: (data) => api.post('/orders/', data),
  getOrder: (orderNumber) => api.get(`/orders/${orderNumber}/`),
  cancelOrder: (orderNumber) => api.post(`/orders/${orderNumber}/cancel/`),
}
