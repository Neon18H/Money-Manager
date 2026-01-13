from django.contrib import admin
from .models import Category, PaymentMethod


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'kind', 'user')
    list_filter = ('kind',)
    search_fields = ('name', 'user__username')


@admin.register(PaymentMethod)
class PaymentMethodAdmin(admin.ModelAdmin):
    list_display = ('name', 'user')
    search_fields = ('name', 'user__username')
