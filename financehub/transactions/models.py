from django.db import models
from django.contrib.auth import get_user_model
from config.models import Category, PaymentMethod

User = get_user_model()


class TransactionBase(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateField()
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True)
    description = models.CharField(max_length=255)
    payment_method = models.ForeignKey(PaymentMethod, on_delete=models.SET_NULL, null=True, blank=True)
    notes = models.TextField(blank=True)

    class Meta:
        abstract = True
        ordering = ['-date']


class Income(TransactionBase):
    source = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.source} - {self.amount}"


class FixedExpense(TransactionBase):
    is_paid = models.BooleanField(default=False)
    due_day = models.PositiveIntegerField(null=True, blank=True)

    def __str__(self):
        return f"{self.description} - {self.amount}"


class VariableExpense(TransactionBase):
    class ExpenseType(models.TextChoices):
        NECESARIO = 'NECESARIO', 'Necesario'
        GUSTO = 'GUSTO', 'Gusto'

    expense_type = models.CharField(max_length=20, choices=ExpenseType.choices)

    def __str__(self):
        return f"{self.description} - {self.amount}"


class Saving(TransactionBase):
    class SavingType(models.TextChoices):
        AHORRO = 'AHORRO', 'Ahorro'
        INVERSION = 'INVERSION', 'Inversión'
        FONDO = 'FONDO', 'Fondo'

    saving_type = models.CharField(max_length=20, choices=SavingType.choices)
    goal_name = models.CharField(max_length=120, blank=True)
    goal_amount = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)

    def __str__(self):
        return f"{self.description} - {self.amount}"
