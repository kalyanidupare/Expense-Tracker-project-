from flask import Flask, render_template, request, jsonify, send_file
from pymongo import MongoClient
from pymongo.errors import ConnectionFailure
import pandas as pd
import os
from bson.objectid import ObjectId
import logging
from datetime import datetime

app = Flask(__name__)
app.logger.setLevel(logging.INFO)

# MongoDB connection with error handling
try:
    client = MongoClient("mongodb://localhost:27017/", serverSelectionTimeoutMS=5000)
    client.server_info()  # will throw an exception if connection fails
    db = client.expense_db
    collection = db.expenses
    app.logger.info("Successfully connected to MongoDB")
except ConnectionFailure as e:
    app.logger.error(f"Failed to connect to MongoDB: {e}")
    client = None

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/get_expenses', methods=['GET'])
def get_expenses():
    try:
        if not client:
            return jsonify({"error": "Database connection not available"}), 503
        expenses = list(collection.find({}, {'_id': 1, 'description': 1, 'amount': 1, 'category': 1, 'date': 1}))
        for expense in expenses:
            expense['_id'] = str(expense['_id'])
        return jsonify(expenses)
    except Exception as e:
        app.logger.error(f"Error fetching expenses: {e}")
        return jsonify({"error": "Failed to fetch expenses"}), 500

@app.route('/add_expense', methods=['POST'])
def add_expense():
    try:
        if not client:
            return jsonify({"error": "Database connection not available"}), 503
        data = request.json
        if not all(key in data for key in ["description", "amount", "category"]):
            return jsonify({"error": "Missing required fields"}), 400
        
        result = collection.insert_one({
            "description": data["description"],
            "amount": float(data["amount"]),
            "category": data["category"],
            "date": datetime.now()
        })
        return jsonify({"message": "Expense added successfully!", "id": str(result.inserted_id)})
    except ValueError:
        return jsonify({"error": "Invalid amount format"}), 400
    except Exception as e:
        app.logger.error(f"Error adding expense: {e}")
        return jsonify({"error": "Failed to add expense"}), 500

@app.route('/update_expense/<id>', methods=['PUT'])
def update_expense(id):
    try:
        if not client:
            return jsonify({"error": "Database connection not available"}), 503
        data = request.json
        if not all(key in data for key in ["description", "amount", "category"]):
            return jsonify({"error": "Missing required fields"}), 400

        result = collection.update_one(
            {"_id": ObjectId(id)},
            {
                "$set": {
                    "description": data["description"],
                    "amount": float(data["amount"]),
                    "category": data["category"],
                    "date": datetime.now()
                }
            }
        )
        if result.modified_count:
            return jsonify({"message": "Expense updated successfully!"})
        return jsonify({"error": "Expense not found"}), 404
    except ValueError:
        return jsonify({"error": "Invalid amount format"}), 400
    except Exception as e:
        app.logger.error(f"Error updating expense: {e}")
        return jsonify({"error": "Failed to update expense"}), 500

@app.route('/search_expenses', methods=['GET'])
def search_expenses():
    try:
        if not client:
            return jsonify({"error": "Database connection not available"}), 503
        
        query = request.args.get('query', '')
        if not query:
            return jsonify({"error": "Search query is required"}), 400

        # Create a case-insensitive regex pattern
        regex_pattern = f".*{query}.*"
        
        # Search in description and category
        expenses = list(collection.find({
            "$or": [
                {"description": {"$regex": regex_pattern, "$options": "i"}},
                {"category": {"$regex": regex_pattern, "$options": "i"}}
            ]
        }, {'_id': 1, 'description': 1, 'amount': 1, 'category': 1, 'date': 1}))
        
        for expense in expenses:
            expense['_id'] = str(expense['_id'])
        return jsonify(expenses)
    except Exception as e:
        app.logger.error(f"Error searching expenses: {e}")
        return jsonify({"error": "Failed to search expenses"}), 500

@app.route('/delete_expense/<id>', methods=['DELETE'])
def delete_expense(id):
    try:
        if not client:
            return jsonify({"error": "Database connection not available"}), 503
        result = collection.delete_one({"_id": ObjectId(id)})
        if result.deleted_count:
            return jsonify({"message": "Expense deleted successfully!"})
        return jsonify({"error": "Expense not found"}), 404
    except Exception as e:
        app.logger.error(f"Error deleting expense: {e}")
        return jsonify({"error": "Failed to delete expense"}), 500

@app.route('/export_monthly_statement')
def export_monthly_statement():
    try:
        if not client:
            return jsonify({"error": "Database connection not available"}), 503
        expenses = list(collection.find({}, {'_id': 0, 'description': 1, 'amount': 1, 'category': 1, 'date': 1}))
        df = pd.DataFrame(expenses)
        if df.empty:
            return jsonify({"error": "No expenses to export"}), 404
        
        file_path = "monthly_statement.csv"
        df.to_csv(file_path, index=False)
        return send_file(file_path, as_attachment=True, download_name="monthly_statement.csv")
    except Exception as e:
        app.logger.error(f"Error exporting statement: {e}")
        return jsonify({"error": "Failed to export statement"}), 500

if __name__ == '__main__':
    app.run(debug=True)
