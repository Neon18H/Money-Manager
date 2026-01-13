from django.conf import settings
from django.db import models


class Category(models.Model):
    class Kind(models.TextChoices):
        INCOME = "INCOME", "Ingreso"
        FIXED = "FIXED", "Gasto fijo"
        VARIABLE = "VARIABLE", "Gasto variable"
        SAVING = "SAVING", "Ahorro"

    name = models.CharField(max_length=100)
    kind = models.CharField(max_length=20, choices=Kind.choices)

    def __str__(self) -> str:
        return f"{self.name} ({self.get_kind_display()})"


class PaymentMethod(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self) -> str:
        return self.name


class TransactionBase(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    date = models.DateField()
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    category = models.ForeignKey(Category, on_delete=models.PROTECT)
    description = models.CharField(max_length=255)
    payment_method = models.ForeignKey(PaymentMethod, on_delete=models.PROTECT)
    notes = models.TextField(blank=True)

    class Meta:
        abstract = True
        ordering = ["-date", "-id"]


class Income(TransactionBase):
    source = models.CharField(max_length=100)

    def __str__(self) -> str:
        return f"{self.source} - {self.amount}"


class FixedExpense(TransactionBase):
    is_paid = models.BooleanField(default=False)
    due_day = models.IntegerField(null=True, blank=True)

    def __str__(self) -> str:
        return f"{self.description} - {self.amount}"


class VariableExpense(TransactionBase):
    class ExpenseType(models.TextChoices):
        NECESARIO = "NECESARIO", "Necesario"
        GUSTO = "GUSTO", "Gusto"

    expense_type = models.CharField(max_length=20, choices=ExpenseType.choices)

    def __str__(self) -> str:
        return f"{self.description} - {self.amount}"


class Saving(TransactionBase):
    class SavingType(models.TextChoices):
        AHORRO = "AHORRO", "Ahorro"
        INVERSION = "INVERSION", "Inversión"
        FONDO = "FONDO", "Fondo"

    saving_type = models.CharField(max_length=20, choices=SavingType.choices)
    goal_name = models.CharField(max_length=100, blank=True)
    goal_amount = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)

    def __str__(self) -> str:
        return f"{self.saving_type} - {self.amount}"
