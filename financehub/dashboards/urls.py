from django.urls import path
from . import views

app_name = 'dashboards'

urlpatterns = [
    path('general/', views.general_dashboard, name='general'),
    path('incomes/', views.income_dashboard, name='incomes'),
    path('fixed-expenses/', views.fixed_expense_dashboard, name='fixed_expenses'),
    path('variable-expenses/', views.variable_expense_dashboard, name='variable_expenses'),
    path('savings/', views.saving_dashboard, name='savings'),
]
