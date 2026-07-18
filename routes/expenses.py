from datetime import datetime

from flask import Blueprint, flash, redirect, render_template, request, url_for
from sqlalchemy import or_
from sqlalchemy.exc import SQLAlchemyError

from models.database import Expense, db

expenses_bp = Blueprint("expenses", __name__, url_prefix="/expenses")


@expenses_bp.route("/")
def list_expenses():
    search = request.args.get("search", "").strip()
    transaction_type = request.args.get("type", "")
    category = request.args.get("category", "")
    payment_method = request.args.get("payment_method", "")
    start_date = request.args.get("start_date", "")
    end_date = request.args.get("end_date", "")
    sort = request.args.get("sort", "newest")

    # Filtering
    query = Expense.query

    if search:
        query = query.filter(
            or_(
                Expense.description.ilike(f"%{search}%"),
                Expense.category.ilike(f"%{search}%"),
                Expense.notes.ilike(f"%{search}%")
            )
        )

    if transaction_type:
        query = query.filter(Expense.transaction_type == transaction_type)

    if category:
        query = query.filter(Expense.category == category)

    if payment_method:
        query = query.filter(Expense.payment_method == payment_method)

    if start_date:
        try:
            query = query.filter(
                Expense.date >= datetime.strptime(start_date, "%Y-%m-%d").date()
            )
        except ValueError:
            flash("Invalid start date.", "warning")

    if end_date:
        try:
            query = query.filter(
                Expense.date <= datetime.strptime(end_date, "%Y-%m-%d").date()
            )
        except ValueError:
            flash("Invalid end date.", "warning")

    # Sorting
    if sort == "oldest":
        query = query.order_by(Expense.date.asc())
    elif sort == "highest":
        query = query.order_by(Expense.amount.desc())
    elif sort == "lowest":
        query = query.order_by(Expense.amount.asc())
    else:
        query = query.order_by(Expense.date.desc())

    expenses = query.all()

    # Summary calculations
    total_income = sum(float(e.amount) for e in expenses if e.transaction_type == "Income")
    total_expense = sum(float(e.amount) for e in expenses if e.transaction_type == "Expense")
    net_balance = total_income - total_expense

    categories = [c[0] for c in db.session.query(Expense.category).distinct().order_by(Expense.category).all()]
    payment_methods = [p[0] for p in db.session.query(Expense.payment_method).distinct().order_by(Expense.payment_method).all()]

    # Template rendering
    return render_template(
        "pages/history.html",
        expenses=expenses,
        categories=categories,
        payment_methods=payment_methods,
        filters={
            "search": search,
            "type": transaction_type,
            "category": category,
            "payment_method": payment_method,
            "start_date": start_date,
            "end_date": end_date,
            "sort": sort,
        },
        summary={
            "total_income": total_income,
            "total_expense": total_expense,
            "net_balance": net_balance,
            "transaction_count": len(expenses),
        },
    )


@expenses_bp.route("/add", methods=["GET", "POST"])
def add_expense():
    if request.method == "POST":
        try:
            amount = float(request.form["amount"])
            if amount <= 0:
                flash("Amount must be greater than zero.", "warning")
                return render_template("pages/add_expense.html", edit_mode=False)

            transaction_type = request.form["transaction_type"].strip()
            if transaction_type not in ["Income", "Expense"]:
                flash("Please select a valid transaction type.", "warning")
                return render_template("pages/add_expense.html", edit_mode=False)

            category = request.form["category"].strip()
            if not category:
                flash("Please select a category.", "warning")
                return render_template("pages/add_expense.html", edit_mode=False)

            payment_method = request.form["payment_method"].strip()

            expense = Expense(
                transaction_type=transaction_type,
                date=datetime.strptime(request.form["date"], "%Y-%m-%d").date(),
                category=category,
                description=request.form.get("description", "").strip(),
                amount=amount,
                payment_method=payment_method,
                notes=request.form.get("notes", "").strip(),
            )

            db.session.add(expense)
            db.session.commit()

            flash("Transaction added successfully.", "success")
            return redirect(url_for("expenses.list_expenses"))

        except SQLAlchemyError as exc:
            db.session.rollback()
            flash(f"Database error: {exc}", "danger")

        except ValueError:
            flash("Please enter a valid amount and date.", "warning")

    return render_template("pages/add_expense.html", edit_mode=False)


# Edit expense route
@expenses_bp.route("/edit/<int:expense_id>", methods=["GET", "POST"])
def edit_expense(expense_id):
    expense = Expense.query.get_or_404(expense_id)

    if request.method == "POST":
        try:
            amount = float(request.form["amount"])
            if amount <= 0:
                flash("Amount must be greater than zero.", "warning")
                return render_template("pages/add_expense.html", expense=expense, edit_mode=True)

            transaction_type = request.form["transaction_type"].strip()
            if transaction_type not in ["Income", "Expense"]:
                flash("Please select a valid transaction type.", "warning")
                return render_template("pages/add_expense.html", expense=expense, edit_mode=True)

            expense.transaction_type = transaction_type
            expense.date = datetime.strptime(request.form["date"], "%Y-%m-%d").date()
            expense.category = request.form["category"].strip()
            expense.description = request.form.get("description", "").strip()
            expense.amount = amount
            expense.payment_method = request.form["payment_method"].strip()
            expense.notes = request.form.get("notes", "").strip()

            db.session.commit()
            flash("Transaction updated successfully.", "success")
            return redirect(url_for("expenses.list_expenses"))

        except (ValueError, SQLAlchemyError) as exc:
            db.session.rollback()
            flash(f"Unable to update transaction: {exc}", "danger")

    return render_template("pages/add_expense.html", expense=expense, edit_mode=True)


# Delete expense route
@expenses_bp.route("/delete/<int:expense_id>", methods=["POST"])
def delete_expense(expense_id):
    expense = Expense.query.get_or_404(expense_id)

    try:
        db.session.delete(expense)
        db.session.commit()
        flash("Transaction deleted successfully.", "success")
    except SQLAlchemyError as exc:
        db.session.rollback()
        flash(f"Unable to delete transaction: {exc}", "danger")

    return redirect(url_for("expenses.list_expenses"))