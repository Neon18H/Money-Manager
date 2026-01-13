# Money Manager

Plataforma Django para control financiero personal con dashboards por módulo.

## Requisitos
- Python 3.10+
- Django 4.2+

## Instalación
```bash
python -m venv .venv
source .venv/bin/activate
pip install django
```

## Ejecución
```bash
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

Luego ingresa a `http://127.0.0.1:8000/`.

## Configuración inicial
Crea categorías y métodos de pago en el admin de Django antes de registrar ingresos, gastos o ahorros.
