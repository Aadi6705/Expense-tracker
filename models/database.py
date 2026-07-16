from flask_sqlalchemy import SQLAlchemy

# SQLAlchemy instance
# This will be initialized with the Flask app in app.py
# using db.init_app(app)
db = SQLAlchemy()


class Expense(db.Model):
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

    def __repr__(self):
        return (
            f"<Expense(id={self.id}, type='{self.transaction_type}', category='{self.category}', amount={self.amount})>"
        )