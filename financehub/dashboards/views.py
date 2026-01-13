import json
from datetime import date
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.db.models import Sum
from .services import (
    get_month_year_from_params,
    get_monthly_totals,
    get_last_12_months_series,
    get_category_breakdown,
    get_daily_series,
    get_top_categories,
    get_top_expenses,
)
from transactions.models import Income, FixedExpense, VariableExpense, Saving


def _month_options():
    return [
        (1, 'Enero'),
        (2, 'Febrero'),
        (3, 'Marzo'),
        (4, 'Abril'),
        (5, 'Mayo'),
        (6, 'Junio'),
        (7, 'Julio'),
        (8, 'Agosto'),
        (9, 'Septiembre'),
        (10, 'Octubre'),
        (11, 'Noviembre'),
        (12, 'Diciembre'),
    ]


def _years():
    current_year = date.today().year
    return [current_year - i for i in range(0, 5)]


@login_required
def general_dashboard(request):
    if request.GET.get('toggle_dark'):
        request.session['dark_mode'] = not request.session.get('dark_mode', False)
        return render(request, 'dashboards/toggle.html', {'ok': True})
    year, month = get_month_year_from_params(request.GET.get('year'), request.GET.get('month'))
    totals = get_monthly_totals(request.user, year, month)
    balance = totals['income'] - totals['fixed'] - totals['variable'] - totals['saving']
    income_labels, income_series = get_last_12_months_series(request.user, Income)
    _, fixed_series = get_last_12_months_series(request.user, FixedExpense)
    _, variable_series = get_last_12_months_series(request.user, VariableExpense)
    _, saving_series = get_last_12_months_series(request.user, Saving)

    expense_labels, expense_data = get_category_breakdown(request.user, FixedExpense, year, month)
    variable_labels, variable_data = get_category_breakdown(request.user, VariableExpense, year, month)
    breakdown = {}
    for label, value in zip(expense_labels, expense_data):
        breakdown[label] = breakdown.get(label, 0) + value
    for label, value in zip(variable_labels, variable_data):
        breakdown[label] = breakdown.get(label, 0) + value

    expenses_total = totals['fixed'] + totals['variable']
    percent_expense = (expenses_total / totals['income'] * 100) if totals['income'] else 0
    percent_saving = (totals['saving'] / totals['income'] * 100) if totals['income'] else 0

    previous_month = month - 1 or 12
    previous_year = year - 1 if month == 1 else year
    prev_totals = get_monthly_totals(request.user, previous_year, previous_month)
    prev_balance = prev_totals['income'] - prev_totals['fixed'] - prev_totals['variable'] - prev_totals['saving']
    balance_delta = balance - prev_balance

    context = {
        'year': year,
        'month': month,
        'month_options': _month_options(),
        'years': _years(),
        'totals': totals,
        'balance': balance,
        'percent_expense': percent_expense,
        'percent_saving': percent_saving,
        'balance_delta': balance_delta,
        'balance_delta_positive': balance_delta >= 0,
        'series_labels': json.dumps(income_labels),
        'income_series': json.dumps(income_series),
        'fixed_series': json.dumps(fixed_series),
        'variable_series': json.dumps(variable_series),
        'saving_series': json.dumps(saving_series),
        'expense_breakdown_labels': json.dumps(list(breakdown.keys())),
        'expense_breakdown_data': json.dumps(list(breakdown.values())),
        'top_expenses': get_top_expenses(request.user, year, month),
    }
    return render(request, 'dashboards/general.html', context)


@login_required
def income_dashboard(request):
    year, month = get_month_year_from_params(request.GET.get('year'), request.GET.get('month'))
    totals = get_monthly_totals(request.user, year, month)
    labels, series = get_last_12_months_series(request.user, Income)
    category_labels, category_data = get_category_breakdown(request.user, Income, year, month)
    daily_labels, daily_data = get_daily_series(request.user, Income, year, month)
    top_categories = get_top_categories(
        Income.objects.filter(user=request.user, date__year=year, date__month=month)
    )
    context = {
        'title': 'Ingresos',
        'year': year,
        'month': month,
        'month_options': _month_options(),
        'years': _years(),
        'total_month': totals['income'],
        'series_labels': json.dumps(labels),
        'series_data': json.dumps(series),
        'category_labels': json.dumps(category_labels),
        'category_data': json.dumps(category_data),
        'daily_labels': json.dumps(daily_labels),
        'daily_data': json.dumps(daily_data),
        'top_categories': top_categories,
    }
    return render(request, 'dashboards/module.html', context)


@login_required
def fixed_expense_dashboard(request):
    year, month = get_month_year_from_params(request.GET.get('year'), request.GET.get('month'))
    totals = get_monthly_totals(request.user, year, month)
    labels, series = get_last_12_months_series(request.user, FixedExpense)
    category_labels, category_data = get_category_breakdown(request.user, FixedExpense, year, month)
    daily_labels, daily_data = get_daily_series(request.user, FixedExpense, year, month)
    top_categories = get_top_categories(
        FixedExpense.objects.filter(user=request.user, date__year=year, date__month=month)
    )
    context = {
        'title': 'Gastos fijos',
        'year': year,
        'month': month,
        'month_options': _month_options(),
        'years': _years(),
        'total_month': totals['fixed'],
        'series_labels': json.dumps(labels),
        'series_data': json.dumps(series),
        'category_labels': json.dumps(category_labels),
        'category_data': json.dumps(category_data),
        'daily_labels': json.dumps(daily_labels),
        'daily_data': json.dumps(daily_data),
        'top_categories': top_categories,
    }
    return render(request, 'dashboards/module.html', context)


@login_required
def variable_expense_dashboard(request):
    year, month = get_month_year_from_params(request.GET.get('year'), request.GET.get('month'))
    totals = get_monthly_totals(request.user, year, month)
    labels, series = get_last_12_months_series(request.user, VariableExpense)
    category_labels, category_data = get_category_breakdown(request.user, VariableExpense, year, month)
    daily_labels, daily_data = get_daily_series(request.user, VariableExpense, year, month)
    top_categories = get_top_categories(
        VariableExpense.objects.filter(user=request.user, date__year=year, date__month=month)
    )
    context = {
        'title': 'Gastos variables',
        'year': year,
        'month': month,
        'month_options': _month_options(),
        'years': _years(),
        'total_month': totals['variable'],
        'series_labels': json.dumps(labels),
        'series_data': json.dumps(series),
        'category_labels': json.dumps(category_labels),
        'category_data': json.dumps(category_data),
        'daily_labels': json.dumps(daily_labels),
        'daily_data': json.dumps(daily_data),
        'top_categories': top_categories,
    }
    return render(request, 'dashboards/module.html', context)


@login_required
def saving_dashboard(request):
    year, month = get_month_year_from_params(request.GET.get('year'), request.GET.get('month'))
    totals = get_monthly_totals(request.user, year, month)
    labels, series = get_last_12_months_series(request.user, Saving)
    category_labels, category_data = get_category_breakdown(request.user, Saving, year, month)
    daily_labels, daily_data = get_daily_series(request.user, Saving, year, month)
    top_categories = get_top_categories(
        Saving.objects.filter(user=request.user, date__year=year, date__month=month)
    )
    context = {
        'title': 'Ahorros',
        'year': year,
        'month': month,
        'month_options': _month_options(),
        'years': _years(),
        'total_month': totals['saving'],
        'series_labels': json.dumps(labels),
        'series_data': json.dumps(series),
        'category_labels': json.dumps(category_labels),
        'category_data': json.dumps(category_data),
        'daily_labels': json.dumps(daily_labels),
        'daily_data': json.dumps(daily_data),
        'top_categories': top_categories,
    }
    return render(request, 'dashboards/module.html', context)
