from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name="Category",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("name", models.CharField(max_length=100)),
                (
                    "kind",
                    models.CharField(
                        choices=[
                            ("INCOME", "Ingreso"),
                            ("FIXED", "Gasto fijo"),
                            ("VARIABLE", "Gasto variable"),
                            ("SAVING", "Ahorro"),
                        ],
                        max_length=20,
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="PaymentMethod",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("name", models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name="Income",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("date", models.DateField()),
                ("amount", models.DecimalField(decimal_places=2, max_digits=12)),
                ("description", models.CharField(max_length=255)),
                ("notes", models.TextField(blank=True)),
                ("source", models.CharField(max_length=100)),
                (
                    "category",
                    models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to="finance.category"),
                ),
                (
                    "payment_method",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.PROTECT, to="finance.paymentmethod"
                    ),
                ),
                (
                    "user",
                    models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
                ),
            ],
            options={
                "ordering": ["-date", "-id"],
            },
        ),
        migrations.CreateModel(
            name="FixedExpense",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("date", models.DateField()),
                ("amount", models.DecimalField(decimal_places=2, max_digits=12)),
                ("description", models.CharField(max_length=255)),
                ("notes", models.TextField(blank=True)),
                ("is_paid", models.BooleanField(default=False)),
                ("due_day", models.IntegerField(blank=True, null=True)),
                (
                    "category",
                    models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to="finance.category"),
                ),
                (
                    "payment_method",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.PROTECT, to="finance.paymentmethod"
                    ),
                ),
                (
                    "user",
                    models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
                ),
            ],
            options={
                "ordering": ["-date", "-id"],
            },
        ),
        migrations.CreateModel(
            name="VariableExpense",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("date", models.DateField()),
                ("amount", models.DecimalField(decimal_places=2, max_digits=12)),
                ("description", models.CharField(max_length=255)),
                ("notes", models.TextField(blank=True)),
                (
                    "expense_type",
                    models.CharField(choices=[("NECESARIO", "Necesario"), ("GUSTO", "Gusto")], max_length=20),
                ),
                (
                    "category",
                    models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to="finance.category"),
                ),
                (
                    "payment_method",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.PROTECT, to="finance.paymentmethod"
                    ),
                ),
                (
                    "user",
                    models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
                ),
            ],
            options={
                "ordering": ["-date", "-id"],
            },
        ),
        migrations.CreateModel(
            name="Saving",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("date", models.DateField()),
                ("amount", models.DecimalField(decimal_places=2, max_digits=12)),
                ("description", models.CharField(max_length=255)),
                ("notes", models.TextField(blank=True)),
                (
                    "saving_type",
                    models.CharField(
                        choices=[("AHORRO", "Ahorro"), ("INVERSION", "Inversión"), ("FONDO", "Fondo")],
                        max_length=20,
                    ),
                ),
                ("goal_name", models.CharField(blank=True, max_length=100)),
                ("goal_amount", models.DecimalField(blank=True, decimal_places=2, max_digits=12, null=True)),
                (
                    "category",
                    models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to="finance.category"),
                ),
                (
                    "payment_method",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.PROTECT, to="finance.paymentmethod"
                    ),
                ),
                (
                    "user",
                    models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
                ),
            ],
            options={
                "ordering": ["-date", "-id"],
            },
        ),
    ]
