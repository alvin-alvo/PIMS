from flask import Blueprint, jsonify

user_bp = Blueprint('user_bp', __name__)

@user_bp.route('/users', methods=['GET'])
def get_users():
    return jsonify({"message": "List of all users"})

@user_bp.route('/users/<user_id>', methods=['GET'])
def get_user(user_id):
    return jsonify({"message": f"User details for {user_id}"})

