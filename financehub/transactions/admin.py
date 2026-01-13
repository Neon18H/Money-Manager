from django.contrib import admin
from .models import Income, FixedExpense, VariableExpense, Saving


@admin.register(Income)
class IncomeAdmin(admin.ModelAdmin):
    list_display = ('source', 'amount', 'date', 'user')
    list_filter = ('date',)
    search_fields = ('source', 'description', 'user__username')


@admin.register(FixedExpense)
class FixedExpenseAdmin(admin.ModelAdmin):
    list_display = ('description', 'amount', 'date', 'is_paid', 'user')
    list_filter = ('date', 'is_paid')
    search_fields = ('description', 'user__username')


@admin.register(VariableExpense)
class VariableExpenseAdmin(admin.ModelAdmin):
    list_display = ('description', 'amount', 'date', 'expense_type', 'user')
    list_filter = ('date', 'expense_type')
    search_fields = ('description', 'user__username')


@admin.register(Saving)
class SavingAdmin(admin.ModelAdmin):
    list_display = ('description', 'amount', 'date', 'saving_type', 'user')
    list_filter = ('date', 'saving_type')
    search_fields = ('description', 'user__username')
