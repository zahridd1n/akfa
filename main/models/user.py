import re
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin


def normalize_phone(phone: str) -> str:
    """Telefon raqamni tozalash va standart +998XXXXXXXXX formatga keltirish"""
    if not phone:
        return ""
    cleaned = re.sub(r"[\s\-\(\)\.]", "", str(phone).strip())
    if cleaned.startswith("998") and not cleaned.startswith("+"):
        cleaned = "+" + cleaned
    elif len(cleaned) == 9 and not cleaned.startswith("+"):
        cleaned = "+998" + cleaned
    return cleaned


def validate_phone(phone: str) -> bool:
    """O'zbek telefon raqami validatsiyasi: +998XXXXXXXXX"""
    phone = normalize_phone(phone)
    return bool(re.match(r"^\+998[0-9]{9}$", phone))


class CustomUserManager(BaseUserManager):
    def create_user(self, phone_number, password=None, **extra_fields):
        if not phone_number:
            raise ValueError("Telefon raqam kiritilishi shart")
        phone_number = normalize_phone(phone_number)
        if not validate_phone(phone_number):
            raise ValueError("Noto'g'ri telefon raqam formati (+998XXXXXXXXX)")
        user = self.model(phone_number=phone_number, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, phone_number, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("role", CustomUser.Role.ADMIN)
        return self.create_user(phone_number, password, **extra_fields)


class CustomUser(AbstractBaseUser, PermissionsMixin):
    class Role(models.TextChoices):
        CLIENT = "client", "Mijoz"
        ADMIN = "admin", "Admin"

    phone_number = models.CharField(
        max_length=13,
        unique=True,
        verbose_name="Telefon raqam",
        help_text="+998XXXXXXXXX formatida",
    )
    full_name = models.CharField(max_length=150, blank=True, verbose_name="To'liq ism")
    role = models.CharField(
        max_length=10,
        choices=Role.choices,
        default=Role.CLIENT,
        verbose_name="Rol",
    )
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = CustomUserManager()

    USERNAME_FIELD = "phone_number"
    REQUIRED_FIELDS = ["full_name"]

    class Meta:
        verbose_name = "Foydalanuvchi"
        verbose_name_plural = "Foydalanuvchilar"
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.full_name} ({self.phone_number})"

    @property
    def is_admin(self):
        return self.role == self.Role.ADMIN
