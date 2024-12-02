from flask import Blueprint, request, jsonify
from App.models import User, db, Message, Call
from datetime import datetime

routes = Blueprint('routes', __name__)

# Sign up route (same as before)
@routes.route('/signup', methods=['POST'])
def signup():
    data = request.json
    if User.query.filter_by(username=data['username']).first():
        return jsonify({"error": "Username already exists!"}), 400

    user = User(username=data['username'])
    user.set_password(data['password'])
    db.session.add(user)
    db.session.commit()
    return jsonify({"message": "User created successfully!"}), 201

# Login route (same as before)
@routes.route('/login', methods=['POST'])
def login():
    data = request.json
    user = User.query.filter_by(username=data['username']).first()

    if not user or not user.check_password(data['password']):
        return jsonify({"error": "Invalid username or password!"}), 401

    # Update status to "online"
    user.status = "online"
    db.session.commit()

    return jsonify({"message": "Login successful!"}), 200

# Check status route (same as before)
@routes.route('/check_status', methods=['GET'])
def check_status():
    username = request.args.get('username')  # Get the username from query parameters
    user = User.query.filter_by(username=username).first()

    if user:
        return jsonify({"username": user.username, "status": user.status})
    else:
        return jsonify({"message": "User not found"}), 404

# Send message route
@routes.route('/send_message', methods=['POST'])
def send_message():
    data = request.json
    sender = User.query.filter_by(username=data['sender']).first()
    receiver = User.query.filter_by(username=data['receiver']).first()

    if not sender or not receiver:
        return jsonify({"error": "Sender or receiver not found!"}), 404

    message = Message(sender_id=sender.id, receiver_id=receiver.id, content=data['content'])
    db.session.add(message)
    db.session.commit()

    return jsonify({"message": "Message sent successfully!"}), 200

# Initiate call route
@routes.route('/initiate_call', methods=['POST'])
def initiate_call():
    data = request.json
    caller = User.query.filter_by(username=data['caller']).first()
    receiver = User.query.filter_by(username=data['receiver']).first()

    if not caller or not receiver:
        return jsonify({"error": "Caller or receiver not found!"}), 404

    if receiver.status != "online":
        return jsonify({"error": "Receiver is not available!"}), 400

    call = Call(caller_id=caller.id, receiver_id=receiver.id, status="initiated")
    db.session.add(call)
    db.session.commit()

    return jsonify({"message": "Call initiated successfully!"}), 200

# Accept call route
@routes.route('/accept_call', methods=['POST'])
def accept_call():
    data = request.json
    call = Call.query.filter_by(id=data['call_id'], status="initiated").first()

    if not call:
        return jsonify({"error": "Call not found or already accepted!"}), 404

    call.status = "ongoing"
    db.session.commit()

    return jsonify({"message": "Call accepted!"}), 200

# End call route
@routes.route('/end_call', methods=['POST'])
def end_call():
    data = request.json
    call = Call.query.filter_by(id=data['call_id'], status="ongoing").first()

    if not call:
        return jsonify({"error": "Call not found or already ended!"}), 404

    call.status = "terminated"
    db.session.commit()

    return jsonify({"message": "Call ended!"}), 200
