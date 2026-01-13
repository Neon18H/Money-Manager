import random
from datetime import date, timedelta
from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from config.models import Category, PaymentMethod
from transactions.models import Income, FixedExpense, VariableExpense, Saving

User = get_user_model()


class Command(BaseCommand):
    help = 'Crea datos demo para FinanceHub.'

    def handle(self, *args, **options):
        user, created = User.objects.get_or_create(username='demo')
        if created:
            user.set_password('demo1234')
            user.save()

        categories = {
            'INCOME': ['Salario', 'Freelance', 'Negocio'],
            'FIXED': ['Renta', 'Servicios', 'Internet'],
            'VARIABLE': ['Supermercado', 'Transporte', 'Ocio'],
            'SAVING': ['Fondo emergencia', 'Inversión'],
        }
        for kind, names in categories.items():
            for name in names:
                Category.objects.get_or_create(user=user, name=name, kind=kind)

        for name in ['Efectivo', 'Tarjeta', 'Transferencia']:
            PaymentMethod.objects.get_or_create(user=user, name=name)

        payment_methods = list(PaymentMethod.objects.filter(user=user))
        start_date = date.today() - timedelta(days=180)
        for i in range(180):
            current_date = start_date + timedelta(days=i)
            if random.random() < 0.4:
                Income.objects.create(
                    user=user,
                    date=current_date,
                    amount=random.randint(500, 2000),
                    category=Category.objects.filter(user=user, kind='INCOME').order_by('?').first(),
                    description='Ingreso demo',
                    payment_method=random.choice(payment_methods),
                    notes='Demo',
                    source='Salario',
                )
            if random.random() < 0.3:
                FixedExpense.objects.create(
                    user=user,
                    date=current_date,
                    amount=random.randint(100, 600),
                    category=Category.objects.filter(user=user, kind='FIXED').order_by('?').first(),
                    description='Gasto fijo demo',
                    payment_method=random.choice(payment_methods),
                    notes='Demo',
                    is_paid=random.choice([True, False]),
                    due_day=current_date.day,
                )
            if random.random() < 0.5:
                VariableExpense.objects.create(
                    user=user,
                    date=current_date,
                    amount=random.randint(20, 200),
                    category=Category.objects.filter(user=user, kind='VARIABLE').order_by('?').first(),
                    description='Gasto variable demo',
                    payment_method=random.choice(payment_methods),
                    notes='Demo',
                    expense_type=random.choice(['NECESARIO', 'GUSTO']),
                )
            if random.random() < 0.2:
                Saving.objects.create(
                    user=user,
                    date=current_date,
                    amount=random.randint(50, 300),
                    category=Category.objects.filter(user=user, kind='SAVING').order_by('?').first(),
                    description='Ahorro demo',
                    payment_method=random.choice(payment_methods),
                    notes='Demo',
                    saving_type=random.choice(['AHORRO', 'INVERSION', 'FONDO']),
                    goal_name='Meta demo',
                    goal_amount=5000,
                )

        self.stdout.write(self.style.SUCCESS('Datos demo creados para usuario demo / demo1234'))
