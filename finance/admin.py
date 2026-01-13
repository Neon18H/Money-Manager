from django.contrib import admin

from finance.models import Category, FixedExpense, Income, PaymentMethod, Saving, SavingGoal, VariableExpense


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("name", "kind", "user")
    list_filter = ("kind",)
    search_fields = ("name",)


@admin.register(PaymentMethod)
class PaymentMethodAdmin(admin.ModelAdmin):
    list_display = ("name", "user")
    search_fields = ("name",)


@admin.register(Income)
class IncomeAdmin(admin.ModelAdmin):
    list_display = ("date", "description", "amount", "source", "user")
    list_filter = ("date",)
    search_fields = ("description", "source")


@admin.register(FixedExpense)
class FixedExpenseAdmin(admin.ModelAdmin):
    list_display = ("date", "description", "amount", "is_paid", "due_day", "user")
    list_filter = ("is_paid", "date")
    search_fields = ("description",)


@admin.register(VariableExpense)
class VariableExpenseAdmin(admin.ModelAdmin):
    list_display = ("date", "description", "amount", "expense_type", "user")
    list_filter = ("expense_type", "date")
    search_fields = ("description",)


@admin.register(Saving)
class SavingAdmin(admin.ModelAdmin):
    list_display = ("date", "description", "amount", "saving_type", "goal", "user")
    list_filter = ("saving_type", "date")
    search_fields = ("description",)


@admin.register(SavingGoal)
class SavingGoalAdmin(admin.ModelAdmin):
    list_display = ("name", "target_amount", "is_active", "user", "created_at")
    list_filter = ("is_active", "created_at")
    search_fields = ("name",)
