from flask import Flask, render_template, request, jsonify, Response
from pymongo import MongoClient
from bson import ObjectId
import csv
from datetime import datetime, timedelta

app = Flask(__name__)

# Connect to MongoDB
client = MongoClient("mongodb://localhost:27017/")
db = client["expense_tracker"]
collection = db["expenses"]

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/get_expenses", methods=["GET"])
def get_expenses():
    expenses = list(collection.find({}, {"_id": 1, "description": 1, "amount": 1, "category": 1, "date": 1}))
    for exp in expenses:
        exp["_id"] = str(exp["_id"])  # Convert ObjectId to string for frontend
    return jsonify(expenses)

@app.route("/add_expense", methods=["POST"])
def add_expense():
    data = request.json
    data["date"] = datetime.now().strftime("%Y-%m-%d")  # Store the current date
    collection.insert_one(data)
    return jsonify({"message": "Expense added successfully"}), 201

@app.route("/delete_expense/<expense_id>", methods=["DELETE"])
def delete_expense(expense_id):
    result = collection.delete_one({"_id": ObjectId(expense_id)})
    if result.deleted_count > 0:
        return jsonify({"message": "Expense deleted"}), 200
    return jsonify({"error": "Expense not found"}), 404

@app.route("/export_monthly_statement", methods=["GET"])
def export_monthly_statement():
    current_month = datetime.now().strftime("%Y-%m")
    expenses = list(collection.find({"date": {"$regex": f"^{current_month}"}}))

    def generate_csv():
        yield "Description,Amount,Category,Date\n"
        for exp in expenses:
            yield f'{exp["description"]},{exp["amount"]},{exp["category"]},{exp["date"]}\n'

    response = Response(generate_csv(), mimetype="text/csv")
    response.headers["Content-Disposition"] = "attachment; filename=monthly_expense.csv"
    return response

@app.route("/get_status/<filter_type>", methods=["GET"])
def get_status(filter_type):
    today = datetime.now()

    if filter_type == "weekly":
        start_date = today - timedelta(days=today.weekday())  # Start of the week (Monday)
    elif filter_type == "monthly":
        start_date = today.replace(day=1)  # Start of the month
    elif filter_type == "yearly":
        start_date = today.replace(month=1, day=1)  # Start of the year
    else:
        return jsonify({"error": "Invalid filter"}), 400

    expenses = list(collection.find({"date": {"$gte": start_date.strftime("%Y-%m-%d")}}))
    total_amount = sum(exp["amount"] for exp in expenses)
    return jsonify({"total": total_amount, "expenses": expenses})

if __name__ == "__main__":
    app.run(debug=True)