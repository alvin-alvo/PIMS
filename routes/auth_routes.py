from flask import Blueprint, request, jsonify, render_template, redirect
import db
from models import User, Authentication

auth_bp = Blueprint('auth_bp', __name__, template_folder='../templates/user')

@auth_bp.route('/register', methods=['GET', 'POST'])
def register_user():
    return render_template('user/register_user.html')
    

@auth_bp.route('/login', methods=['GET', 'POST'])
def login_user():
    return render_template('user/user_login.html')

@auth_bp.route('/logout')
def user_logout():
    return render_template('user/user_login.html')
