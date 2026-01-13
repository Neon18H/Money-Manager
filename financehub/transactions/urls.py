from django.urls import path
from . import views

urlpatterns = [
    path('incomes/', views.IncomeListView.as_view(), name='income_list'),
    path('incomes/new/', views.IncomeCreateView.as_view(), name='income_create'),
    path('incomes/<int:pk>/edit/', views.IncomeUpdateView.as_view(), name='income_update'),
    path('incomes/<int:pk>/delete/', views.IncomeDeleteView.as_view(), name='income_delete'),
    path('fixed-expenses/', views.FixedExpenseListView.as_view(), name='fixed_expense_list'),
    path('fixed-expenses/new/', views.FixedExpenseCreateView.as_view(), name='fixed_expense_create'),
    path('fixed-expenses/<int:pk>/edit/', views.FixedExpenseUpdateView.as_view(), name='fixed_expense_update'),
    path('fixed-expenses/<int:pk>/delete/', views.FixedExpenseDeleteView.as_view(), name='fixed_expense_delete'),
    path('variable-expenses/', views.VariableExpenseListView.as_view(), name='variable_expense_list'),
    path('variable-expenses/new/', views.VariableExpenseCreateView.as_view(), name='variable_expense_create'),
    path('variable-expenses/<int:pk>/edit/', views.VariableExpenseUpdateView.as_view(), name='variable_expense_update'),
    path('variable-expenses/<int:pk>/delete/', views.VariableExpenseDeleteView.as_view(), name='variable_expense_delete'),
    path('savings/', views.SavingListView.as_view(), name='saving_list'),
    path('savings/new/', views.SavingCreateView.as_view(), name='saving_create'),
    path('savings/<int:pk>/edit/', views.SavingUpdateView.as_view(), name='saving_update'),
    path('savings/<int:pk>/delete/', views.SavingDeleteView.as_view(), name='saving_delete'),
]
