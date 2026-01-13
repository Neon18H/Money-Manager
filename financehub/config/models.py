from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


class Category(models.Model):
    class Kind(models.TextChoices):
        INCOME = 'INCOME', 'Ingreso'
        FIXED = 'FIXED', 'Gasto fijo'
        VARIABLE = 'VARIABLE', 'Gasto variable'
        SAVING = 'SAVING', 'Ahorro'

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    kind = models.CharField(max_length=20, choices=Kind.choices)

    class Meta:
        unique_together = ('user', 'name', 'kind')
        ordering = ['name']

    def __str__(self):
        return f"{self.name} ({self.get_kind_display()})"


class PaymentMethod(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)

    class Meta:
        unique_together = ('user', 'name')
        ordering = ['name']

    def __str__(self):
        return self.name
