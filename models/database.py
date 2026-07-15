import sqlite3
import os

# Path to the SQLite database
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DB_PATH = os.path.join(BASE_DIR, "data", "expenses.db")


def get_connection():
    """
    Creates and returns a connection to the SQLite database.
    """
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def create_table():
    """
    Creates the expenses table if it doesn't already exist.
    """
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS expenses (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            date TEXT NOT NULL,
            category TEXT NOT NULL,
            description TEXT,
            amount REAL NOT NULL,
            payment_method TEXT NOT NULL
        )
    """)

    conn.commit()
    conn.close()


def add_expense(date, category, description, amount, payment_method):
    """
    Inserts a new expense into the database.
    """
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO expenses
        (date, category, description, amount, payment_method)
        VALUES (?, ?, ?, ?, ?)
    """, (date, category, description, amount, payment_method))

    conn.commit()
    conn.close()


def get_all_expenses():
    """
    Returns all expenses ordered by newest first.
    """
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT *
        FROM expenses
        ORDER BY date DESC
    """)

    expenses = cursor.fetchall()
    conn.close()

    return expenses


def get_expense_by_id(expense_id):
    """
    Returns a single expense by its ID.
    """
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT *
        FROM expenses
        WHERE id = ?
    """, (expense_id,))

    expense = cursor.fetchone()
    conn.close()

    return expense


def update_expense(expense_id, date, category, description, amount, payment_method):
    """
    Updates an existing expense.
    """
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        UPDATE expenses
        SET
            date = ?,
            category = ?,
            description = ?,
            amount = ?,
            payment_method = ?
        WHERE id = ?
    """, (date, category, description, amount, payment_method, expense_id))

    conn.commit()
    conn.close()


def delete_expense(expense_id):
    """
    Deletes an expense by ID.
    """
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        DELETE FROM expenses
        WHERE id = ?
    """, (expense_id,))

    conn.commit()
    conn.close()
from flask_sqlalchemy import SQLAlchemy

# SQLAlchemy instance
# This will be initialized with the Flask app in app.py
# using db.init_app(app)
db = SQLAlchemy()


class Expense(db.Model):
    __tablename__ = "expenses"

    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.Date, nullable=False)
    category = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(255), nullable=True)
    amount = db.Column(db.Float, nullable=False)
    payment_method = db.Column(db.String(50), nullable=False)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(
        db.DateTime,
        server_default=db.func.now(),
        onupdate=db.func.now()
    )

    def to_dict(self):
        return {
            "id": self.id,
            "date": self.date.isoformat() if self.date else None,
            "category": self.category,
            "description": self.description,
            "amount": self.amount,
            "payment_method": self.payment_method,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None,
        }

    def __repr__(self):
        return (
            f"<Expense(id={self.id}, category='{self.category}', amount={self.amount})>"
        )