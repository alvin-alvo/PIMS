from flask import Blueprint, jsonify

auth_bp = Blueprint('auth_bp', __name__)

@auth_bp.route('/login', methods=['POST'])
def login():
    return jsonify({"message": "Login successfull!"})

@auth_bp.route('/register', methods=['POST'])
def registe():
    return jsonify({"message": "user registered!"})

