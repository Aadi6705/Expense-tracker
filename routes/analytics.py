from flask import Blueprint, render_template
from services.analytics_service import (
    get_dashboard_summary,
    get_financial_statistics,
    get_financial_insights,
    get_spending_behavior,
    get_budget_analysis,
    get_smart_insights,
)

analytics_bp = Blueprint(
    "analytics",
    __name__,
    url_prefix="/analytics"
)

@analytics_bp.route("/")
def analytics():
    statistics = get_financial_statistics()
    dashboard = get_dashboard_summary()
    insights = get_financial_insights()
    spending_behavior = get_spending_behavior()
    budget_analysis = get_budget_analysis()
    smart_insights = get_smart_insights()
    return render_template(
        "pages/analytics.html",
        dashboard=dashboard,
        statistics=statistics,
        insights=insights,
        spending_behavior=spending_behavior,
        budget_analysis=budget_analysis,
        smart_insights=smart_insights,
        **dashboard,
    )