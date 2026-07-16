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