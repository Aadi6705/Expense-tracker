from flask import Blueprint, render_template
from services.analytics import get_dashboard_summary

dashboard_bp = Blueprint(
    "dashboard",
    __name__,
    url_prefix="/dashboard"
)


@dashboard_bp.route("/")
def dashboard():
    summary = get_dashboard_summary()

    return render_template(
        "pages/dashboard.html",
        total_income=summary["total_income"],
        total_expense=summary["total_expense"],
        total_balance=summary["total_balance"],
        transaction_count=summary["transaction_count"],
        recent_transactions=summary["recent_transactions"],
        category_summary=summary["category_summary"],
        monthly_summary=summary["monthly_summary"],
        financial_insights=summary["financial_insights"],
    )