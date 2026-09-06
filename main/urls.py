from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import auth, address, product, cart, order, admin_views, site_settings

router = DefaultRouter()
router.register(r'categories', product.CategoryViewSet, basename='category')
router.register(r'products', product.ProductViewSet, basename='product')
router.register(r'addresses', address.AddressViewSet, basename='address')

urlpatterns = [
    # Auth
    path('auth/register/', auth.register_view, name='auth-register'),
    path('auth/login/', auth.login_view, name='auth-login'),
    path('auth/logout/', auth.logout_view, name='auth-logout'),
    path('auth/profile/', auth.profile_view, name='auth-profile'),
    path('auth/change-password/', auth.change_password_view, name='auth-change-password'),
    # Kategoriya va Mahsulot
    path('', include(router.urls)),
    # Savat
    path('cart/', cart.cart_detail, name='cart-detail'),
    path('cart/add/', cart.cart_add, name='cart-add'),
    path('cart/items/<int:item_id>/', cart.cart_item_update, name='cart-item-update'),
    path('cart/items/<int:item_id>/delete/', cart.cart_item_delete, name='cart-item-delete'),
    path('cart/clear/', cart.cart_clear, name='cart-clear'),
    # Buyurtmalar
    path('orders/', order.orders_list_create, name='orders'),
    path('orders/<str:order_number>/', order.order_detail, name='order-detail'),
    path('orders/<str:order_number>/cancel/', order.order_cancel, name='order-cancel'),
    # Sayt sozlamalari (ommaviy)
    path('site-settings/', site_settings.site_settings_view, name='site-settings'),
    path('banners/', site_settings.banners_list, name='banners-list'),
    # Admin Panel
    path('admin-panel/dashboard/', admin_views.admin_dashboard, name='admin-dashboard'),
    path('admin-panel/products/', admin_views.admin_products_list, name='admin-products'),
    path('admin-panel/products/<int:product_id>/', admin_views.admin_product_detail, name='admin-product-detail'),
    path('admin-panel/products/<int:product_id>/images/', admin_views.admin_product_add_image, name='admin-product-add-image'),
    path('admin-panel/products/<int:product_id>/images/<int:image_id>/', admin_views.admin_product_delete_image, name='admin-product-delete-image'),
    path('admin-panel/products/<int:product_id>/colors/', admin_views.admin_product_add_color, name='admin-product-add-color'),
    path('admin-panel/products/<int:product_id>/colors/<int:color_id>/', admin_views.admin_product_color_detail, name='admin-product-color-detail'),
    path('admin-panel/orders/', admin_views.admin_orders_list, name='admin-orders'),
    path('admin-panel/orders/<int:order_id>/status/', admin_views.admin_order_status, name='admin-order-status'),
    path('admin-panel/customers/', admin_views.admin_customers_list, name='admin-customers'),
    # Admin: Sayt sozlamalari
    path('admin-panel/site-settings/', site_settings.admin_site_settings_update, name='admin-site-settings'),
    path('admin-panel/banners/', site_settings.admin_banner_create, name='admin-banner-create'),
    path('admin-panel/banners/<int:banner_id>/', site_settings.admin_banner_detail, name='admin-banner-detail'),
]
