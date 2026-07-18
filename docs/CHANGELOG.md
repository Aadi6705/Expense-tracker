# CHANGELOG.md

All notable changes to FinanceFlow are logged here, most recent first. This is separate from `Memory.md`: **Memory** tracks *why* decisions were made; **Changelog** tracks *what* changed and *when*.

---

## [Unreleased]

### Added
- `docs/` suite: `PRD.md`, `Architecture.md`, `Rules.md`, `Phases.md`, `Design.md`, `Memory.md`, `CHANGELOG.md` — formalizes prior ad hoc progress into a structured reference set.

### In Progress
- Smart Budget API (`/api/budgets/<category_id>/status`) to replace placeholder data in the Budget Intelligence frontend components (Phase 3).

---

## Prior Progress (Retroactively Logged)

### Phase 2 — Budget Planner
- Added Budget create/edit/delete
- Added monthly allocation per category
- Added remaining-budget calculation, progress bar, utilization %
- Added category cards and summary cards
- Added Dashboard KPIs: total income, total expense, balance, monthly summary, charts, budget summary
- Added Budget Intelligence frontend components (impact panel, live preview, progress bar, status card) — placeholder API integration only

### Phase 1 — Expense Tracker
- Flask backend, SQLAlchemy, SQLite set up
- Bootstrap 5 UI, professional dashboard shell
- Add/Edit/Delete transaction
- Categories, payment method, notes, date fields
- Income & expense support

---

*Format guide: use `Added`, `Changed`, `Fixed`, `Removed` headings under each dated or phase-based section. Every entry here should correspond to something a user or developer would actually notice.*
