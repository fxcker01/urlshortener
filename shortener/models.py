from django.db import models
from django.contrib.auth.models import User

class ShortURL(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)  # ← ось тут
    original_url = models.URLField()
    short_code = models.CharField(max_length=10, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.short_code} > {self.original_url}"