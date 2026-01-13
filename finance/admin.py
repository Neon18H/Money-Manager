from django.contrib import admin

from .models import Category, FixedExpense, Income, PaymentMethod, Saving, VariableExpense


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("name", "kind")
    list_filter = ("kind",)
    search_fields = ("name",)


@admin.register(PaymentMethod)
class PaymentMethodAdmin(admin.ModelAdmin):
    list_display = ("name",)
    search_fields = ("name",)


@admin.register(Income)
class IncomeAdmin(admin.ModelAdmin):
    list_display = ("source", "amount", "date", "user")
    list_filter = ("date",)
    search_fields = ("source", "description")


@admin.register(FixedExpense)
class FixedExpenseAdmin(admin.ModelAdmin):
    list_display = ("description", "amount", "date", "is_paid", "user")
    list_filter = ("date", "is_paid")
    search_fields = ("description",)


@admin.register(VariableExpense)
class VariableExpenseAdmin(admin.ModelAdmin):
    list_display = ("description", "amount", "date", "expense_type", "user")
    list_filter = ("date", "expense_type")
    search_fields = ("description",)


@admin.register(Saving)
class SavingAdmin(admin.ModelAdmin):
    list_display = ("saving_type", "amount", "date", "user")
    list_filter = ("date", "saving_type")
    search_fields = ("description", "goal_name")
