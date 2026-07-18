# Architecture.md — System Architecture

**Last updated:** 2026-07-18

---

## 1. Technical Stack

| Layer | Technology |
|---|---|
| Backend framework | Flask (Blueprints) |
| ORM | SQLAlchemy |
| Database | SQLite (dev) — swappable for PostgreSQL later without changing app code |
| Frontend | Bootstrap 5, Bootstrap Icons |
| Charts | Chart.js |
| Client-side interactivity | Vanilla JS, Fetch API (no jQuery) |
| Templating | Jinja2 |

## 2. High-Level Flow

```
                    Dashboard
                        │
        ┌───────────────┼────────────────┐
        │               │                │
        ▼               ▼                ▼
   Expenses       Budget Planner       Reports
        │               │                │
        └───────────────┼────────────────┘
                         │
                         ▼
              Financial Analytics Engine
                         │
        ┌────────────────┼─────────────────┐
        │                │                 │
        ▼                ▼                 ▼
   Budget API     Insights Engine    Forecast Engine
                         │
                         ▼
                Recommendation Engine
                         │
                         ▼
                  SQLAlchemy Database
                         │
                         ▼
                   SQLite Database
```

Every page-level module (Expenses, Budget, Reports) reads from and writes to the database through the **Financial Analytics Engine** — a shared calculation layer. No page computes its own version of a financial figure independently. This is the single most important architectural rule in the project (see `Rules.md`).

## 3. Folder Structure

```
FinanceFlow/
│
├── docs/
│   ├── PRD.md
│   ├── Architecture.md
│   ├── Rules.md
│   ├── Phases.md
│   ├── Design.md
│   ├── Memory.md
│   └── CHANGELOG.md
│
├── app.py                     # App factory / entry point
├── config.py                  # Environment + app configuration
├── extensions.py              # SQLAlchemy db instance, shared extensions
│
├── models/
│   ├── __init__.py
│   ├── transaction.py          # Income & expense records
│   ├── budget.py                # Monthly budget allocations per category
│   └── category.py              # Category definitions
│
├── routes/                     # Flask Blueprints — one per feature area
│   ├── __init__.py
│   ├── dashboard.py
│   ├── expenses.py
│   ├── budget.py
│   ├── analytics.py             # Phase 4+
│   ├── reports.py               # Phase 6+
│   ├── goals.py                 # Phase 7+
│   └── api.py                   # JSON endpoints consumed by Fetch calls
│
├── services/                   # Reusable business logic — the "Engine" layer
│   ├── __init__.py
│   ├── analytics_engine.py      # Shared calculations: totals, utilization, trends
│   ├── budget_engine.py         # Budget impact + status logic
│   ├── insights_engine.py       # Phase 3+
│   ├── forecast_engine.py       # Phase 5+
│   └── recommendation_engine.py # Phase 3+ / Phase 9
│
├── templates/
│   ├── base.html
│   ├── dashboard.html
│   ├── expenses.html
│   ├── budget.html
│   ├── analytics.html
│   ├── reports.html
│   └── goals.html
│
├── static/
│   ├── css/
│   │   └── style.css
│   ├── js/
│   │   ├── budget-live-preview.js
│   │   ├── dashboard-charts.js
│   │   └── api-client.js         # Shared fetch() wrapper
│   └── img/
│
├── instance/
│   └── financeflow.db
│
├── requirements.txt
└── README.md
```

## 4. Layering Rules

1. **Routes (`routes/`)** handle HTTP only: parse the request, call a service, return a response or render a template. No business logic lives in a route function.
2. **Services (`services/`)** contain all calculation logic. A route never computes a financial figure directly — it calls a service function.
3. **Models (`models/`)** are pure data definitions (SQLAlchemy models) plus simple query helpers. No aggregation logic belongs on a model.
4. **Templates** render what services/routes hand them. No calculation happens in Jinja beyond simple formatting (currency, dates).
5. **Static JS** calls `routes/api.py` endpoints via `fetch()` and updates the DOM. It never duplicates server-side calculation logic — if the UI needs a number, it asks the API for it.

## 5. Data Flow Example — Logging an Expense

1. User submits the expense form → `routes/expenses.py` receives POST
2. Route calls `services/budget_engine.py` to check the transaction against that category's monthly budget
3. Route calls `models/transaction.py` to persist the record
4. Route returns updated budget status (JSON, for the live preview) or redirects with a flash message
5. Frontend JS (`budget-live-preview.js`) updates the progress bar and status badge without a full page reload

## 6. Why SQLAlchemy Over Raw SQL

- Consistent model definitions across Expenses, Budget, Reports, and future modules
- Query composition (filters, joins) needed for Analytics/Forecast phases is much cleaner with the ORM
- Migrations (Flask-Migrate/Alembic) become available if the schema evolves

## 7. Extensibility Points

- **New chart type** → add a function to `analytics_engine.py`, expose via `routes/api.py`, consume in a new Chart.js instance. No changes needed elsewhere.
- **New forecast model** → lives entirely in `forecast_engine.py`; routes/templates just consume its output.
- **AI Assistant (Phase 9)** → will call into the same `services/` layer as its "tools," rather than reimplementing calculations — the assistant should be a new consumer of the Financial Analytics Engine, not a parallel system.
