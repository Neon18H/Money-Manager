import calendar
from datetime import date
from django.db.models import Sum
from django.db.models.functions import TruncMonth, TruncDay
from transactions.models import Income, FixedExpense, VariableExpense, Saving


def get_month_year_from_params(year_param, month_param):
    today = date.today()
    year = int(year_param) if year_param else today.year
    month = int(month_param) if month_param else today.month
    return year, month


def get_monthly_totals(user, year, month):
    totals = {
        'income': Income.objects.filter(user=user, date__year=year, date__month=month).aggregate(total=Sum('amount')),
        'fixed': FixedExpense.objects.filter(user=user, date__year=year, date__month=month).aggregate(total=Sum('amount')),
        'variable': VariableExpense.objects.filter(user=user, date__year=year, date__month=month).aggregate(total=Sum('amount')),
        'saving': Saving.objects.filter(user=user, date__year=year, date__month=month).aggregate(total=Sum('amount')),
    }
    return {key: (value['total'] or 0) for key, value in totals.items()}


def get_last_12_months_series(user, model):
    today = date.today()
    start = date(today.year, today.month, 1)
    months = []
    for i in range(11, -1, -1):
        month_year = (start.year * 12 + start.month - 1) - i
        year = month_year // 12
        month = month_year % 12 + 1
        months.append(date(year, month, 1))
    queryset = (
        model.objects.filter(user=user, date__gte=months[0])
        .annotate(month=TruncMonth('date'))
        .values('month')
        .annotate(total=Sum('amount'))
        .order_by('month')
    )
    data_map = {
        (item['month'].date() if hasattr(item['month'], 'date') else item['month']): float(item['total'])
        for item in queryset
    }
    labels = [m.strftime('%b %Y') for m in months]
    data = [data_map.get(m, 0) for m in months]
    return labels, data


def get_category_breakdown(user, model, year, month):
    queryset = (
        model.objects.filter(user=user, date__year=year, date__month=month, category__isnull=False)
        .values('category__name')
        .annotate(total=Sum('amount'))
        .order_by('-total')
    )
    labels = [item['category__name'] for item in queryset]
    data = [float(item['total']) for item in queryset]
    return labels, data


def get_daily_series(user, model, year, month):
    last_day = calendar.monthrange(year, month)[1]
    days = [date(year, month, day) for day in range(1, last_day + 1)]
    queryset = (
        model.objects.filter(user=user, date__year=year, date__month=month)
        .annotate(day=TruncDay('date'))
        .values('day')
        .annotate(total=Sum('amount'))
        .order_by('day')
    )
    data_map = {
        (item['day'].date() if hasattr(item['day'], 'date') else item['day']): float(item['total'])
        for item in queryset
    }
    labels = [d.strftime('%d %b') for d in days]
    data = [data_map.get(d, 0) for d in days]
    return labels, data


def get_top_categories(queryset, limit=5):
    return queryset.values('category__name').annotate(total=Sum('amount')).order_by('-total')[:limit]


def get_top_expenses(user, year, month, limit=10):
    fixed = FixedExpense.objects.filter(user=user, date__year=year, date__month=month).values(
        'description', 'amount', 'date'
    )
    variable = VariableExpense.objects.filter(user=user, date__year=year, date__month=month).values(
        'description', 'amount', 'date'
    )
    combined = [
        {**item, 'kind': 'Gasto fijo'} for item in fixed
    ] + [
        {**item, 'kind': 'Gasto variable'} for item in variable
    ]
    combined.sort(key=lambda item: item['amount'], reverse=True)
    return combined[:limit]
