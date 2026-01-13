import calendar
from datetime import date
from decimal import Decimal

from django.db.models import Sum
from django.db.models.functions import ExtractDay, TruncMonth
from django.utils import timezone

from .models import FixedExpense, Income, Saving, VariableExpense


def _month_bounds(year: int, month: int) -> tuple[date, date]:
    last_day = calendar.monthrange(year, month)[1]
    return date(year, month, 1), date(year, month, last_day)


def _safe_sum(queryset) -> Decimal:
    return queryset.aggregate(total=Sum("amount"))["total"] or Decimal("0")


def get_month_kpis(user, year: int, month: int) -> dict:
    income_total = _safe_sum(Income.objects.filter(user=user, date__year=year, date__month=month))
    fixed_total = _safe_sum(
        FixedExpense.objects.filter(user=user, date__year=year, date__month=month)
    )
    variable_total = _safe_sum(
        VariableExpense.objects.filter(user=user, date__year=year, date__month=month)
    )
    saving_total = _safe_sum(Saving.objects.filter(user=user, date__year=year, date__month=month))

    gastos_totales = fixed_total + variable_total
    balance = income_total - gastos_totales - saving_total

    return {
        "ingresos_total_mes": income_total,
        "gastos_fijos_total_mes": fixed_total,
        "gastos_variables_total_mes": variable_total,
        "ahorros_total_mes": saving_total,
        "gastos_totales_mes": gastos_totales,
        "balance_mes": balance,
    }


def get_last_12_months_series(user, model) -> list[dict]:
    today = timezone.localdate()
    year = today.year
    month = today.month

    months = []
    for i in range(11, -1, -1):
        target_month = month - i
        target_year = year
        while target_month <= 0:
            target_month += 12
            target_year -= 1
        months.append(date(target_year, target_month, 1))

    start_date = months[0]
    end_date = _month_bounds(months[-1].year, months[-1].month)[1]

    totals = (
        model.objects.filter(user=user, date__gte=start_date, date__lte=end_date)
        .annotate(month=TruncMonth("date"))
        .values("month")
        .annotate(total=Sum("amount"))
        .order_by("month")
    )

    total_map = {item["month"].date(): item["total"] for item in totals}
    series = []
    for month_date in months:
        series.append(
            {
                "month": month_date.strftime("%b %Y"),
                "total": float(total_map.get(month_date, Decimal("0"))),
            }
        )
    return series


def get_category_breakdown(user, model, year: int, month: int) -> list[dict]:
    breakdown = (
        model.objects.filter(user=user, date__year=year, date__month=month)
        .values("category__name")
        .annotate(total=Sum("amount"))
        .order_by("-total")
    )
    return [
        {"category": item["category__name"], "total": float(item["total"])}
        for item in breakdown
    ]


def get_daily_series(user, model, year: int, month: int) -> list[dict]:
    start_date, end_date = _month_bounds(year, month)
    daily = (
        model.objects.filter(user=user, date__gte=start_date, date__lte=end_date)
        .annotate(day=ExtractDay("date"))
        .values("day")
        .annotate(total=Sum("amount"))
        .order_by("day")
    )
    total_map = {item["day"]: item["total"] for item in daily}
    days = range(1, end_date.day + 1)
    return [
        {"day": day, "total": float(total_map.get(day, Decimal("0")))} for day in days
    ]


def get_previous_month(year: int, month: int) -> tuple[int, int]:
    if month == 1:
        return year - 1, 12
    return year, month - 1


def calculate_delta(current: Decimal, previous: Decimal) -> dict:
    if previous == 0:
        return {"value": None, "direction": "neutral"}
    diff = current - previous
    direction = "up" if diff >= 0 else "down"
    percent = (diff / previous) * 100
    return {"value": float(percent), "direction": direction}
