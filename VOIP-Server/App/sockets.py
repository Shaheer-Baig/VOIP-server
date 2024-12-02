from flask import Blueprint, request, jsonify
from App.models import User, db

routes = Blueprint('routes', __name__)

# Signup Route
@routes.route('/signup', methods=['POST'])
def signup():
    data = request.get_json()

    # Validate input
    if not data or not data.get('username') or not data.get('password'):
        return jsonify({"error": "Username and password are required!"}), 400

    # Check if username already exists
    if User.query.filter_by(username=data['username']).first():
        return jsonify({"error": "Username already exists!"}), 400

    # Create a new user
    user = User(username=data['username'])
    user.set_password(data['password'])  # Hash the password
    db.session.add(user)
    db.session.commit()

    return jsonify({"message": "User created successfully!"}), 201

# Login Route
@routes.route('/login', methods=['POST'])
def login():
    data = request.get_json()

    # Validate input
    if not data or not data.get('username') or not data.get('password'):
        return jsonify({"error": "Username and password are required!"}), 400

    # Fetch the user from the database
    user = User.query.filter_by(username=data['username']).first()

    # Check if user exists and password is correct
    if not user or not user.check_password(data['password']):
        return jsonify({"error": "Invalid username or password!"}), 401

    # Update status to "online"
    user.status = "online"
    db.session.commit()

    return jsonify({"message": "Login successful!"}), 200
