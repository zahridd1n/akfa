import api from './axios'

export const siteApi = {
  getSettings: ()           => api.get('/site-settings/'),
  getAbout: ()              => api.get('/about/'),
  submitContact: (data)     => api.post('/contact/', data),

  // Admin
  updateSettings: (data)    => api.patch('/admin-panel/site-settings/', data),
  updateAbout: (data)       => api.patch('/admin-panel/about/', data),
  getContacts: (params = {}) => api.get('/admin-panel/contacts/', { params }),
  markRead: (id, isRead)    => api.patch(`/admin-panel/contacts/${id}/`, { is_read: isRead }),
  deleteContact: (id)       => api.delete(`/admin-panel/contacts/${id}/`),
}
