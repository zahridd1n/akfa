from django.db import models


class ContactMessage(models.Model):
    """Foydalanuvchilardan kelgan murojatlar."""
    name    = models.CharField(max_length=150, verbose_name="Ism")
    phone   = models.CharField(max_length=30, verbose_name="Telefon")
    message = models.TextField(blank=True, default="", verbose_name="Xabar")
    is_read = models.BooleanField(default=False, verbose_name="O'qildi")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Sana")

    class Meta:
        verbose_name = "Murojat"
        verbose_name_plural = "Murojatlar"
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.name} — {self.phone}"
