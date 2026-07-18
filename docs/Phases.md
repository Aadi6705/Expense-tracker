# Phases.md — Development Phases

**Purpose:** Break the build into sequenced, self-contained phases so work (human or AI-assisted) stays coherent instead of ad hoc. Do not start a phase until the previous one is functionally complete, unless explicitly agreed otherwise.

**Last updated:** 2026-07-18

---

## Status Legend
✔ Complete · 🟡 In Progress · ⬜ Not Started

---

## Phase 1 — Expense Tracker ✔ Complete

- Flask backend, SQLAlchemy, SQLite
- Bootstrap 5 UI, professional dashboard shell
- Add / Edit / Delete transaction
- Categories, payment method, notes, date
- Income & expense support

## Phase 2 — Budget Planner ✔ Complete

- Create / Edit / Delete budget
- Monthly allocation per category
- Remaining budget calculation
- Progress bar, utilization %
- Category cards, summary cards
- Dashboard KPIs (total income, total expense, balance, monthly summary, charts, budget summary)
- Budget Intelligence frontend components (impact panel, live preview, progress bar, status card) — built with placeholder API integration

## Phase 3 — Smart Budget Integration 🟡 In Progress

**Goal:** Connect the Budget Planner and Expense Module in real time so every logged transaction immediately reflects in that category's budget status — no page refresh.

**Remaining work:**
- [ ] Budget API (`routes/api.py`: `/api/budgets/<category_id>/status`)
- [ ] Wire live preview components to the real API (replace placeholder data)
- [ ] Dynamic progress bar updates on transaction submit
- [ ] Smart alerts (e.g. "This will put you over budget for Groceries")

**Exit criteria:** logging an expense updates the relevant budget card's progress bar and status without a full page reload, using live data from the database.

## Phase 4 — Financial Intelligence ⬜ Not Started

- Budget Health Score (single composite score per month)
- Spending Insights (plain-language observations, e.g. "You spent 30% more on Dining this month")
- Smart Recommendations (rule-based, not ML, at this stage)
- Category Performance (over/under budget by category, month over month)
- Daily Spending view
- Savings Rate calculation

**Depends on:** Phase 3's real-time budget API being stable.

## Phase 5 — Professional Analytics ⬜ Not Started

Charts (Chart.js, shared palette):
- Budget vs Actual
- Income vs Expense
- Monthly Trend
- Category Trend
- Cash Flow
- Savings Trend
- Expense Heatmap
- Top Categories

## Phase 6 — Forecasting ⬜ Not Started

- Expected month-end spending (based on current-month pace)
- Budget exhaustion date (per category, if trend continues)
- Future savings projection
- Category-level forecast

**Note:** simple trend-based projection first (e.g. linear extrapolation from days elapsed); do not reach for a full ML pipeline unless the simple model proves insufficient.

## Phase 7 — Reports ⬜ Not Started

- Monthly report
- Yearly report
- Export to PDF
- Export to CSV
- Financial summary view

## Phase 8 — Savings Goals ⬜ Not Started

- Emergency Fund, Vacation Fund, custom named goals
- Progress tracking per goal
- Contribution history

## Phase 9 — Recurring Transactions ⬜ Not Started

- Salary, Rent, Subscriptions, EMIs, SIPs, Bills
- Auto-generation of recurring entries on schedule
- Edit/cancel a recurring series without affecting past entries

## Phase 10 — AI Finance Assistant ⬜ Not Started

- Natural-language queries over the user's own data, e.g.:
  - "Where did I spend most this month?"
  - "Can I afford a ₹50,000 laptop?"
  - "Which category wastes the most money?"
  - "Suggest next month's budget."
- Should be implemented as a consumer of the existing `services/` engine layer (Section 7, `Architecture.md`) — not a parallel calculation system.

---

## Sequencing Notes

- Phases 4 and 5 can be developed in parallel once Phase 3 is done, since Analytics mostly reads from the same engine Intelligence introduces.
- Phase 6 (Forecasting) depends on Phase 5's trend data being available and correct.
- Phase 10 (AI Assistant) should be the last phase — it depends on every other engine being stable and correctly abstracted, since it will call into all of them.
- If a phase is blocked, document why in `Memory.md` rather than skipping ahead silently.
