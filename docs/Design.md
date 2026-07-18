# Design.md — Visual Design Guidelines

**Purpose:** Single source of truth for colors, typography, and UI conventions so every new page/feature looks like it belongs to the same product.

**Last updated:** 2026-07-18

---

## 1. Design Philosophy

Professional. Minimal. Trustworthy. This is a finance tool — it should read like something a bank or fintech product would ship, not a hobby project. No unnecessary emojis, no playful illustration style, no clutter.

## 2. Color Palette

**Primary theme: Professional Blue**

| Token | Hex | Usage |
|---|---|---|
| `--primary` | `#0D6EFD` (Bootstrap blue) or a custom deeper `#1B4F72` | Primary actions, active nav, key highlights |
| `--primary-dark` | `#0A3D62` | Navbar, headers, emphasis text |
| `--success` | `#198754` | Under-budget status, positive trends, income |
| `--warning` | `#FFC107` | Approaching budget limit |
| `--danger` | `#DC3545` | Over budget, negative trends, expense highlights |
| `--neutral-bg` | `#F5F7FA` | Page background |
| `--surface` | `#FFFFFF` | Cards, panels |
| `--text-primary` | `#1C1F26` | Body text |
| `--text-muted` | `#6C757D` | Secondary text, labels |
| `--border` | `#E3E6EA` | Card borders, dividers |

**Rule:** Every chart (Chart.js) uses this same palette — no chart introduces its own one-off colors. Income/positive = `--success`, Expense/negative = `--danger`, neutral categories cycle through a fixed set of secondary blues/teals, not random Chart.js defaults.

## 3. Typography

| Role | Font | Notes |
|---|---|---|
| Headings | System sans-serif stack (e.g. `"Segoe UI", Roboto, sans-serif`) or Bootstrap default | Bold, clear hierarchy — h1 for page title, h2 for section, no skipping levels |
| Body | Same sans-serif stack | 15–16px base size |
| Numbers / figures | Tabular/monospace-leaning where possible (e.g. `"Roboto Mono"` for amounts in tables) | Keeps currency columns aligned |

Keep to Bootstrap's default type scale rather than introducing custom font sizes ad hoc — consistency matters more than novelty here.

## 4. Layout Conventions

- **Cards** for every discrete unit of information (a budget category, a KPI, a chart) — consistent border-radius and shadow across the app.
- **Summary cards** at the top of a page (Dashboard, Budget) — KPI number, label, small trend indicator.
- **Progress bars** for budget utilization: green under 70%, yellow 70–100%, red over 100%. Same thresholds everywhere a progress bar appears.
- **Navbar**: fixed, professional, blue accent, current page indicated clearly (active state, not just color).
- **Spacing**: use Bootstrap's spacing utilities (`m-*`, `p-*`, `gap-*`) — don't hand-write custom margin/padding values.
- **Responsive**: cards reflow to single column below `md` breakpoint; charts resize rather than overflow.

## 5. Iconography

- Bootstrap Icons only, used sparingly and functionally (e.g. an arrow-up/down next to a trend number, a category icon on a budget card) — never decoratively.

## 6. Status Language

Consistent status vocabulary across the app:

| State | Label | Color |
|---|---|---|
| Under budget, healthy | "On track" | `--success` |
| Approaching limit (70–100%) | "Near limit" | `--warning` |
| Over budget | "Over budget" | `--danger` |

Use this exact vocabulary everywhere a budget/category status is shown — dashboard, budget page, live preview, alerts. Don't introduce synonyms per page.

## 7. Chart Guidelines (Chart.js)

- Same color palette as Section 2, every chart.
- Consistent chart type per data shape: trends over time → line chart; category comparison → bar or doughnut; single KPI → number card, not a chart.
- Tooltips formatted as currency (`₹` or `$`, matching whatever the user's data uses) — never raw unformatted numbers.
- Legends only when there are 3+ series; otherwise label directly.

## 8. What to Avoid

- No gradients-as-decoration, no drop shadows beyond Bootstrap's default card elevation.
- No emoji in buttons, headers, or status badges.
- No more than one accent color competing with the primary blue on a single page.
- No chart color palette that doesn't match Section 2.
