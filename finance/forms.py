from django import forms

from .models import Category, FixedExpense, Income, Saving, VariableExpense


class BootstrapModelForm(forms.ModelForm):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            if isinstance(field.widget, forms.CheckboxInput):
                existing = field.widget.attrs.get("class", "")
                field.widget.attrs["class"] = f"{existing} form-check-input".strip()
                continue
            existing = field.widget.attrs.get("class", "")
            field.widget.attrs["class"] = f"{existing} form-control".strip()


class IncomeForm(BootstrapModelForm):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.fields["category"].queryset = Category.objects.filter(kind=Category.Kind.INCOME)

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
        widgets = {
            "date": forms.DateInput(attrs={"type": "date"}),
            "notes": forms.Textarea(attrs={"rows": 3}),
        }


class FixedExpenseForm(BootstrapModelForm):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.fields["category"].queryset = Category.objects.filter(kind=Category.Kind.FIXED)

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
        widgets = {
            "date": forms.DateInput(attrs={"type": "date"}),
            "notes": forms.Textarea(attrs={"rows": 3}),
        }


class VariableExpenseForm(BootstrapModelForm):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.fields["category"].queryset = Category.objects.filter(kind=Category.Kind.VARIABLE)

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
        widgets = {
            "date": forms.DateInput(attrs={"type": "date"}),
            "notes": forms.Textarea(attrs={"rows": 3}),
        }


class SavingForm(BootstrapModelForm):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.fields["category"].queryset = Category.objects.filter(kind=Category.Kind.SAVING)

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
        widgets = {
            "date": forms.DateInput(attrs={"type": "date"}),
            "notes": forms.Textarea(attrs={"rows": 3}),
        }
