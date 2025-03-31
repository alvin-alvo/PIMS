from flask import Blueprint, request, jsonify, render_template
import db
from models import User

user_bp = Blueprint('user_bp', __name__, template_folder='../templates/user')

@user_bp.route('/home')
# @login_required
def user_home():
    return render_template('user/user_dashboard.html')

@user_bp.route('/dashboard')
def user_dashboard():
    return render_template('user/user_dashboard.html')

@user_bp.route('/address')
def user_address():
    return render_template('user/user_address.html')

@user_bp.route('/contacts')
def user_contacts():
    return render_template('user/user_contacts.html')

@user_bp.route('/emg_contacts')
def user_emg_contacts():
    return render_template('user/user_emg_contacts.html')

@user_bp.route('/education')
def user_education():
    return render_template('user/user_education.html')

@user_bp.route('/workexp')
def user_workexp():
    return render_template('user/user_workexp.html')

@user_bp.route('/finance')
def user_finance():
    return render_template('user/user_finance.html')

@user_bp.route('/onlineacc')
def user_onlineacc():
    return render_template('user/user_onlineacc.html')

@user_bp.route('/user/<user_id>', methods=['GET'])
def get_user(user_id):
    user = User.query.get(user_id)
    if not user:
        return jsonify({'error': 'User not found'}), 404
    return jsonify({
        'user_id': user.user_id,
        'F_Name': user.F_Name,
        'L_Name': user.L_Name,
        'Gender': user.Gender,
        'DOB': user.DOB,
        'Age': user.Age
    })

@user_bp.route('/user/<user_id>', methods=['PUT'])
def update_user(user_id):
    data = request.json
    user = User.query.get(user_id)
    if not user:
        return jsonify({'error': 'User not found'}), 404
    user.F_Name = data.get('F_Name', user.F_Name)
    user.L_Name = data.get('L_Name', user.L_Name)
    db.session.commit()
    return jsonify({'message': 'User updated successfully'})
