import { createRouter, createWebHistory } from 'vue-router'

// Lazy-load client pages
const HomeView       = () => import('@/views/client/HomeView.vue')
const CatalogView    = () => import('@/views/client/CatalogView.vue')
const ProductDetail  = () => import('@/views/client/ProductDetailView.vue')
const CartView       = () => import('@/views/client/CartView.vue')
const CheckoutView   = () => import('@/views/client/CheckoutView.vue')
const ProfileView    = () => import('@/views/client/ProfileView.vue')
const ContactView    = () => import('@/views/client/ContactView.vue')
const AboutView      = () => import('@/views/client/AboutView.vue')

// Lazy-load admin pages
const AdminDashboard   = () => import('@/views/admin/DashboardView.vue')
const AdminProducts    = () => import('@/views/admin/ProductsView.vue')
const AdminProductForm = () => import('@/views/admin/ProductFormView.vue')
const AdminOrders      = () => import('@/views/admin/OrdersView.vue')
const AdminCustomers   = () => import('@/views/admin/CustomersView.vue')
const AdminReports     = () => import('@/views/admin/ReportsView.vue')
const AdminContacts    = () => import('@/views/admin/ContactsView.vue')

// Layouts
const ClientLayout = () => import('@/layouts/ClientLayout.vue')
const AdminLayout  = () => import('@/layouts/AdminLayout.vue')

const routes = [
  {
    path: '/',
    component: ClientLayout,
    children: [
      { path: '',         name: 'home',       component: HomeView },
      { path: 'catalog',  name: 'catalog',    component: CatalogView },
      { path: 'product/:slug', name: 'product', component: ProductDetail },
      { path: 'cart',     name: 'cart',       component: CartView, meta: { requiresAuth: true } },
      { path: 'checkout', name: 'checkout',   component: CheckoutView, meta: { requiresAuth: true } },
      { path: 'profile',  name: 'profile',    component: ProfileView, meta: { requiresAuth: true } },
      { path: 'contact',  name: 'contact',    component: ContactView },
      { path: 'about',    name: 'about',      component: AboutView },
    ]
  },
  {
    path: '/admin',
    component: AdminLayout,
    meta: { requiresAuth: true, requiresAdmin: true },
    children: [
      { path: '',           redirect: '/admin/dashboard' },
      { path: 'dashboard',  name: 'admin-dashboard',      component: AdminDashboard },
      { path: 'products',   name: 'admin-products',        component: AdminProducts },
      { path: 'products/new',  name: 'admin-product-new', component: AdminProductForm },
      { path: 'products/:id',  name: 'admin-product-edit',component: AdminProductForm },
      { path: 'orders',     name: 'admin-orders',          component: AdminOrders },
      { path: 'customers',  name: 'admin-customers',       component: AdminCustomers },
      { path: 'reports',    name: 'admin-reports',         component: AdminReports },
      { path: 'contacts',   name: 'admin-contacts',        component: AdminContacts },
    ]
  },
  { path: '/:pathMatch(.*)*', redirect: '/' }
]

const router = createRouter({
  history: createWebHistory(),
  routes,
  scrollBehavior(to, from, savedPosition) {
    if (savedPosition) return savedPosition
    if (to.hash) return { el: to.hash, behavior: 'smooth' }
    return { top: 0, behavior: 'smooth' }
  },
})

// Navigation guard
router.beforeEach((to, from, next) => {
  const token = localStorage.getItem('token')
  const user = JSON.parse(localStorage.getItem('user') || 'null')

  if (to.meta.requiresAuth && !token) {
    window.dispatchEvent(new CustomEvent('auth:open-modal'))
    return next('/')
  }

  if (to.meta.requiresAdmin && user?.role !== 'admin') {
    return next('/')
  }

  next()
})

export default router
