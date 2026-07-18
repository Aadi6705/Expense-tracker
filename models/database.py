from flask_sqlalchemy import SQLAlchemy

# SQLAlchemy instance
# This will be initialized with the Flask app in app.py
# using db.init_app(app)
db = SQLAlchemy()


class Expense(db.Model):
    """Stores income and expense transactions."""
    __tablename__ = "expenses"

    id = db.Column(db.Integer, primary_key=True)
    transaction_type = db.Column(db.String(20), nullable=False)
    date = db.Column(db.Date, nullable=False)
    category = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(255), nullable=True)
    amount = db.Column(db.Numeric(12, 2), nullable=False)
    payment_method = db.Column(db.String(50), nullable=False)
    notes = db.Column(db.Text, nullable=True)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(
        db.DateTime,
        server_default=db.func.now(),
        onupdate=db.func.now()
    )

    def to_dict(self):
        return {
            "id": self.id,
            "transaction_type": self.transaction_type,
            "date": self.date.isoformat() if self.date else None,
            "category": self.category,
            "description": self.description,
            "amount": self.amount,
            "payment_method": self.payment_method,
            "notes": self.notes,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None,
        }

    @property
    def is_income(self):
        return self.transaction_type == "Income"

    @property
    def is_expense(self):
        return self.transaction_type == "Expense"

    def __repr__(self):
        return (
            f"<Expense(id={self.id}, type='{self.transaction_type}', category='{self.category}', amount={self.amount})>"
        )


class Budget(db.Model):
    """Stores monthly budget allocations for each category."""
    __tablename__ = "budgets"

    id = db.Column(db.Integer, primary_key=True)
    category = db.Column(db.String(100), unique=True, nullable=False)
    monthly_budget = db.Column(db.Numeric(12, 2), nullable=False)

    created_at = db.Column(
        db.DateTime,
        server_default=db.func.now()
    )

    updated_at = db.Column(
        db.DateTime,
        server_default=db.func.now(),
        onupdate=db.func.now()
    )

    def to_dict(self):
        return {
            "id": self.id,
            "category": self.category,
            "monthly_budget": float(self.monthly_budget),
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None,
        }

    def __repr__(self):
        return (
            f"<Budget(id={self.id}, category='{self.category}', "
            f"monthly_budget={self.monthly_budget})>"
        )