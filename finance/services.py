import calendar
import datetime
from decimal import Decimal

from django.db.models import Sum
from django.db.models.functions import TruncDate, TruncMonth
from django.utils import timezone

from finance.models import FixedExpense, Income, Saving, VariableExpense


def _month_range(year: int, month: int) -> tuple[datetime.date, datetime.date]:
    last_day = calendar.monthrange(year, month)[1]
    start = datetime.date(year, month, 1)
    end = datetime.date(year, month, last_day)
    return start, end


def get_month_kpis(user, year: int, month: int) -> dict:
    start, end = _month_range(year, month)

    def total_for_range(model, range_start, range_end):
        return (
            model.objects.filter(user=user, date__range=(range_start, range_end)).aggregate(total=Sum("amount"))["total"]
            or Decimal("0")
        )

    income_total = total_for_range(Income, start, end)
    fixed_total = total_for_range(FixedExpense, start, end)
    variable_total = total_for_range(VariableExpense, start, end)
    saving_total = total_for_range(Saving, start, end)
    expense_total = fixed_total + variable_total
    balance = income_total - expense_total - saving_total

    prev_month = month - 1
    prev_year = year
    if prev_month == 0:
        prev_month = 12
        prev_year -= 1
    prev_start, prev_end = _month_range(prev_year, prev_month)
    prev_income = total_for_range(Income, prev_start, prev_end)
    prev_expenses = total_for_range(FixedExpense, prev_start, prev_end) + total_for_range(
        VariableExpense,
        prev_start,
        prev_end,
    )

    delta_income = income_total - prev_income
    delta_expenses = expense_total - prev_expenses

    expense_pct = (expense_total / income_total * Decimal("100")) if income_total else Decimal("0")
    saving_pct = (saving_total / income_total * Decimal("100")) if income_total else Decimal("0")

    return {
        "income_total": income_total,
        "fixed_total": fixed_total,
        "variable_total": variable_total,
        "saving_total": saving_total,
        "expense_total": expense_total,
        "balance": balance,
        "expense_pct": expense_pct,
        "saving_pct": saving_pct,
        "delta_income": delta_income,
        "delta_expenses": delta_expenses,
    }


def get_last_12_months_series(user, model):
    today = timezone.localdate()
    start_month = (today.replace(day=1) - datetime.timedelta(days=365)).replace(day=1)
    months = []
    current = start_month
    for _ in range(12):
        months.append(current)
        year = current.year + (current.month // 12)
        month = current.month % 12 + 1
        current = current.replace(year=year, month=month)

    totals = (
        model.objects.filter(user=user, date__gte=months[0])
        .annotate(month=TruncMonth("date"))
        .values("month")
        .annotate(total=Sum("amount"))
    )
    totals_map = {item["month"].date(): item["total"] for item in totals}

    labels = [month.strftime("%b %Y") for month in months]
    data = [float(totals_map.get(month, 0) or 0) for month in months]
    return {"labels": labels, "data": data}


def get_category_breakdown(user, model, year: int, month: int):
    start, end = _month_range(year, month)
    data = (
        model.objects.filter(user=user, date__range=(start, end))
        .values("category__name")
        .annotate(total=Sum("amount"))
        .order_by("-total")
    )
    labels = [item["category__name"] for item in data]
    values = [float(item["total"]) for item in data]
    return {"labels": labels, "data": values}


def get_daily_series(user, model, year: int, month: int):
    start, end = _month_range(year, month)
    data = (
        model.objects.filter(user=user, date__range=(start, end))
        .annotate(day=TruncDate("date"))
        .values("day")
        .annotate(total=Sum("amount"))
        .order_by("day")
    )
    labels = [item["day"].strftime("%d/%m") for item in data]
    values = [float(item["total"]) for item in data]
    return {"labels": labels, "data": values}
