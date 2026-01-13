# Money Manager

Plataforma web en **Django** para control financiero personal con módulos de ingresos, gastos fijos, gastos variables y ahorros. Incluye dashboards con KPIs y gráficos (Chart.js), autenticación con Django y filtros por mes/año.

## Requisitos

- Python 3.11+
- SQLite (por defecto en Django)

## Instalación rápida

```bash
python -m venv .venv
source .venv/bin/activate
pip install django
```

## Ejecutar

```bash
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

## Rutas principales

- `/` → Dashboard general
- `/dashboard/ingresos/`
- `/dashboard/gastos-fijos/`
- `/dashboard/gastos-variables/`
- `/dashboard/ahorros/`

CRUD:

- `/ingresos/`
- `/gastos-fijos/`
- `/gastos-variables/`
- `/ahorros/`

## Notas

- Todas las vistas requieren login.
- Cada usuario solo ve sus datos.
- Las categorías y medios de pago se gestionan en el admin de Django.
- Usa Bootstrap 5 y Chart.js vía CDN.
