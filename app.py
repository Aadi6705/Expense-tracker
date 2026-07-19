from flask import Flask, redirect, url_for
from models.database import db
from routes.expenses import expenses_bp
from routes.dashboard import dashboard_bp
from routes.budget import budget_bp
from routes.api import api_bp


app = Flask(__name__)
app.register_blueprint(api_bp)
app.register_blueprint(budget_bp)
app.register_blueprint(dashboard_bp)

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///expense_tracker.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["SECRET_KEY"] = "dev-secret-key"
app.register_blueprint(expenses_bp)

# Initialize SQLAlchemy
db.init_app(app)

# Create database tables
with app.app_context():
    db.create_all()


@app.route("/")
def home():
    return redirect(url_for("dashboard.dashboard"))


if __name__ == "__main__":
    app.run(debug=True)