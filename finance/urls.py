from django.urls import path
from django.views.generic import RedirectView

from finance import views

urlpatterns = [
    path("", RedirectView.as_view(pattern_name="dashboard_general", permanent=False)),
    path("dashboards/general/", views.dashboard, name="dashboard_general"),
    path("dashboards/incomes/", views.income_dashboard, name="income_dashboard"),
    path("dashboards/fixed-expenses/", views.fixed_expense_dashboard, name="fixed_expense_dashboard"),
    path("dashboards/variable-expenses/", views.variable_expense_dashboard, name="variable_expense_dashboard"),
    path("dashboards/savings/", views.saving_dashboard, name="saving_dashboard"),
    path("ingresos/", views.IncomeListView.as_view(), name="income_list"),
    path("ingresos/nuevo/", views.IncomeCreateView.as_view(), name="income_create"),
    path("ingresos/<int:pk>/editar/", views.IncomeUpdateView.as_view(), name="income_update"),
    path("ingresos/<int:pk>/eliminar/", views.IncomeDeleteView.as_view(), name="income_delete"),
    path("gastos-fijos/", views.FixedExpenseListView.as_view(), name="fixed_expense_list"),
    path("gastos-fijos/nuevo/", views.FixedExpenseCreateView.as_view(), name="fixed_expense_create"),
    path("gastos-fijos/<int:pk>/editar/", views.FixedExpenseUpdateView.as_view(), name="fixed_expense_update"),
    path("gastos-fijos/<int:pk>/eliminar/", views.FixedExpenseDeleteView.as_view(), name="fixed_expense_delete"),
    path("gastos-variables/", views.VariableExpenseListView.as_view(), name="variable_expense_list"),
    path("gastos-variables/nuevo/", views.VariableExpenseCreateView.as_view(), name="variable_expense_create"),
    path("gastos-variables/<int:pk>/editar/", views.VariableExpenseUpdateView.as_view(), name="variable_expense_update"),
    path("gastos-variables/<int:pk>/eliminar/", views.VariableExpenseDeleteView.as_view(), name="variable_expense_delete"),
    path("ahorros/", views.SavingListView.as_view(), name="saving_list"),
    path("ahorros/nuevo/", views.SavingCreateView.as_view(), name="saving_create"),
    path("ahorros/<int:pk>/editar/", views.SavingUpdateView.as_view(), name="saving_update"),
    path("ahorros/<int:pk>/eliminar/", views.SavingDeleteView.as_view(), name="saving_delete"),
    path("settings/", views.settings_home, name="settings_home"),
    path("settings/categories/", views.CategoryListView.as_view(), name="settings_categories"),
    path("settings/categories/nuevo/", views.CategoryCreateView.as_view(), name="settings_category_create"),
    path("settings/categories/<int:pk>/editar/", views.CategoryUpdateView.as_view(), name="settings_category_update"),
    path("settings/categories/<int:pk>/eliminar/", views.CategoryDeleteView.as_view(), name="settings_category_delete"),
    path("settings/payment-methods/", views.PaymentMethodListView.as_view(), name="settings_payment_methods"),
    path("settings/payment-methods/nuevo/", views.PaymentMethodCreateView.as_view(), name="settings_payment_method_create"),
    path(
        "settings/payment-methods/<int:pk>/editar/",
        views.PaymentMethodUpdateView.as_view(),
        name="settings_payment_method_update",
    ),
    path(
        "settings/payment-methods/<int:pk>/eliminar/",
        views.PaymentMethodDeleteView.as_view(),
        name="settings_payment_method_delete",
    ),
]
