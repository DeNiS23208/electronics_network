from __future__ import annotations
from django.db import models
from django.core.exceptions import ValidationError


class Product(models.Model):
    name = models.CharField(max_length=255)
    model = models.CharField(max_length=255)
    release_date = models.DateField()

    class Meta:
        ordering = ["-release_date", "name"]
        unique_together = ("name", "model")

    def __str__(self):
        return f"{self.name} ({self.model})"


class NetworkNode(models.Model):
    name = models.CharField(max_length=255)

    email = models.EmailField()
    country = models.CharField(max_length=100)
    city = models.CharField(max_length=100)
    street = models.CharField(max_length=100)
    house_number = models.CharField(max_length=20)

    products = models.ManyToManyField(Product, blank=True, related_name="nodes")

    supplier = models.ForeignKey(
        "self",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="children",
        help_text="Поставщик (предыдущее по иерархии звено)",
    )

    debt = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["name"]
        verbose_name = "Звено сети"
        verbose_name_plural = "Звенья сети"

    def __str__(self):
        return f"{self.name} — {self.city}, {self.country}"

    @property
    def level(self) -> int:
        lvl, cur = 0, self.supplier
        while cur:
            lvl += 1
            cur = cur.supplier
        return lvl

    def clean(self):
        # глубина максимум 3 уровня (0,1,2)
        if self.supplier and self.supplier.level >= 2:
            raise ValidationError("Глубина иерархии не может превышать 3 уровня.")
        # запрет циклов
        seen = {self.pk}
        cur = self.supplier
        while cur:
            if cur.pk in seen:
                raise ValidationError("Обнаружен цикл в иерархии поставщиков.")
            seen.add(cur.pk)
            cur = cur.supplier

    def save(self, *args, **kwargs):
        self.full_clean()
        return super().save(*args, **kwargs)
