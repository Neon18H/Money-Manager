import csv
import json
from decimal import Decimal

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q, Sum
from django.http import HttpResponse
from django.shortcuts import render
from django.urls import reverse_lazy
from django.utils import timezone
from django.views.generic import CreateView, DeleteView, ListView, UpdateView

from .forms import FixedExpenseForm, IncomeForm, SavingForm, VariableExpenseForm
from .models import FixedExpense, Income, Saving, VariableExpense
from .services import (
    calculate_delta,
    get_category_breakdown,
    get_daily_series,
    get_last_12_months_series,
    get_month_kpis,
    get_previous_month,
)

MONTH_CHOICES = [
    (1, "Enero"),
    (2, "Febrero"),
    (3, "Marzo"),
    (4, "Abril"),
    (5, "Mayo"),
    (6, "Junio"),
    (7, "Julio"),
    (8, "Agosto"),
    (9, "Septiembre"),
    (10, "Octubre"),
    (11, "Noviembre"),
    (12, "Diciembre"),
]


def get_year_month(request):
    today = timezone.localdate()
    year = int(request.GET.get("year", today.year))
    month = int(request.GET.get("month", today.month))
    return year, month


def build_year_options():
    current_year = timezone.localdate().year
    return [current_year - 1, current_year, current_year + 1]


class UserFilteredQuerysetMixin(LoginRequiredMixin):
    def get_queryset(self):
        return super().get_queryset().filter(user=self.request.user)

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)


class SearchableListView(UserFilteredQuerysetMixin, ListView):
    paginate_by = 10
    search_fields: list[str] = []

    def get_queryset(self):
        queryset = super().get_queryset()
        query = self.request.GET.get("q")
        if query and self.search_fields:
            filters = Q()
            for field in self.search_fields:
                filters |= Q(**{f"{field}__icontains": query})
            queryset = queryset.filter(filters)
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["query"] = self.request.GET.get("q", "")
        return context


class IncomeListView(SearchableListView):
    model = Income
    template_name = "finance/income_list.html"
    search_fields = ["source", "description", "category__name"]
    extra_context = {"page_title": "Ingresos"}


class IncomeCreateView(UserFilteredQuerysetMixin, CreateView):
    model = Income
    form_class = IncomeForm
    template_name = "finance/income_form.html"
    success_url = reverse_lazy("finance:income-list")
    extra_context = {"page_title": "Nuevo ingreso"}

    def form_valid(self, form):
        messages.success(self.request, "Ingreso creado correctamente.")
        return super().form_valid(form)


class IncomeUpdateView(UserFilteredQuerysetMixin, UpdateView):
    model = Income
    form_class = IncomeForm
    template_name = "finance/income_form.html"
    success_url = reverse_lazy("finance:income-list")
    extra_context = {"page_title": "Editar ingreso"}

    def form_valid(self, form):
        messages.success(self.request, "Ingreso actualizado correctamente.")
        return super().form_valid(form)


class IncomeDeleteView(UserFilteredQuerysetMixin, DeleteView):
    model = Income
    template_name = "finance/confirm_delete.html"
    success_url = reverse_lazy("finance:income-list")
    extra_context = {"page_title": "Eliminar ingreso"}

    def delete(self, request, *args, **kwargs):
        messages.success(self.request, "Ingreso eliminado correctamente.")
        return super().delete(request, *args, **kwargs)


class FixedExpenseListView(SearchableListView):
    model = FixedExpense
    template_name = "finance/fixed_expense_list.html"
    search_fields = ["description", "category__name"]
    extra_context = {"page_title": "Gastos fijos"}


class FixedExpenseCreateView(UserFilteredQuerysetMixin, CreateView):
    model = FixedExpense
    form_class = FixedExpenseForm
    template_name = "finance/fixed_expense_form.html"
    success_url = reverse_lazy("finance:fixed-expense-list")
    extra_context = {"page_title": "Nuevo gasto fijo"}

    def form_valid(self, form):
        messages.success(self.request, "Gasto fijo creado correctamente.")
        return super().form_valid(form)


class FixedExpenseUpdateView(UserFilteredQuerysetMixin, UpdateView):
    model = FixedExpense
    form_class = FixedExpenseForm
    template_name = "finance/fixed_expense_form.html"
    success_url = reverse_lazy("finance:fixed-expense-list")
    extra_context = {"page_title": "Editar gasto fijo"}

    def form_valid(self, form):
        messages.success(self.request, "Gasto fijo actualizado correctamente.")
        return super().form_valid(form)


class FixedExpenseDeleteView(UserFilteredQuerysetMixin, DeleteView):
    model = FixedExpense
    template_name = "finance/confirm_delete.html"
    success_url = reverse_lazy("finance:fixed-expense-list")
    extra_context = {"page_title": "Eliminar gasto fijo"}

    def delete(self, request, *args, **kwargs):
        messages.success(self.request, "Gasto fijo eliminado correctamente.")
        return super().delete(request, *args, **kwargs)


class VariableExpenseListView(SearchableListView):
    model = VariableExpense
    template_name = "finance/variable_expense_list.html"
    search_fields = ["description", "category__name"]
    extra_context = {"page_title": "Gastos variables"}


class VariableExpenseCreateView(UserFilteredQuerysetMixin, CreateView):
    model = VariableExpense
    form_class = VariableExpenseForm
    template_name = "finance/variable_expense_form.html"
    success_url = reverse_lazy("finance:variable-expense-list")
    extra_context = {"page_title": "Nuevo gasto variable"}

    def form_valid(self, form):
        messages.success(self.request, "Gasto variable creado correctamente.")
        return super().form_valid(form)


class VariableExpenseUpdateView(UserFilteredQuerysetMixin, UpdateView):
    model = VariableExpense
    form_class = VariableExpenseForm
    template_name = "finance/variable_expense_form.html"
    success_url = reverse_lazy("finance:variable-expense-list")
    extra_context = {"page_title": "Editar gasto variable"}

    def form_valid(self, form):
        messages.success(self.request, "Gasto variable actualizado correctamente.")
        return super().form_valid(form)


class VariableExpenseDeleteView(UserFilteredQuerysetMixin, DeleteView):
    model = VariableExpense
    template_name = "finance/confirm_delete.html"
    success_url = reverse_lazy("finance:variable-expense-list")
    extra_context = {"page_title": "Eliminar gasto variable"}

    def delete(self, request, *args, **kwargs):
        messages.success(self.request, "Gasto variable eliminado correctamente.")
        return super().delete(request, *args, **kwargs)


class SavingListView(SearchableListView):
    model = Saving
    template_name = "finance/saving_list.html"
    search_fields = ["description", "category__name", "goal_name"]
    extra_context = {"page_title": "Ahorros"}


class SavingCreateView(UserFilteredQuerysetMixin, CreateView):
    model = Saving
    form_class = SavingForm
    template_name = "finance/saving_form.html"
    success_url = reverse_lazy("finance:saving-list")
    extra_context = {"page_title": "Nuevo ahorro"}

    def form_valid(self, form):
        messages.success(self.request, "Ahorro creado correctamente.")
        return super().form_valid(form)


class SavingUpdateView(UserFilteredQuerysetMixin, UpdateView):
    model = Saving
    form_class = SavingForm
    template_name = "finance/saving_form.html"
    success_url = reverse_lazy("finance:saving-list")
    extra_context = {"page_title": "Editar ahorro"}

    def form_valid(self, form):
        messages.success(self.request, "Ahorro actualizado correctamente.")
        return super().form_valid(form)


class SavingDeleteView(UserFilteredQuerysetMixin, DeleteView):
    model = Saving
    template_name = "finance/confirm_delete.html"
    success_url = reverse_lazy("finance:saving-list")
    extra_context = {"page_title": "Eliminar ahorro"}

    def delete(self, request, *args, **kwargs):
        messages.success(self.request, "Ahorro eliminado correctamente.")
        return super().delete(request, *args, **kwargs)


def _module_dashboard_context(user, model, year: int, month: int) -> dict:
    total = model.objects.filter(user=user, date__year=year, date__month=month).aggregate(
        total=Sum("amount")
    )["total"] or Decimal("0")
    previous_year, previous_month = get_previous_month(year, month)
    previous_total = model.objects.filter(
        user=user, date__year=previous_year, date__month=previous_month
    ).aggregate(total=Sum("amount"))["total"] or Decimal("0")
    delta = calculate_delta(total, previous_total)

    series = get_last_12_months_series(user, model)
    pie = get_category_breakdown(user, model, year, month)
    daily = get_daily_series(user, model, year, month)

    return {
        "total_mes": total,
        "delta": delta,
        "bar_labels": json.dumps([item["month"] for item in series]),
        "bar_data": json.dumps([item["total"] for item in series]),
        "pie_labels": json.dumps([item["category"] for item in pie]),
        "pie_data": json.dumps([item["total"] for item in pie]),
        "line_labels": json.dumps([item["day"] for item in daily]),
        "line_data": json.dumps([item["total"] for item in daily]),
    }


@login_required
def dashboard_general(request):
    year, month = get_year_month(request)
    kpis = get_month_kpis(request.user, year, month)
    prev_year, prev_month = get_previous_month(year, month)
    prev_kpis = get_month_kpis(request.user, prev_year, prev_month)

    income_total = kpis["ingresos_total_mes"]
    gastos_totales = kpis["gastos_totales_mes"]
    ahorro_total = kpis["ahorros_total_mes"]
    balance_total = kpis["balance_mes"]

    expense_ratio = (gastos_totales / income_total * 100) if income_total else None
    saving_ratio = (ahorro_total / income_total * 100) if income_total else None

    income_delta = calculate_delta(income_total, prev_kpis["ingresos_total_mes"])
    expense_delta = calculate_delta(gastos_totales, prev_kpis["gastos_totales_mes"])
    saving_delta = calculate_delta(ahorro_total, prev_kpis["ahorros_total_mes"])
    balance_delta = calculate_delta(balance_total, prev_kpis["balance_mes"])

    income_series = get_last_12_months_series(request.user, Income)
    fixed_series = get_last_12_months_series(request.user, FixedExpense)
    variable_series = get_last_12_months_series(request.user, VariableExpense)
    saving_series = get_last_12_months_series(request.user, Saving)

    bar_labels = [item["month"] for item in income_series]
    bar_datasets = {
        "ingresos": [item["total"] for item in income_series],
        "gastos_fijos": [item["total"] for item in fixed_series],
        "gastos_variables": [item["total"] for item in variable_series],
        "ahorros": [item["total"] for item in saving_series],
    }

    fixed_breakdown = get_category_breakdown(request.user, FixedExpense, year, month)
    variable_breakdown = get_category_breakdown(request.user, VariableExpense, year, month)
    expense_breakdown = {}
    for item in fixed_breakdown + variable_breakdown:
        expense_breakdown[item["category"]] = expense_breakdown.get(item["category"], 0) + item[
            "total"
        ]

    pie_labels = list(expense_breakdown.keys())
    pie_data = list(expense_breakdown.values())

    expenses_qs = list(
        FixedExpense.objects.filter(user=request.user, date__year=year, date__month=month)
        .values("description", "amount", "category__name", "date")
        .order_by("-amount")
    ) + list(
        VariableExpense.objects.filter(user=request.user, date__year=year, date__month=month)
        .values("description", "amount", "category__name", "date")
        .order_by("-amount")
    )
    top_expenses = sorted(expenses_qs, key=lambda item: item["amount"], reverse=True)[:10]

    context = {
        "page_title": "Dashboard General",
        "year": year,
        "month": month,
        "months": MONTH_CHOICES,
        "years": build_year_options(),
        "kpis": kpis,
        "expense_ratio": expense_ratio,
        "saving_ratio": saving_ratio,
        "income_delta": income_delta,
        "expense_delta": expense_delta,
        "saving_delta": saving_delta,
        "balance_delta": balance_delta,
        "bar_labels": json.dumps(bar_labels),
        "bar_datasets": json.dumps(bar_datasets),
        "pie_labels": json.dumps(pie_labels),
        "pie_data": json.dumps(pie_data),
        "top_expenses": top_expenses,
    }
    return render(request, "finance/dashboard_general.html", context)


@login_required
def dashboard_income(request):
    year, month = get_year_month(request)
    context = {
        "page_title": "Dashboard de Ingresos",
        "year": year,
        "month": month,
        "months": MONTH_CHOICES,
        "years": build_year_options(),
    }
    context.update(_module_dashboard_context(request.user, Income, year, month))
    return render(request, "finance/dashboard_income.html", context)


@login_required
def dashboard_fixed_expense(request):
    year, month = get_year_month(request)
    context = {
        "page_title": "Dashboard de Gastos Fijos",
        "year": year,
        "month": month,
        "months": MONTH_CHOICES,
        "years": build_year_options(),
    }
    context.update(_module_dashboard_context(request.user, FixedExpense, year, month))
    return render(request, "finance/dashboard_fixed_expense.html", context)


@login_required
def dashboard_variable_expense(request):
    year, month = get_year_month(request)
    context = {
        "page_title": "Dashboard de Gastos Variables",
        "year": year,
        "month": month,
        "months": MONTH_CHOICES,
        "years": build_year_options(),
    }
    context.update(_module_dashboard_context(request.user, VariableExpense, year, month))
    return render(request, "finance/dashboard_variable_expense.html", context)


@login_required
def dashboard_saving(request):
    year, month = get_year_month(request)
    context = {
        "page_title": "Dashboard de Ahorros",
        "year": year,
        "month": month,
        "months": MONTH_CHOICES,
        "years": build_year_options(),
    }
    context.update(_module_dashboard_context(request.user, Saving, year, month))
    return render(request, "finance/dashboard_saving.html", context)


def _export_monthly_summary(request, title: str, data: dict) -> HttpResponse:
    response = HttpResponse(content_type="text/csv")
    response["Content-Disposition"] = f"attachment; filename={title}.csv"
    writer = csv.writer(response)
    writer.writerow(["Indicador", "Valor"])
    for key, value in data.items():
        writer.writerow([key, value])
    return response


@login_required
def export_general_summary(request):
    year, month = get_year_month(request)
    kpis = get_month_kpis(request.user, year, month)
    data = {
        "Ingresos": kpis["ingresos_total_mes"],
        "Gastos fijos": kpis["gastos_fijos_total_mes"],
        "Gastos variables": kpis["gastos_variables_total_mes"],
        "Ahorros": kpis["ahorros_total_mes"],
        "Gastos totales": kpis["gastos_totales_mes"],
        "Balance": kpis["balance_mes"],
    }
    return _export_monthly_summary(request, f"resumen_general_{year}_{month}", data)


@login_required
def export_module_summary(request, module: str):
    year, month = get_year_month(request)
    model_map = {
        "income": Income,
        "fixed": FixedExpense,
        "variable": VariableExpense,
        "saving": Saving,
    }
    model = model_map.get(module)
    if not model:
        return HttpResponse(status=404)
    total = model.objects.filter(user=request.user, date__year=year, date__month=month).aggregate(
        total=Sum("amount")
    )["total"] or Decimal("0")
    return _export_monthly_summary(
        request, f"resumen_{module}_{year}_{month}", {"Total": total}
    )
