import api from './axios'

export const addressApi = {
  getAddresses: () => api.get('/addresses/'),
  createAddress: (data) => api.post('/addresses/', data),
  getAddress: (id) => api.get(`/addresses/${id}/`),
  updateAddress: (id, data) => api.patch(`/addresses/${id}/`, data),
  deleteAddress: (id) => api.delete(`/addresses/${id}/`),
  setDefault: (id) => api.post(`/addresses/${id}/set_default/`),
}
