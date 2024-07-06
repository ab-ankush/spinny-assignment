from django.db import models
from django.contrib.auth.models import User
import uuid

from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    password_set = models.BooleanField(default=False)

    def save(self, *args, **kwargs):
        if not self.password_set and self.password:
            self.set_password(self.password)
            self.password_set = True
        super().save(*args, **kwargs)

    def __str__(self):
        return self.username


class Box(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    length = models.DecimalField(max_digits=10, decimal_places=2)
    breadth = models.DecimalField(max_digits=10, decimal_places=2)
    height = models.DecimalField(max_digits=10, decimal_places=2)
    area = models.DecimalField(max_digits=10, decimal_places=2, editable=False)
    volume = models.DecimalField(
        max_digits=10, decimal_places=2, editable=False)
    created_at = models.DateTimeField(
        auto_now_add=True, editable=False, blank=True, null=True)
    updated_at = models.DateTimeField(auto_now=True)
    creator = models.ForeignKey(
        User, on_delete=models.CASCADE, editable=False, related_name='creator', blank=True, null=True)
    last_modified_by = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='last_modified_by', blank=True, null=True)

    def __str__(self):
        return f"Box {self.id}"

    def save(self, *args, **kwargs):
        self.area = self.length * self.breadth
        self.volume = self.length * self.breadth * self.height
        super().save(*args, **kwargs)
