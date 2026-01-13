from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from .models import Income, FixedExpense, VariableExpense, Saving
from .forms import IncomeForm, FixedExpenseForm, VariableExpenseForm, SavingForm
from config.models import Category, PaymentMethod


class UserQuerysetMixin(LoginRequiredMixin):
    def get_queryset(self):
        return super().get_queryset().filter(user=self.request.user)

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        if 'category' in form.fields:
            form.fields['category'].queryset = Category.objects.filter(user=self.request.user)
        if 'payment_method' in form.fields:
            form.fields['payment_method'].queryset = PaymentMethod.objects.filter(user=self.request.user)
        return form


class IncomeListView(UserQuerysetMixin, ListView):
    model = Income
    paginate_by = 10
    template_name = 'transactions/income_list.html'


class IncomeCreateView(UserQuerysetMixin, CreateView):
    model = Income
    form_class = IncomeForm
    success_url = reverse_lazy('income_list')
    template_name = 'transactions/income_form.html'


class IncomeUpdateView(UserQuerysetMixin, UpdateView):
    model = Income
    form_class = IncomeForm
    success_url = reverse_lazy('income_list')
    template_name = 'transactions/income_form.html'


class IncomeDeleteView(UserQuerysetMixin, DeleteView):
    model = Income
    success_url = reverse_lazy('income_list')
    template_name = 'transactions/confirm_delete.html'


class FixedExpenseListView(UserQuerysetMixin, ListView):
    model = FixedExpense
    paginate_by = 10
    template_name = 'transactions/fixed_expense_list.html'


class FixedExpenseCreateView(UserQuerysetMixin, CreateView):
    model = FixedExpense
    form_class = FixedExpenseForm
    success_url = reverse_lazy('fixed_expense_list')
    template_name = 'transactions/fixed_expense_form.html'


class FixedExpenseUpdateView(UserQuerysetMixin, UpdateView):
    model = FixedExpense
    form_class = FixedExpenseForm
    success_url = reverse_lazy('fixed_expense_list')
    template_name = 'transactions/fixed_expense_form.html'


class FixedExpenseDeleteView(UserQuerysetMixin, DeleteView):
    model = FixedExpense
    success_url = reverse_lazy('fixed_expense_list')
    template_name = 'transactions/confirm_delete.html'


class VariableExpenseListView(UserQuerysetMixin, ListView):
    model = VariableExpense
    paginate_by = 10
    template_name = 'transactions/variable_expense_list.html'


class VariableExpenseCreateView(UserQuerysetMixin, CreateView):
    model = VariableExpense
    form_class = VariableExpenseForm
    success_url = reverse_lazy('variable_expense_list')
    template_name = 'transactions/variable_expense_form.html'


class VariableExpenseUpdateView(UserQuerysetMixin, UpdateView):
    model = VariableExpense
    form_class = VariableExpenseForm
    success_url = reverse_lazy('variable_expense_list')
    template_name = 'transactions/variable_expense_form.html'


class VariableExpenseDeleteView(UserQuerysetMixin, DeleteView):
    model = VariableExpense
    success_url = reverse_lazy('variable_expense_list')
    template_name = 'transactions/confirm_delete.html'


class SavingListView(UserQuerysetMixin, ListView):
    model = Saving
    paginate_by = 10
    template_name = 'transactions/saving_list.html'


class SavingCreateView(UserQuerysetMixin, CreateView):
    model = Saving
    form_class = SavingForm
    success_url = reverse_lazy('saving_list')
    template_name = 'transactions/saving_form.html'


class SavingUpdateView(UserQuerysetMixin, UpdateView):
    model = Saving
    form_class = SavingForm
    success_url = reverse_lazy('saving_list')
    template_name = 'transactions/saving_form.html'


class SavingDeleteView(UserQuerysetMixin, DeleteView):
    model = Saving
    success_url = reverse_lazy('saving_list')
    template_name = 'transactions/confirm_delete.html'
