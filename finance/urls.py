from django.urls import path

from . import views

app_name = "finance"

urlpatterns = [
    path("", views.dashboard_general, name="dashboard-general"),
    path("dashboard/ingresos/", views.dashboard_income, name="dashboard-income"),
    path("dashboard/gastos-fijos/", views.dashboard_fixed_expense, name="dashboard-fixed"),
    path("dashboard/gastos-variables/", views.dashboard_variable_expense, name="dashboard-variable"),
    path("dashboard/ahorros/", views.dashboard_saving, name="dashboard-saving"),
    path("export/general/", views.export_general_summary, name="export-general"),
    path("export/<str:module>/", views.export_module_summary, name="export-module"),
    path("ingresos/", views.IncomeListView.as_view(), name="income-list"),
    path("ingresos/nuevo/", views.IncomeCreateView.as_view(), name="income-create"),
    path("ingresos/<int:pk>/editar/", views.IncomeUpdateView.as_view(), name="income-update"),
    path("ingresos/<int:pk>/eliminar/", views.IncomeDeleteView.as_view(), name="income-delete"),
    path("gastos-fijos/", views.FixedExpenseListView.as_view(), name="fixed-expense-list"),
    path("gastos-fijos/nuevo/", views.FixedExpenseCreateView.as_view(), name="fixed-expense-create"),
    path(
        "gastos-fijos/<int:pk>/editar/",
        views.FixedExpenseUpdateView.as_view(),
        name="fixed-expense-update",
    ),
    path(
        "gastos-fijos/<int:pk>/eliminar/",
        views.FixedExpenseDeleteView.as_view(),
        name="fixed-expense-delete",
    ),
    path("gastos-variables/", views.VariableExpenseListView.as_view(), name="variable-expense-list"),
    path(
        "gastos-variables/nuevo/",
        views.VariableExpenseCreateView.as_view(),
        name="variable-expense-create",
    ),
    path(
        "gastos-variables/<int:pk>/editar/",
        views.VariableExpenseUpdateView.as_view(),
        name="variable-expense-update",
    ),
    path(
        "gastos-variables/<int:pk>/eliminar/",
        views.VariableExpenseDeleteView.as_view(),
        name="variable-expense-delete",
    ),
    path("ahorros/", views.SavingListView.as_view(), name="saving-list"),
    path("ahorros/nuevo/", views.SavingCreateView.as_view(), name="saving-create"),
    path("ahorros/<int:pk>/editar/", views.SavingUpdateView.as_view(), name="saving-update"),
    path("ahorros/<int:pk>/eliminar/", views.SavingDeleteView.as_view(), name="saving-delete"),
]
