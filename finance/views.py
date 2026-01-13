import calendar
import datetime
import json
from decimal import Decimal

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q, Sum
from django.shortcuts import render
from django.urls import reverse_lazy
from django.utils import timezone
from django.views.generic import CreateView, DeleteView, ListView, UpdateView

from finance.forms import (
    CategoryForm,
    FixedExpenseForm,
    IncomeForm,
    PaymentMethodForm,
    SavingForm,
    SavingGoalForm,
    VariableExpenseForm,
)
from finance.models import Category, FixedExpense, Income, PaymentMethod, Saving, SavingGoal, VariableExpense
from finance.services import (
    get_category_breakdown,
    get_daily_series,
    get_last_12_months_series,
    get_month_kpis,
    get_saving_distribution,
    get_saving_goal_progress,
    get_year_12_months_series,
)

MONTH_LABELS = ["Ene", "Feb", "Mar", "Abr", "May", "Jun", "Jul", "Ago", "Sep", "Oct", "Nov", "Dic"]


class UserQuerySetMixin:
    def get_queryset(self):
        return super().get_queryset().filter(user=self.request.user)


class UserFormMixin:
    category_kind = None

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs.update({"user": self.request.user, "category_kind": self.category_kind})
        return kwargs

    def form_valid(self, form):
        form.instance.user = self.request.user
        messages.success(self.request, "Registro guardado correctamente.")
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        action = "Editar" if getattr(self, "object", None) else "Nuevo"
        context["form_title"] = f"{action} {self.model._meta.verbose_name.title()}"
        form = context.get("form")
        if form and "category" in form.fields:
            context["category_empty"] = not form.fields["category"].queryset.exists()
            context["category_settings_url"] = reverse_lazy("settings_categories")
        if form and "payment_method" in form.fields:
            context["payment_method_empty"] = not form.fields["payment_method"].queryset.exists()
            context["payment_settings_url"] = reverse_lazy("settings_payment_methods")
        if form and "goal" in form.fields:
            context["goal_empty"] = not form.fields["goal"].queryset.exists()
            context["goal_create_url"] = reverse_lazy("saving_goal_create")
        return context


class BaseDeleteView(LoginRequiredMixin, UserQuerySetMixin, DeleteView):
    template_name = "finance/confirm_delete.html"

    def delete(self, request, *args, **kwargs):
        messages.success(request, "Registro eliminado correctamente.")
        return super().delete(request, *args, **kwargs)


class IncomeListView(LoginRequiredMixin, UserQuerySetMixin, ListView):
    model = Income
    template_name = "finance/income_list.html"
    paginate_by = 10

    def get_queryset(self):
        queryset = super().get_queryset()
        query = self.request.GET.get("q")
        if query:
            queryset = queryset.filter(Q(description__icontains=query) | Q(source__icontains=query))
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({"title": "Ingresos", "create_url": reverse_lazy("income_create")})
        return context


class IncomeCreateView(LoginRequiredMixin, UserFormMixin, CreateView):
    model = Income
    form_class = IncomeForm
    template_name = "finance/form.html"
    success_url = reverse_lazy("income_list")
    category_kind = Category.KIND_INCOME


class IncomeUpdateView(LoginRequiredMixin, UserFormMixin, UserQuerySetMixin, UpdateView):
    model = Income
    form_class = IncomeForm
    template_name = "finance/form.html"
    success_url = reverse_lazy("income_list")
    category_kind = Category.KIND_INCOME


class IncomeDeleteView(BaseDeleteView):
    model = Income
    success_url = reverse_lazy("income_list")


class FixedExpenseListView(LoginRequiredMixin, UserQuerySetMixin, ListView):
    model = FixedExpense
    template_name = "finance/fixed_expense_list.html"
    paginate_by = 10

    def get_queryset(self):
        queryset = super().get_queryset()
        query = self.request.GET.get("q")
        if query:
            queryset = queryset.filter(Q(description__icontains=query))
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({"title": "Gastos Fijos", "create_url": reverse_lazy("fixed_expense_create")})
        return context


class FixedExpenseCreateView(LoginRequiredMixin, UserFormMixin, CreateView):
    model = FixedExpense
    form_class = FixedExpenseForm
    template_name = "finance/form.html"
    success_url = reverse_lazy("fixed_expense_list")
    category_kind = Category.KIND_FIXED


class FixedExpenseUpdateView(LoginRequiredMixin, UserFormMixin, UserQuerySetMixin, UpdateView):
    model = FixedExpense
    form_class = FixedExpenseForm
    template_name = "finance/form.html"
    success_url = reverse_lazy("fixed_expense_list")
    category_kind = Category.KIND_FIXED


class FixedExpenseDeleteView(BaseDeleteView):
    model = FixedExpense
    success_url = reverse_lazy("fixed_expense_list")


class VariableExpenseListView(LoginRequiredMixin, UserQuerySetMixin, ListView):
    model = VariableExpense
    template_name = "finance/variable_expense_list.html"
    paginate_by = 10

    def get_queryset(self):
        queryset = super().get_queryset()
        query = self.request.GET.get("q")
        if query:
            queryset = queryset.filter(Q(description__icontains=query))
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({"title": "Gastos Variables", "create_url": reverse_lazy("variable_expense_create")})
        return context


class VariableExpenseCreateView(LoginRequiredMixin, UserFormMixin, CreateView):
    model = VariableExpense
    form_class = VariableExpenseForm
    template_name = "finance/form.html"
    success_url = reverse_lazy("variable_expense_list")
    category_kind = Category.KIND_VARIABLE


class VariableExpenseUpdateView(LoginRequiredMixin, UserFormMixin, UserQuerySetMixin, UpdateView):
    model = VariableExpense
    form_class = VariableExpenseForm
    template_name = "finance/form.html"
    success_url = reverse_lazy("variable_expense_list")
    category_kind = Category.KIND_VARIABLE


class VariableExpenseDeleteView(BaseDeleteView):
    model = VariableExpense
    success_url = reverse_lazy("variable_expense_list")


class SavingListView(LoginRequiredMixin, UserQuerySetMixin, ListView):
    model = Saving
    template_name = "finance/saving_list.html"
    paginate_by = 10

    def get_queryset(self):
        queryset = super().get_queryset()
        query = self.request.GET.get("q")
        if query:
            queryset = queryset.filter(
                Q(description__icontains=query) | Q(goal_name__icontains=query) | Q(goal__name__icontains=query)
            )
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({"title": "Ahorros", "create_url": reverse_lazy("saving_create")})
        return context


class SavingCreateView(LoginRequiredMixin, UserFormMixin, CreateView):
    model = Saving
    form_class = SavingForm
    template_name = "finance/form.html"
    success_url = reverse_lazy("saving_list")
    category_kind = Category.KIND_SAVING

    def get_initial(self):
        initial = super().get_initial()
        goal_id = self.request.GET.get("goal")
        if goal_id:
            initial["goal"] = goal_id
        return initial


class SavingUpdateView(LoginRequiredMixin, UserFormMixin, UserQuerySetMixin, UpdateView):
    model = Saving
    form_class = SavingForm
    template_name = "finance/form.html"
    success_url = reverse_lazy("saving_list")
    category_kind = Category.KIND_SAVING


class SavingDeleteView(BaseDeleteView):
    model = Saving
    success_url = reverse_lazy("saving_list")


@login_required
def dashboard(request):
    today = timezone.localdate()
    year = int(request.GET.get("year", today.year))
    month = int(request.GET.get("month", today.month))

    kpis = get_month_kpis(request.user, year, month)

    income_series = get_year_12_months_series(Income, request.user, year)
    fixed_series = get_year_12_months_series(FixedExpense, request.user, year)
    variable_series = get_year_12_months_series(VariableExpense, request.user, year)
    saving_series = get_year_12_months_series(Saving, request.user, year)
    expense_series = {
        "labels": income_series["labels"],
        "data": [
            fixed + variable
            for fixed, variable in zip(fixed_series["data"], variable_series["data"], strict=False)
        ],
    }

    expense_category_data = _merge_category_breakdown(
        get_category_breakdown(request.user, FixedExpense, year, month),
        get_category_breakdown(request.user, VariableExpense, year, month),
    )

    top_expenses = _top_expenses(request.user, year, month)

    context = {
        "year": year,
        "month": month,
        "month_name": calendar.month_name[month],
        "months": range(1, 13),
        "kpis": kpis,
        "income_series": json.dumps(income_series),
        "expense_series": json.dumps(expense_series),
        "saving_series": json.dumps(saving_series),
        "month_labels": json.dumps(MONTH_LABELS),
        "expense_category_data": json.dumps(expense_category_data),
        "top_expenses": top_expenses,
    }
    return render(request, "finance/dashboard.html", context)


@login_required
def income_dashboard(request):
    return _module_dashboard(request, Income, "income")


@login_required
def fixed_expense_dashboard(request):
    return _module_dashboard(request, FixedExpense, "fixed")


@login_required
def variable_expense_dashboard(request):
    return _module_dashboard(request, VariableExpense, "variable")


@login_required
def saving_dashboard(request):
    today = timezone.localdate()
    year = int(request.GET.get("year", today.year))
    month = int(request.GET.get("month", today.month))
    start_month = datetime.date(year, month, 1)
    end_month = datetime.date(year, month, calendar.monthrange(year, month)[1])
    start_year = datetime.date(year, 1, 1)
    end_year = datetime.date(year, 12, 31)

    total_month = (
        Saving.objects.filter(user=request.user, date__range=(start_month, end_month)).aggregate(total=Sum("amount"))[
            "total"
        ]
        or Decimal("0")
    )
    total_year = (
        Saving.objects.filter(user=request.user, date__range=(start_year, end_year)).aggregate(total=Sum("amount"))[
            "total"
        ]
        or Decimal("0")
    )
    income_month = (
        Income.objects.filter(user=request.user, date__range=(start_month, end_month)).aggregate(total=Sum("amount"))[
            "total"
        ]
        or Decimal("0")
    )
    saving_pct = (total_month / income_month * Decimal("100")) if income_month else Decimal("0")

    goals_progress = get_saving_goal_progress(request.user)
    savings_distribution = get_saving_distribution(request.user, year)
    monthly_series = get_year_12_months_series(Saving, request.user, year)

    context = {
        "year": year,
        "month": month,
        "month_name": calendar.month_name[month],
        "months": range(1, 13),
        "total_month": total_month,
        "total_year": total_year,
        "saving_pct": saving_pct,
        "goals_progress": goals_progress,
        "saving_distribution": json.dumps(savings_distribution),
        "monthly_series": json.dumps(monthly_series),
        "month_labels": json.dumps(MONTH_LABELS),
    }
    return render(request, "finance/saving_dashboard.html", context)


@login_required
def settings_home(request):
    context = {
        "category_count": Category.objects.filter(user=request.user).count(),
        "payment_method_count": PaymentMethod.objects.filter(user=request.user).count(),
    }
    return render(request, "finance/settings/home.html", context)


class CategoryListView(LoginRequiredMixin, UserQuerySetMixin, ListView):
    model = Category
    template_name = "finance/settings/category_list.html"
    paginate_by = 10

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({"title": "Categorías", "create_url": reverse_lazy("settings_category_create")})
        return context


class CategoryCreateView(LoginRequiredMixin, CreateView):
    model = Category
    form_class = CategoryForm
    template_name = "finance/settings/category_form.html"
    success_url = reverse_lazy("settings_categories")

    def form_valid(self, form):
        form.instance.user = self.request.user
        messages.success(self.request, "Categoría guardada correctamente.")
        return super().form_valid(form)


class CategoryUpdateView(LoginRequiredMixin, UserQuerySetMixin, UpdateView):
    model = Category
    form_class = CategoryForm
    template_name = "finance/settings/category_form.html"
    success_url = reverse_lazy("settings_categories")

    def form_valid(self, form):
        messages.success(self.request, "Categoría actualizada correctamente.")
        return super().form_valid(form)


class CategoryDeleteView(BaseDeleteView):
    model = Category
    success_url = reverse_lazy("settings_categories")


class PaymentMethodListView(LoginRequiredMixin, UserQuerySetMixin, ListView):
    model = PaymentMethod
    template_name = "finance/settings/payment_method_list.html"
    paginate_by = 10

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({"title": "Métodos de pago", "create_url": reverse_lazy("settings_payment_method_create")})
        return context


class PaymentMethodCreateView(LoginRequiredMixin, CreateView):
    model = PaymentMethod
    form_class = PaymentMethodForm
    template_name = "finance/settings/payment_method_form.html"
    success_url = reverse_lazy("settings_payment_methods")

    def form_valid(self, form):
        form.instance.user = self.request.user
        messages.success(self.request, "Método de pago guardado correctamente.")
        return super().form_valid(form)


class PaymentMethodUpdateView(LoginRequiredMixin, UserQuerySetMixin, UpdateView):
    model = PaymentMethod
    form_class = PaymentMethodForm
    template_name = "finance/settings/payment_method_form.html"
    success_url = reverse_lazy("settings_payment_methods")

    def form_valid(self, form):
        messages.success(self.request, "Método de pago actualizado correctamente.")
        return super().form_valid(form)


class PaymentMethodDeleteView(BaseDeleteView):
    model = PaymentMethod
    success_url = reverse_lazy("settings_payment_methods")


class SavingGoalListView(LoginRequiredMixin, UserQuerySetMixin, ListView):
    model = SavingGoal
    template_name = "finance/saving_goal_list.html"
    paginate_by = 10

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({"title": "Metas de ahorro", "create_url": reverse_lazy("saving_goal_create")})
        return context


class SavingGoalCreateView(LoginRequiredMixin, CreateView):
    model = SavingGoal
    form_class = SavingGoalForm
    template_name = "finance/saving_goal_form.html"
    success_url = reverse_lazy("saving_goal_list")

    def form_valid(self, form):
        form.instance.user = self.request.user
        messages.success(self.request, "Meta creada correctamente.")
        return super().form_valid(form)


class SavingGoalUpdateView(LoginRequiredMixin, UserQuerySetMixin, UpdateView):
    model = SavingGoal
    form_class = SavingGoalForm
    template_name = "finance/saving_goal_form.html"
    success_url = reverse_lazy("saving_goal_list")

    def form_valid(self, form):
        messages.success(self.request, "Meta actualizada correctamente.")
        return super().form_valid(form)


class SavingGoalDeleteView(BaseDeleteView):
    model = SavingGoal
    success_url = reverse_lazy("saving_goal_list")


def _module_dashboard(request, model, slug):
    today = timezone.localdate()
    year = int(request.GET.get("year", today.year))
    month = int(request.GET.get("month", today.month))
    start = datetime.date(year, month, 1)
    end = datetime.date(year, month, calendar.monthrange(year, month)[1])

    total_month = (
        model.objects.filter(user=request.user, date__range=(start, end)).aggregate(total=Sum("amount"))["total"]
        or Decimal("0")
    )
    last_12 = get_last_12_months_series(request.user, model)
    category_data = get_category_breakdown(request.user, model, year, month)
    daily_series = get_daily_series(request.user, model, year, month)

    context = {
        "year": year,
        "month": month,
        "month_name": calendar.month_name[month],
        "months": range(1, 13),
        "total_month": total_month,
        "last_12": json.dumps(last_12),
        "category_data": json.dumps(category_data),
        "daily_series": json.dumps(daily_series),
        "slug": slug,
    }
    return render(request, "finance/module_dashboard.html", context)


def _merge_category_breakdown(primary, secondary):
    totals = {}
    for label, value in zip(primary["labels"], primary["data"], strict=False):
        totals[label] = totals.get(label, 0) + value
    for label, value in zip(secondary["labels"], secondary["data"], strict=False):
        totals[label] = totals.get(label, 0) + value
    labels = list(totals.keys())
    data = [totals[label] for label in labels]
    return {"labels": labels, "data": data}


def _top_expenses(user, year, month):
    start = datetime.date(year, month, 1)
    end = datetime.date(year, month, calendar.monthrange(year, month)[1])
    fixed = (
        FixedExpense.objects.filter(user=user, date__range=(start, end))
        .values("description", "amount", "category__name")
    )
    variable = (
        VariableExpense.objects.filter(user=user, date__range=(start, end))
        .values("description", "amount", "category__name")
    )
    combined = [
        {"description": item["description"], "amount": item["amount"], "category": item["category__name"]}
        for item in list(fixed) + list(variable)
    ]
    combined.sort(key=lambda item: item["amount"], reverse=True)
    return combined[:10]
