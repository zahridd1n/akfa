from rest_framework.permissions import BasePermission


class IsAdminUser(BasePermission):
    """Faqat admin roli uchun"""
    message = "Bu amalni faqat adminlar bajarishi mumkin."

    def has_permission(self, request, view):
        return bool(
            request.user and
            request.user.is_authenticated and
            request.user.role == "admin"
        )


class IsClientUser(BasePermission):
    """Faqat client roli uchun"""
    message = "Bu amalni faqat mijozlar bajarishi mumkin."

    def has_permission(self, request, view):
        return bool(
            request.user and
            request.user.is_authenticated and
            request.user.role == "client"
        )


class IsOwnerOrAdmin(BasePermission):
    """Resurs egasi yoki admin"""
    def has_object_permission(self, request, view, obj):
        if not request.user or not request.user.is_authenticated:
            return False
        if request.user.role == "admin":
            return True
        # obj.user, obj.cart.user kabi fieldlar
        owner = getattr(obj, "user", None)
        if owner is None:
            owner = getattr(getattr(obj, "cart", None), "user", None)
        return owner == request.user
