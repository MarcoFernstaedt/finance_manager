from app import app, db
from app.models import User, Expense
from flask import request, jsonify

@app.route('/')
def index():
    return "Welcome to the Finance Manager"

@app.route('/register', methods=['POST'])
def register():
    username = request.json['username']
    password = request.json['password']
    user = User(username=username, password=password)
    db.session.add(user)
    db.session.commit()
    return jsonify({"message": "User registered successfully"})

@app.route('/add_expense', methods=['POST'])
def add_expense():
    data = request.json
    amount = data.get('amount')
    description = data.get('description')
    user_id = data.get('user_id')
    expense = Expense(amount=amount, description=description, user_id=user_id)
    db.session.add(expense)
    db.session.commit()
    return jsonify({"message": "Expense added successfully"})

@app.route('/expenses', methods=['GET'])
def get_expenses():
    user_id = request.args.get('user_id')
    expenses = Expense.query.filter_by(user_id=user_id).all()
    return jsonify([{"id": e.id, "amount": e.amount, "description": e.description, "user_id": e.user_id} for e in expenses])
