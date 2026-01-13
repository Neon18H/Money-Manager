# FinanceHub (Money-Manager)

Plataforma web en **Django 5.x** para control financiero personal con módulos de ingresos, gastos fijos, gastos variables y ahorros. Incluye dashboards con KPIs y gráficos (Chart.js), autenticación y filtros por mes/año.

## Estructura

```
financehub/
├─ accounts/
├─ config/
├─ dashboards/
├─ transactions/
├─ templates/
├─ static/
├─ manage.py
└─ financehub/
```

## Requisitos

- Python 3.11+
- PostgreSQL (producción) o SQLite (desarrollo)

## Instalación rápida

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

## Configuración

### Desarrollo (SQLite por defecto)
No requiere variables adicionales.

### Producción (PostgreSQL vía variables de entorno)

```bash
export POSTGRES_DB=financehub
export POSTGRES_USER=financehub
export POSTGRES_PASSWORD=secret
export POSTGRES_HOST=localhost
export POSTGRES_PORT=5432
export DJANGO_SECRET_KEY=change-me
export DJANGO_DEBUG=False
export DJANGO_ALLOWED_HOSTS=your-domain.com
```

## Ejecutar

```bash
cd financehub
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

## Crear datos demo

```bash
python manage.py seed_demo
```

Usuario demo: `demo` / `demo1234`.

## Rutas principales

- `/` → redirige a `/dashboards/general/`
- `/dashboards/general/`
- `/dashboards/incomes/`
- `/dashboards/fixed-expenses/`
- `/dashboards/variable-expenses/`
- `/dashboards/savings/`

CRUD:

- `/incomes/`
- `/fixed-expenses/`
- `/variable-expenses/`
- `/savings/`

## Notas

- Todas las vistas requieren login.
- Cada usuario solo ve sus datos.
- Las categorías y medios de pago se gestionan en el admin de Django.
