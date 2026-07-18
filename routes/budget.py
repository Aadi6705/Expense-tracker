from flask import Blueprint, render_template, request, redirect, url_for, flash, abort
from datetime import date
from sqlalchemy import func
from models.database import db, Budget, Expense

budget_bp = Blueprint("budget", __name__, url_prefix="/budgets")


@budget_bp.route("/")
def list_budgets():
    # Load budgets
    budgets = Budget.query.order_by(Budget.category.asc()).all()

    today = date.today()

    total_planned = 0
    total_spent = 0

    # Calculate current-month budget metrics
    for budget in budgets:
        spent = db.session.query(func.coalesce(func.sum(Expense.amount), 0)).filter(
            Expense.transaction_type == "Expense",
            Expense.category == budget.category,
            func.extract("year", Expense.date) == today.year,
            func.extract("month", Expense.date) == today.month,
        ).scalar() or 0

        spent = float(spent)
        monthly_budget = float(budget.monthly_budget)

        remaining = max(monthly_budget - spent, 0)
        usage_percent = 0 if monthly_budget == 0 else min((spent / monthly_budget) * 100, 100)

        budget.daily_average = round(spent / max(today.day, 1), 2)
        budget.projected_spending = round((spent / max(today.day, 1)) * 30, 2)

        if usage_percent < 75:
            status = "On Track"
        elif usage_percent < 100:
            status = "Near Limit"
        else:
            status = "Exceeded"

        budget.spent = spent
        budget.remaining = remaining
        budget.usage_percent = round(usage_percent, 1)
        budget.status = status

        total_planned += monthly_budget
        total_spent += spent

    # Build dashboard summary
    summary = {
        "total_budgets": len(budgets),
        "total_planned": total_planned,
        "total_spent": total_spent,
        "total_remaining": max(total_planned - total_spent, 0),
        "overall_usage": round((total_spent / total_planned) * 100, 1) if total_planned else 0,
        "over_budget_categories": len([b for b in budgets if b.status == "Exceeded"]),
        "healthy_categories": len([b for b in budgets if b.status == "On Track"]),
    }

    # Render page
    return render_template(
        "pages/budget.html",
        budgets=budgets,
        summary=summary,
    )


@budget_bp.route("/add", methods=["POST"])
def add_budget():
    category = request.form.get("category", "").strip().title()
    monthly_budget = request.form.get("monthly_budget", "").strip()

    if not category or not monthly_budget:
        flash("Category and monthly budget are required.", "warning")
        return redirect(url_for("budget.list_budgets"))

    existing = Budget.query.filter_by(category=category).first()
    if existing:
        flash(
            f'Budget for "{category}" already exists. You can edit the existing budget instead.',
            "warning",
        )
        return redirect(url_for("budget.list_budgets"))

    budget = Budget(category=category, monthly_budget=monthly_budget)
    db.session.add(budget)
    try:
        db.session.commit()
        flash("Budget added successfully.", "success")
    except Exception:
        db.session.rollback()
        flash("Unable to save changes. Please try again.", "danger")

    return redirect(url_for("budget.list_budgets"))


# Edit budget route
@budget_bp.route("/edit/<int:budget_id>", methods=["POST"])
def edit_budget(budget_id):
    budget = Budget.query.get_or_404(budget_id)

    monthly_budget = request.form.get("monthly_budget", "").strip()

    if not monthly_budget:
        flash("Monthly budget is required.", "warning")
        return redirect(url_for("budget.list_budgets"))

    budget.monthly_budget = monthly_budget

    try:
        db.session.commit()
        flash("Budget updated successfully.", "success")
    except Exception:
        db.session.rollback()
        flash("Unable to update budget. Please try again.", "danger")

    return redirect(url_for("budget.list_budgets"))


@budget_bp.route("/delete/<int:budget_id>", methods=["POST"])
def delete_budget(budget_id):
    budget = Budget.query.get_or_404(budget_id)
    db.session.delete(budget)
    try:
        db.session.commit()
        flash("Budget deleted successfully.", "success")
    except Exception:
        db.session.rollback()
        flash("Unable to save changes. Please try again.", "danger")

    return redirect(url_for("budget.list_budgets"))