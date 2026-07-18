# Memory.md — Project Memory & Decision Log

**Purpose:** This is the file to read first in any new session — human or AI. It captures where the project stands right now and the decisions already made, so nobody re-derives the architecture from scratch or contradicts a past decision by accident.

**Last updated:** 2026-07-18

---

## 1. Current State (Read This First)

- **Current phase:** Phase 3 — Smart Budget Integration (🟡 in progress)
- **What's fully working:** Expense tracking (add/edit/delete, categories, payment method, notes, income+expense), Budget Planner (create/edit/delete, monthly allocation, remaining budget, progress bar, utilization %), Dashboard KPIs (total income/expense/balance, monthly summary, charts, budget summary)
- **What's partially built:** Budget Intelligence frontend components (impact panel, live preview, progress bar, status card) exist but are wired to **placeholder data**, not the real API yet.
- **What's actively being built:** The Budget API endpoint(s) that will replace those placeholders and make the Expense Module and Budget Planner update each other in real time.
- **Immediate next step:** Build `/api/budgets/<category_id>/status` (or equivalent) in `routes/api.py`, backed by `services/budget_engine.py`, and point the existing frontend live-preview JS at it.

## 2. Key Architectural Decisions

1. **Scope evolution:** The project has evolved from a simple Expense Tracker into a full Personal Finance Management System (FinanceFlow). This was a deliberate scope decision, not scope creep — see `PRD.md` Section 2 (Vision).
2. **Tight expense↔budget integration:** Expenses and Budgets are not independent modules. Every expense immediately reflects its impact on the relevant budget category. This is the reason Phase 3 exists before Analytics/Forecasting.
3. **No redundant calculations:** All financial metrics (remaining budget, utilization %, totals, trends) are computed dynamically from the database at request time, never stored as separate columns. See `Rules.md` Section 1 (Golden Rule).
4. **Dashboard as hub:** The Dashboard is the central financial overview. Expenses, Budgets, Reports, and Analytics all consume shared calculations from the Financial Analytics Engine (`services/`) rather than each computing their own version.
5. **Stack lock-in:** Flask + Blueprints, SQLAlchemy, SQLite (dev), Bootstrap 5, Chart.js, vanilla JS + Fetch API. No jQuery, no frontend framework swap. Decided to keep this a server-rendered app deliberately — see `Architecture.md` Section 1 and `Rules.md` Section 6.
6. **Async UI updates:** Wherever an interaction is naturally async (e.g. budget live preview on expense entry), the UI should update via Fetch without a full page reload — not a hard requirement everywhere, but the default preference.
7. **Phased build order is intentional:** Forecasting depends on Analytics; the AI Assistant (Phase 10) is deliberately last because it's meant to call into the existing service layer rather than duplicate logic. Don't build a later phase early "because it's easy" without updating this file to explain why the sequencing changed.
8. **Portfolio dual-purpose:** The project is being built to serve as both a college major project submission and a professional portfolio piece — this affects how much documentation/polish matters relative to a purely personal tool.

## 3. Open Questions / Not Yet Decided

- Exact currency to standardize on for display (₹ appears in some examples, $ in others) — pick one and apply consistently before Phase 4.
- Whether Forecasting (Phase 6) will use simple trend extrapolation only, or eventually a proper statistical/ML model — current default assumption is "simple first" (see `Phases.md`).
- Whether multi-user support will ever be in scope — currently explicitly out of scope (`PRD.md` Section 8), but flagged here in case that changes.

## 4. How to Use This File

- **At the start of a session:** read Section 1 to know exactly where things stand before touching code.
- **After a meaningful change:** add a dated entry below (Section 5) and update Section 1 if the current phase/next-step has changed.
- **Before making an architectural change:** check Section 2 — if you're about to contradict a listed decision, that needs to be called out explicitly, not silently overridden.

## 5. Session Log

| Date | Change | Notes |
|---|---|---|
| 2026-07-18 | Documentation suite created (PRD, Architecture, Rules, Phases, Design, Memory) | Formalized existing ad hoc progress into structured docs. No code changes. |

*(Add a new row above this line after each meaningful working session.)*
