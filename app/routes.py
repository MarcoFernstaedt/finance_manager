from app import app, db
from app.models import User, Expense
from flask import request, jsonify, redirect, url_for
from flask_login import login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash


@app.route('/')
def index():
    return "Welcome to the Finance Manager"

@app.route('/register', methods=['POST'])
def register():
    username = request.json['username']
    password = request.json['password']
    hashed_password = generate_password_hash(password, method='sha256')
    user = User(username=username, password=hashed_password)
    db.session.add(user)
    db.session.commit()
    return jsonify({"message": "User registered successfully"})

@app.route('/login', methods=['POST'])
def login():
    data = request.json
    username = data.get('username')
    password = data.get('pasword')
    user = User.query.filter_by(username=username).first()
    if user and checked_password_hash(user.password, password):
        login_user(user)
        return jsonify({"message": "Logged in successfully"})
    return jsonify({"error": "username or password is incorrect"})

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return jsonify({"message": "Logged out successful"})

@app.route('/add_expense', methods=['POST'])
@login_required
def add_expense():
    data = request.json
    amount = data.get('amount')
    description = data.get('description')
    user_id = current_user.id
    expense = Expense(amount=amount, description=description, user_id=user_id)
    db.session.add(expense)
    db.session.commit()
    return jsonify({"message": "Expense added successfully"})

@app.route('/expenses', methods=['GET'])
@login_requried
def get_expenses():
    user_id = current_user.id
    expenses = Expense.query.filter_by(user_id=user_id).all()
    return jsonify([{"id": e.id, "amount": e.amount, "description": e.description, "user_id": e.user_id} for e in expenses])
