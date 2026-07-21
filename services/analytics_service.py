from sqlalchemy import func
from models.database import db, Expense


def get_dashboard_summary():
    income = (
        db.session.query(func.coalesce(func.sum(Expense.amount), 0))
        .filter(Expense.transaction_type == "Income")
        .scalar()
    )

    expense = (
        db.session.query(func.coalesce(func.sum(Expense.amount), 0))
        .filter(Expense.transaction_type == "Expense")
        .scalar()
    )

    count = Expense.query.count()

    balance = income - expense

    recent_transactions = get_recent_transactions()
    category_summary = get_category_summary()
    monthly_summary = get_monthly_summary()
    financial_insights = get_financial_insights()

    return {
        "total_income": float(income),
        "total_expense": float(expense),
        "total_balance": float(balance),
        "transaction_count": count,
        "recent_transactions": recent_transactions,
        "category_summary": category_summary,
        "monthly_summary": monthly_summary,
        "financial_insights": financial_insights,
    }


def get_recent_transactions(limit=5):
    return (
        Expense.query
        .order_by(Expense.created_at.desc())
        .limit(limit)
        .all()
    )


def get_category_summary():
    results = (
        db.session.query(
            Expense.category,
            func.coalesce(func.sum(Expense.amount), 0)
        )
        .filter(Expense.transaction_type == "Expense")
        .group_by(Expense.category)
        .order_by(func.sum(Expense.amount).desc())
        .all()
    )

    return {
        "labels": [row[0] for row in results],
        "values": [float(row[1]) for row in results]
    }


def get_monthly_summary():
    results = (
        db.session.query(
            func.strftime("%Y-%m", Expense.date).label("month"),
            func.coalesce(func.sum(Expense.amount), 0)
        )
        .filter(Expense.transaction_type == "Expense")
        .group_by("month")
        .order_by("month")
        .all()
    )

    return {
        "labels": [row[0] for row in results],
        "values": [float(row[1]) for row in results]
    }
def get_financial_insights():
    total_income = (
        db.session.query(func.coalesce(func.sum(Expense.amount), 0))
        .filter(Expense.transaction_type == "Income")
        .scalar()
    )

    total_expense = (
        db.session.query(func.coalesce(func.sum(Expense.amount), 0))
        .filter(Expense.transaction_type == "Expense")
        .scalar()
    )

    highest_category = (
        db.session.query(
            Expense.category,
            func.sum(Expense.amount).label("total")
        )
        .filter(Expense.transaction_type == "Expense")
        .group_by(Expense.category)
        .order_by(func.sum(Expense.amount).desc())
        .first()
    )

    largest_expense = (
        Expense.query
        .filter(Expense.transaction_type == "Expense")
        .order_by(Expense.amount.desc())
        .first()
    )

    largest_income = (
        Expense.query
        .filter(Expense.transaction_type == "Income")
        .order_by(Expense.amount.desc())
        .first()
    )

    payment_method = (
        db.session.query(
            Expense.payment_method,
            func.count(Expense.id).label("count")
        )
        .group_by(Expense.payment_method)
        .order_by(func.count(Expense.id).desc())
        .first()
    )

    savings_rate = 0
    if float(total_income) > 0:
        savings_rate = round(((float(total_income) - float(total_expense)) / float(total_income)) * 100, 2)

    return {
        "savings_rate": savings_rate,
        "highest_category": highest_category[0] if highest_category else "N/A",
        "highest_category_amount": float(highest_category[1]) if highest_category else 0,
        "largest_expense": largest_expense,
        "largest_income": largest_income,
        "most_used_payment_method": payment_method[0] if payment_method else "N/A"
    }


# ======================================================
# Phase 5 - Advanced Analytics
# ======================================================

def get_financial_statistics():
    """Return high-level financial statistics for the Analytics page."""

    dashboard = get_dashboard_summary()
    insights = get_financial_insights()

    total_income = dashboard["total_income"]
    total_expense = dashboard["total_expense"]

    net_savings = total_income - total_expense

    savings_rate = 0
    if total_income > 0:
        savings_rate = round((net_savings / total_income) * 100, 2)

    average_transaction = 0
    if dashboard["transaction_count"] > 0:
        average_transaction = round(
            (total_income + total_expense) / dashboard["transaction_count"],
            2,
        )

    return {
        "total_income": total_income,
        "total_expense": total_expense,
        "net_savings": net_savings,
        "transaction_count": dashboard["transaction_count"],
        "average_transaction": average_transaction,
        "savings_rate": savings_rate,
        "highest_category": insights["highest_category"],
        "highest_category_amount": insights["highest_category_amount"],
        "most_used_payment_method": insights["most_used_payment_method"],
    }

def get_spending_behavior():
    """Return additional spending behaviour metrics for the Analytics page."""

    expense_count = (
        Expense.query
        .filter(Expense.transaction_type == "Expense")
        .count()
    )

    total_expense = (
        db.session.query(func.coalesce(func.sum(Expense.amount), 0))
        .filter(Expense.transaction_type == "Expense")
        .scalar()
    )

    average_expense = 0
    if expense_count > 0:
        average_expense = round(float(total_expense) / expense_count, 2)

    largest_expense = (
        Expense.query
        .filter(Expense.transaction_type == "Expense")
        .order_by(Expense.amount.desc())
        .first()
    )

    largest_income = (
        Expense.query
        .filter(Expense.transaction_type == "Income")
        .order_by(Expense.amount.desc())
        .first()
    )

    category_count = (
        db.session.query(func.count(func.distinct(Expense.category)))
        .filter(Expense.transaction_type == "Expense")
        .scalar()
    )

    average_per_category = 0
    if category_count:
        average_per_category = round(float(total_expense) / category_count, 2)

    return {
        "average_expense": average_expense,
        "average_per_category": average_per_category,
        "largest_expense": largest_expense,
        "largest_income": largest_income,
        "expense_count": expense_count,
    }


def get_budget_analysis():
    """Return overall budget analytics for the Analytics page."""

    from models.database import Budget

    budgets = Budget.query.all()

    def budget_value(budget):
        for field in ("budget_amount", "limit_amount", "monthly_limit", "amount"):
            if hasattr(budget, field):
                value = getattr(budget, field)
                return float(value or 0)
        return 0.0

    total_budget = sum(budget_value(b) for b in budgets)

    total_spent = (
        db.session.query(func.coalesce(func.sum(Expense.amount), 0))
        .filter(Expense.transaction_type == "Expense")
        .scalar()
    )

    total_spent = float(total_spent)
    remaining_budget = total_budget - total_spent

    utilization_percentage = 0
    if total_budget > 0:
        utilization_percentage = round((total_spent / total_budget) * 100, 2)

    category_analysis = []
    over_budget_categories = []

    for budget in budgets:
        spent = (
            db.session.query(func.coalesce(func.sum(Expense.amount), 0))
            .filter(
                Expense.transaction_type == "Expense",
                Expense.category == budget.category,
            )
            .scalar()
        )

        spent = float(spent)
        current_budget = budget_value(budget)
        utilization = 0
        if current_budget > 0:
            utilization = round((spent / float(current_budget)) * 100, 2)

        item = {
            "category": budget.category,
            "budget": float(current_budget),
            "spent": spent,
            "remaining": float(current_budget) - spent,
            "utilization": utilization,
        }

        category_analysis.append(item)

        if spent > float(current_budget):
            over_budget_categories.append(item)

    return {
        "total_budget": total_budget,
        "total_spent": total_spent,
        "remaining_budget": remaining_budget,
        "utilization_percentage": utilization_percentage,
        "category_analysis": sorted(category_analysis, key=lambda x: x["utilization"], reverse=True),
        "over_budget_categories": over_budget_categories,
    }

def get_smart_insights():
    """Generate smart financial insights for the Analytics page."""

    statistics = get_financial_statistics()
    budget = get_budget_analysis()

    insights = []

    # Savings insight
    if statistics["savings_rate"] >= 30:
        insights.append({
            "type": "success",
            "title": "Excellent Savings",
            "message": f"Your savings rate is {statistics['savings_rate']}%. Keep up the good work!"
        })
    elif statistics["savings_rate"] >= 10:
        insights.append({
            "type": "info",
            "title": "Healthy Savings",
            "message": f"Your savings rate is {statistics['savings_rate']}%. There's still room for improvement."
        })
    else:
        insights.append({
            "type": "warning",
            "title": "Low Savings Rate",
            "message": "Your expenses are consuming most of your income."
        })

    # Budget utilization insight
    if budget["utilization_percentage"] > 100:
        insights.append({
            "type": "danger",
            "title": "Budget Exceeded",
            "message": "Your overall expenses have exceeded your planned budget."
        })
    elif budget["utilization_percentage"] > 80:
        insights.append({
            "type": "warning",
            "title": "Budget Alert",
            "message": "You have used more than 80% of your total budget."
        })
    else:
        insights.append({
            "type": "success",
            "title": "Budget On Track",
            "message": "Your spending is currently within the planned budget."
        })

    # Over-budget categories
    for item in budget["over_budget_categories"]:
        insights.append({
            "type": "danger",
            "title": f"{item['category']} Budget Exceeded",
            "message": f"You have exceeded this category budget by ₹{item['spent'] - item['budget']:.2f}."
        })

    if not budget["over_budget_categories"]:
        insights.append({
            "type": "success",
            "title": "Great Budget Control",
            "message": "No categories are currently over budget."
        })

    # Spending concentration insight
    if statistics["highest_category"] != "N/A" and statistics["total_expense"] > 0:
        category_percentage = round(
            (statistics["highest_category_amount"] / statistics["total_expense"]) * 100,
            2,
        )

        insights.append({
            "type": "info",
            "title": "Top Spending Category",
            "message": (
                f"{statistics['highest_category']} accounts for "
                f"{category_percentage}% of your total expenses."
            ),
        })

    # Net savings insight
    if statistics["net_savings"] > 0:
        insights.append({
            "type": "success",
            "title": "Positive Cash Flow",
            "message": (
                f"You have saved ₹{statistics['net_savings']:.2f} overall."
            ),
        })
    elif statistics["net_savings"] < 0:
        insights.append({
            "type": "danger",
            "title": "Negative Cash Flow",
            "message": (
                f"Your expenses exceed your income by ₹{abs(statistics['net_savings']):.2f}."
            ),
        })

    # Payment method insight
    if statistics["most_used_payment_method"] != "N/A":
        insights.append({
            "type": "info",
            "title": "Preferred Payment Method",
            "message": (
                f"You mostly use {statistics['most_used_payment_method']} for transactions."
            ),
        })

    # Remaining budget insight
    if budget["remaining_budget"] > 0:
        insights.append({
            "type": "success",
            "title": "Remaining Budget",
            "message": (
                f"You still have ₹{budget['remaining_budget']:.2f} available to spend."
            ),
        })
    elif budget["total_budget"] > 0:
        insights.append({
            "type": "danger",
            "title": "Budget Exhausted",
            "message": "Your entire budget has been exhausted."
        })

    return insights