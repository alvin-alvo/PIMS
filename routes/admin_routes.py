from flask import Blueprint, jsonify, render_template, session, redirect, url_for, flash
import db
from models import User

admin_bp = Blueprint('admin_bp', __name__, template_folder='../templates/admin')

@admin_bp.route('/dashboard')
def admin_dashboard():
    if 'admin_id' not in session:
        flash("You must be logged in to access this page.", "warning")
        return redirect(url_for('auth_bp.admin_login'))
    
    return render_template('admin/admin_dashboard.html', admin_name=session.get('admin_name'))

@admin_bp.route('/admin/users', methods=['GET'])
def get_all_users():
    users = User.query.all()
    return jsonify([{'user_id': u.user_id, 'name': f"{u.F_Name} {u.L_Name}"} for u in users])

@admin_bp.route('/admin/user/<user_id>', methods=['DELETE'])
def delete_user(user_id):
    user = User.query.get(user_id)
    if not user:
        return jsonify({'error': 'User not found'}), 404
    db.session.delete(user)
    db.session.commit()
    return jsonify({'message': 'User deleted successfully'})
