from flask import Flask, render_template
from models.database import db

app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///expense_tracker.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["SECRET_KEY"] = "dev-secret-key"

# Initialize SQLAlchemy
db.init_app(app)

# Create database tables
with app.app_context():
    db.create_all()


@app.route("/")
def home():
    return render_template("pages/home.html")


if __name__ == "__main__":
    app.run(debug=True)