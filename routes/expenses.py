

from datetime import datetime

from flask import Blueprint, flash, redirect, render_template, request, url_for
from sqlalchemy.exc import SQLAlchemyError

from models.database import Expense, db

expenses_bp = Blueprint("expenses", __name__, url_prefix="/expenses")


@expenses_bp.route("/")
def list_expenses():
    expenses = Expense.query.order_by(Expense.date.desc()).all()
    return render_template("pages/history.html", expenses=expenses)


@expenses_bp.route("/add", methods=["GET", "POST"])
def add_expense():
    if request.method == "POST":
        try:
            amount = float(request.form["amount"])
            if amount <= 0:
                flash("Amount must be greater than zero.", "warning")
                return render_template("pages/add_expense.html")

            expense = Expense(
                date=datetime.strptime(request.form["date"], "%Y-%m-%d").date(),
                category=request.form["category"].strip(),
                description=request.form.get("description", "").strip(),
                amount=amount,
                payment_method=request.form["payment_method"],
            )

            db.session.add(expense)
            db.session.commit()

            flash("Expense added successfully.", "success")
            return redirect(url_for("expenses.list_expenses"))

        except SQLAlchemyError as exc:
            db.session.rollback()
            flash(f"Database error: {exc}", "danger")

        except ValueError:
            flash("Please enter a valid amount and date.", "warning")

    return render_template("pages/add_expense.html")