# PRD.md — Product Requirements Document

**Project:** FinanceFlow — Intelligent Personal Finance Management System
**Working alternates:** BudgetIQ, FinSight, PocketPilot, SpendWise
**Status:** Active development
**Last updated:** 2026-07-18

---

## 1. Problem Statement

Most personal expense trackers only record transactions after the fact. They tell you what you spent, not what it means, whether you're on track, or what to do next. FinanceFlow is built to close that gap: a system that tracks money in and out, but also actively interprets that data to help the user make better financial decisions in real time.

## 2. Vision

FinanceFlow is not a CRUD expense tracker. It is a personal finance management platform that helps users understand, control, and improve their financial habits through:

- Real-time budget tracking
- Intelligent spending analysis
- Predictive/forecasting insights
- Actionable financial recommendations

Every transaction the user logs should immediately answer a question, not just add a row to a table.

## 3. Target Users

| User type | Need |
|---|---|
| Student / early-career individual | Simple budgeting, avoid overspending, build saving habits |
| College submission reviewer | A well-architected, portfolio-quality full-stack project |
| Personal end user (you) | A daily-use tool that tells you where you stand financially, not just where you've been |

## 4. Objectives

The system should help users:

1. Track income and expenses
2. Plan monthly budgets
3. Monitor spending in real time
4. Prevent budget overspending
5. Improve saving habits
6. Analyze financial behavior
7. Predict future spending
8. Generate financial reports
9. Receive intelligent recommendations

## 5. Core Principle

**Every page must answer a financial question.**

| Page | Question it answers |
|---|---|
| Dashboard | How healthy are my finances? |
| Expenses | Where is my money going? |
| Budget | Can I still spend? |
| Reports | How did I perform this month? |
| Analytics | What trends exist? |
| AI Assistant | What should I do next? |

If a feature doesn't clearly answer one of these questions for the user, it doesn't belong on that page.

## 6. Functional Requirements

### 6.1 Completed (Current Baseline)

**Core System**
- Flask backend
- SQLAlchemy ORM
- SQLite database
- Bootstrap 5 UI
- Professional dashboard

**Expense Module**
- Add / Edit / Delete transaction
- Categories, payment method, notes, date
- Income & expense support (both transaction types)

**Budget Module**
- Create / Edit / Delete budget
- Monthly allocation per category
- Remaining budget calculation
- Progress bar + utilization %
- Category cards, summary cards

**Dashboard**
- Total income, total expense, balance
- Monthly summary
- Charts (Chart.js)
- Budget summary

**UI**
- Professional blue theme, Bootstrap Icons, responsive layout, professional navbar

**Budget Intelligence (frontend, partial)**
- Budget impact panel, live preview components, progress bar, budget status card (placeholder API integration — not yet wired to real data)

### 6.2 In Progress

**Smart Budget API** — connects the Budget Planner and Expense Module in real time, so logging an expense immediately updates that category's remaining budget and status, without a page refresh.

### 6.3 Planned (see `Phases.md` for sequencing)

- Financial Intelligence: budget health score, spending insights, smart recommendations, category performance, daily spending, savings rate
- Professional Analytics: budget vs actual, income vs expense, monthly/category trend, cash flow, savings trend, expense heatmap, top categories
- Forecasting: expected month-end spend, budget exhaustion date, future savings projection, category forecast
- Reports: monthly/yearly report, export to PDF/CSV, financial summary
- Savings Goals: emergency fund, vacation fund, custom goals, progress tracking
- Recurring Transactions: salary, rent, subscriptions, EMIs, SIPs, bills
- AI Finance Assistant: natural-language queries over the user's own data (e.g. "Where did I spend most this month?", "Can I afford a ₹50,000 laptop?")

## 7. Non-Functional Requirements

- **Performance:** dashboard and budget pages must load without visible lag on a local SQLite dataset of a few thousand transactions.
- **Data integrity:** no financial figure should ever be stored redundantly if it can be derived — see `Rules.md`.
- **Usability:** every new feature must fit the existing visual language (see `Design.md`) — no visual regressions.
- **Maintainability:** feature additions follow the phase sequence in `Phases.md`; nothing is bolted on ad hoc.
- **Portfolio quality:** code and docs should be presentable as-is in a GitHub repo and a college submission.

## 8. Out of Scope (for now)

- Multi-user accounts / authentication (single-user app until explicitly scoped in a future phase)
- Real bank account integration (Plaid-style) — all data is manually entered or CSV-imported
- Mobile app — web-responsive only
- Multi-currency support

## 9. Success Criteria

A feature is "done" when:
1. It answers its page's core question (Section 5)
2. It uses dynamically calculated data, not hardcoded or duplicated values
3. It matches the design system in `Design.md`
4. It's reflected in `Memory.md` and `CHANGELOG.md`
