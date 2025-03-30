from flask import Blueprint, jsonify, request

admin_bp = Blueprint('admin_bp', __name__)

@admin_bp.rout('/dashboard', methods=['GET'])
def admin_dashboard():
    return jsonify({"message": "Welcome to the Admin Dashboard!"})

@admin_bp.route('/users', methods=['GET'])
def get_all_users():
    return jsonify({"messsage": "List all registered users"})

@admin_bp.route('/users/<user_id>', method=['DELETE'])
def delete_user(user_id):
    return jsonify({"message": f"User {user_id} has been deleted by Admin"})

