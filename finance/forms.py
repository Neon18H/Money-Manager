from django import forms
from django.contrib.auth.forms import AuthenticationForm

from finance.models import Category, FixedExpense, Income, PaymentMethod, Saving, VariableExpense


class BootstrapAuthenticationForm(AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            existing_classes = field.widget.attrs.get("class", "")
            field.widget.attrs["class"] = f"{existing_classes} form-control".strip()


class BaseTransactionForm(forms.ModelForm):
    date = forms.DateField(widget=forms.DateInput(attrs={"type": "date", "class": "form-control"}))
    description = forms.CharField(widget=forms.TextInput(attrs={"class": "form-control"}))
    amount = forms.DecimalField(widget=forms.NumberInput(attrs={"class": "form-control", "step": "0.01"}))
    category = forms.ModelChoiceField(queryset=Category.objects.none(), widget=forms.Select(attrs={"class": "form-select"}))
    payment_method = forms.ModelChoiceField(
        queryset=PaymentMethod.objects.none(),
        widget=forms.Select(attrs={"class": "form-select"}),
    )
    notes = forms.CharField(
        required=False,
        widget=forms.Textarea(attrs={"class": "form-control", "rows": 3}),
    )

    def __init__(self, *args, user=None, category_kind=None, **kwargs):
        super().__init__(*args, **kwargs)
        if user is not None:
            category_qs = Category.objects.filter(user=user)
            if category_kind:
                category_qs = category_qs.filter(kind=category_kind)
            self.fields["category"].queryset = category_qs
            self.fields["payment_method"].queryset = PaymentMethod.objects.filter(user=user)


class IncomeForm(BaseTransactionForm):
    source = forms.CharField(widget=forms.TextInput(attrs={"class": "form-control"}))

    class Meta:
        model = Income
        fields = [
            "date",
            "amount",
            "category",
            "description",
            "payment_method",
            "notes",
            "source",
        ]


class FixedExpenseForm(BaseTransactionForm):
    is_paid = forms.BooleanField(required=False, widget=forms.CheckboxInput(attrs={"class": "form-check-input"}))
    due_day = forms.IntegerField(
        required=False,
        widget=forms.NumberInput(attrs={"class": "form-control", "min": 1, "max": 31}),
    )

    class Meta:
        model = FixedExpense
        fields = [
            "date",
            "amount",
            "category",
            "description",
            "payment_method",
            "notes",
            "is_paid",
            "due_day",
        ]


class VariableExpenseForm(BaseTransactionForm):
    expense_type = forms.ChoiceField(
        choices=VariableExpense.TYPE_CHOICES,
        widget=forms.Select(attrs={"class": "form-select"}),
    )

    class Meta:
        model = VariableExpense
        fields = [
            "date",
            "amount",
            "category",
            "description",
            "payment_method",
            "notes",
            "expense_type",
        ]


class SavingForm(BaseTransactionForm):
    saving_type = forms.ChoiceField(
        choices=Saving.SAVING_TYPE_CHOICES,
        widget=forms.Select(attrs={"class": "form-select"}),
    )
    goal_name = forms.CharField(required=False, widget=forms.TextInput(attrs={"class": "form-control"}))
    goal_amount = forms.DecimalField(
        required=False,
        widget=forms.NumberInput(attrs={"class": "form-control", "step": "0.01"}),
    )

    class Meta:
        model = Saving
        fields = [
            "date",
            "amount",
            "category",
            "description",
            "payment_method",
            "notes",
            "saving_type",
            "goal_name",
            "goal_amount",
        ]
