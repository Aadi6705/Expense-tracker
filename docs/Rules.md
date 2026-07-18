# Rules.md — Development Rules & AI Boundaries

**Purpose:** This file sets hard boundaries for anyone (human or AI) contributing code to FinanceFlow. When in doubt, follow this file over general best practices — it reflects decisions already made for this specific project.

**Last updated:** 2026-07-18

---

## 1. Golden Rule

**Never duplicate a calculation.** If a number can be derived from the database, it must be derived — every time, dynamically — never stored redundantly and never recomputed slightly differently in two places. Budget remaining, utilization %, totals, trends: all of it comes from `services/analytics_engine.py` or `services/budget_engine.py`, called fresh, every time.

If you (or the AI) are about to write a second version of a calculation that already exists somewhere else in the codebase — stop. Import the existing one instead.

## 2. Backend Rules

- **Flask Blueprints only** — no monolithic `app.py` with all routes. Every feature area gets its own blueprint in `routes/`.
- **SQLAlchemy ORM only** — no raw SQL strings unless there's a specific, documented performance reason, and even then it goes through a service function, not inline in a route.
- **Service-layer logic** — business logic belongs in `services/`, never in a route function and never in a template.
- **REST-style API endpoints** — `routes/api.py` should read like a predictable REST surface (`/api/budgets/<id>/status`, not `/api/getBudgetStatusForId`).
- **Validation on every input** — every form submission and API payload is validated server-side before it touches the database, regardless of any client-side validation already done.
- **Explicit error handling** — no bare `except:`. Catch specific exceptions, flash a clear user-facing message, and log the underlying error.

## 3. Database Rules

- Every new table needs a clear reason it can't be derived from an existing one.
- No calculated/derivable fields stored as columns (e.g. don't store `remaining_budget` — compute it from `allocation - sum(transactions)` at query time).
- Migrations should be used for schema changes once Flask-Migrate is introduced (Phase 3+) — no manually editing the SQLite file.

## 4. Frontend Rules

- **Bootstrap 5 only** for layout/components — no mixing in another CSS framework.
- **No jQuery.** Use the Fetch API and vanilla JS for all dynamic behavior.
- **Update the UI without a full page reload** wherever the interaction is naturally async (budget live preview, dashboard filters, form submissions that return status).
- **Separate JS files per feature** (`budget-live-preview.js`, `dashboard-charts.js`, etc.) — no giant shared `main.js` with unrelated logic mixed together.
- **Chart.js only**, same color palette across every chart on the site (see `Design.md`).

## 5. UI/UX Rules

- Professional, minimal — this is a finance tool, not a consumer app. No unnecessary emojis in the UI.
- Blue accent theme, consistent across every page (see `Design.md` for exact tokens).
- Responsive by default — every new page/component must be checked at mobile width before being considered done.
- Consistent spacing scale — don't introduce one-off margin/padding values; reuse the existing Bootstrap spacing utilities.

## 6. What the AI Should NOT Do

- Do not introduce a new frontend framework (React, Vue, etc.) — this is a server-rendered Flask + Bootstrap app by design.
- Do not add a new Python dependency without checking if the need can be met with what's already in `requirements.txt`.
- Do not build a feature ahead of its phase in `Phases.md` "because it's easy" — sequencing exists to keep the architecture coherent as it grows.
- Do not silently change an existing calculation's logic — if a figure's definition needs to change (e.g. how "utilization %" is computed), it must be called out explicitly, since other features may depend on the old definition.
- Do not hardcode sample/demo data into templates or routes — use the database, even for placeholders (seed scripts are fine, hardcoded HTML numbers are not).
- Do not remove or bypass validation to "make a demo work."

## 7. What the AI Should Always Do

- Check `Memory.md` at the start of a session before making architectural assumptions.
- Update `Memory.md` and `CHANGELOG.md` after any non-trivial change.
- Ask before completing a phase and starting the next one out of order.
- Point out if a request would violate the Golden Rule (Section 1) or duplicate existing logic, rather than silently complying.

## 8. Commit / Change Hygiene

- One logical feature per commit/change where practical.
- Every change that affects a calculation or a page's data flow gets a one-line entry in `CHANGELOG.md`.
- Every change that affects an architectural decision (not just a feature) gets a note in `Memory.md`.
