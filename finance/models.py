from django.conf import settings
from django.db import models


class Category(models.Model):
    KIND_INCOME = "INCOME"
    KIND_FIXED = "FIXED"
    KIND_VARIABLE = "VARIABLE"
    KIND_SAVING = "SAVING"

    KIND_CHOICES = [
        (KIND_INCOME, "Ingreso"),
        (KIND_FIXED, "Gasto Fijo"),
        (KIND_VARIABLE, "Gasto Variable"),
        (KIND_SAVING, "Ahorro"),
    ]

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    kind = models.CharField(max_length=20, choices=KIND_CHOICES)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ["name"]
        constraints = [
            models.UniqueConstraint(fields=["user", "name", "kind"], name="unique_category_per_user_kind"),
        ]

    def __str__(self) -> str:
        return self.name


class PaymentMethod(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ["name"]
        constraints = [
            models.UniqueConstraint(fields=["user", "name"], name="unique_payment_method_per_user"),
        ]

    def __str__(self) -> str:
        return self.name


class BaseTransaction(models.Model):
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


class Income(BaseTransaction):
    source = models.CharField(max_length=100)

    def __str__(self) -> str:
        return f"{self.description} - {self.amount}"

    def get_update_url(self):
        return f"/ingresos/{self.pk}/editar/"

    def get_delete_url(self):
        return f"/ingresos/{self.pk}/eliminar/"


class FixedExpense(BaseTransaction):
    is_paid = models.BooleanField(default=False)
    due_day = models.IntegerField(null=True, blank=True)

    def __str__(self) -> str:
        return f"{self.description} - {self.amount}"

    def get_update_url(self):
        return f"/gastos-fijos/{self.pk}/editar/"

    def get_delete_url(self):
        return f"/gastos-fijos/{self.pk}/eliminar/"


class VariableExpense(BaseTransaction):
    TYPE_NECESSARY = "NECESARIO"
    TYPE_WANT = "GUSTO"

    TYPE_CHOICES = [
        (TYPE_NECESSARY, "Necesario"),
        (TYPE_WANT, "Gusto"),
    ]

    expense_type = models.CharField(max_length=20, choices=TYPE_CHOICES)

    def __str__(self) -> str:
        return f"{self.description} - {self.amount}"

    def get_update_url(self):
        return f"/gastos-variables/{self.pk}/editar/"

    def get_delete_url(self):
        return f"/gastos-variables/{self.pk}/eliminar/"


class Saving(BaseTransaction):
    SAVING_TYPE_AHORRO = "AHORRO"
    SAVING_TYPE_INVERSION = "INVERSION"
    SAVING_TYPE_FONDO = "FONDO"

    SAVING_TYPE_CHOICES = [
        (SAVING_TYPE_AHORRO, "Ahorro"),
        (SAVING_TYPE_INVERSION, "Inversión"),
        (SAVING_TYPE_FONDO, "Fondo"),
    ]

    saving_type = models.CharField(max_length=20, choices=SAVING_TYPE_CHOICES)
    goal = models.ForeignKey("SavingGoal", on_delete=models.SET_NULL, null=True, blank=True, related_name="savings")
    goal_name = models.CharField(max_length=150, blank=True)
    goal_amount = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)

    def __str__(self) -> str:
        return f"{self.description} - {self.amount}"

    def get_update_url(self):
        return f"/ahorros/{self.pk}/editar/"

    def get_delete_url(self):
        return f"/ahorros/{self.pk}/eliminar/"


class SavingGoal(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    name = models.CharField(max_length=150)
    target_amount = models.DecimalField(max_digits=12, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ["-created_at"]
        constraints = [
            models.UniqueConstraint(fields=["user", "name"], name="unique_saving_goal_per_user"),
        ]

    def __str__(self) -> str:
        return self.name

    def get_update_url(self):
        return f"/ahorros/metas/{self.pk}/editar/"

    def get_delete_url(self):
        return f"/ahorros/metas/{self.pk}/eliminar/"
