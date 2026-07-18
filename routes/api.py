

from datetime import date

from flask import Blueprint, jsonify
from sqlalchemy import func

from models.database import Budget, Expense, db

api_bp = Blueprint("api", __name__, url_prefix="/api")


@api_bp.route("/budget/<string:category>")
def budget_details(category):
    """Return live budget metrics for a category for the current month."""
    today = date.today()

    budget = Budget.query.filter_by(category=category).first()
    if not budget:
        return jsonify({"error": "Budget not found"}), 404

    spent = (
        db.session.query(func.coalesce(func.sum(Expense.amount), 0))
        .filter(
            Expense.transaction_type == "Expense",
            Expense.category == category,
            func.extract("year", Expense.date) == today.year,
            func.extract("month", Expense.date) == today.month,
        )
        .scalar()
        or 0
    )

    monthly_budget = float(budget.monthly_budget)
    spent = float(spent)
    remaining = max(monthly_budget - spent, 0)
    usage_percent = 0 if monthly_budget == 0 else round((spent / monthly_budget) * 100, 1)
    daily_average = round(spent / max(today.day, 1), 2)
    projected_spending = round(daily_average * 30, 2)

    if usage_percent < 75:
        status = "On Track"
    elif usage_percent < 100:
        status = "Near Limit"
    else:
        status = "Exceeded"

    return jsonify(
        {
            "category": category,
            "monthly_budget": monthly_budget,
            "spent": spent,
            "remaining": remaining,
            "usage_percent": usage_percent,
            "status": status,
            "daily_average": daily_average,
            "projected_spending": projected_spending,
        }
    )