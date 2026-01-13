from django import forms
from .models import Income, FixedExpense, VariableExpense, Saving


class DateInput(forms.DateInput):
    input_type = 'date'


class IncomeForm(forms.ModelForm):
    class Meta:
        model = Income
        fields = [
            'date',
            'amount',
            'category',
            'description',
            'payment_method',
            'notes',
            'source',
        ]
        widgets = {'date': DateInput()}


class FixedExpenseForm(forms.ModelForm):
    class Meta:
        model = FixedExpense
        fields = [
            'date',
            'amount',
            'category',
            'description',
            'payment_method',
            'notes',
            'is_paid',
            'due_day',
        ]
        widgets = {'date': DateInput()}


class VariableExpenseForm(forms.ModelForm):
    class Meta:
        model = VariableExpense
        fields = [
            'date',
            'amount',
            'category',
            'description',
            'payment_method',
            'notes',
            'expense_type',
        ]
        widgets = {'date': DateInput()}


class SavingForm(forms.ModelForm):
    class Meta:
        model = Saving
        fields = [
            'date',
            'amount',
            'category',
            'description',
            'payment_method',
            'notes',
            'saving_type',
            'goal_name',
            'goal_amount',
        ]
        widgets = {'date': DateInput()}
