from flask import Blueprint, request, render_template, session, redirect, url_for, flash
from db import get_db_connection
from auth import admin_required
import mysql.connector

admin_bp = Blueprint('admin_bp', __name__, template_folder='../templates/admin')

@admin_bp.route('/dashboard', methods=['GET'])
@admin_required
def admin_dashboard():
    if 'admin_id' not in session:
        flash("You must be logged in to access this page.", "warning")
        return redirect(url_for('auth_bp.admin_login'))
    
     
    admin = {
        "admin_name": session.get("admin_name"),
        "admin_email": session.get("admin_email"),
        "admin_phone": session.get("admin_phone"),
        "admin_password": session.get("admin_password"),  
    }
    return render_template('admin/admin_dashboard.html', admin=admin)

@admin_bp.route('/admin/users', methods=['GET', 'POST'])
@admin_required
def get_all_users():
    # Handle user deletion
    if request.method == 'POST' and 'delete_user' in request.form:
        user_id = request.form['delete_user']
        conn = None
        cursor = None
        try:
            conn = get_db_connection()
            cursor = conn.cursor()

            # Disable foreign key checks (temporarily)
            cursor.execute("SET FOREIGN_KEY_CHECKS = 0")

            #  Delete from ALL related tables (order matters!)
            tables_to_clean = [
                "authentication",
                "contact",
                "address",
                "education",
                "work_experience",
                "user"
            ]

            for table in tables_to_clean:
                cursor.execute(f"DELETE FROM {table} WHERE user_id = %s", (user_id,))
                print(f"Deleted from {table}: {cursor.rowcount} rows")

            #  Re-enable foreign key checks
            cursor.execute("SET FOREIGN_KEY_CHECKS = 1")
            
            conn.commit()
            flash(f"User {user_id} and all related data deleted", "success")

        except mysql.connector.Error as err:
            if conn:
                conn.rollback()
            flash(f"Deletion failed: {err}", "danger")
            print(f"SQL Error: {err}")
            return redirect(url_for('admin_bp.get_all_users'))  

        finally:
            if cursor:
                cursor.close()
            if conn:
                conn.close()

    # Fetch all users (for both GET and POST after deletion)
    conn = None
    cursor = None
    try:
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        
        query = """
        SELECT 
            u.user_id,
            u.F_Name,
            u.L_Name,
            c.Email_id,
            c.Phone_No
        FROM 
            user u
        JOIN 
            contact c ON u.user_id = c.user_id
        ORDER BY 
            u.L_Name ASC, u.F_Name ASC
        """
        cursor.execute(query)
        users = cursor.fetchall()
        
    except mysql.connector.Error as err:
        flash(f"Database error: {err}", "danger")
        users = []
        
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()
            
    return render_template('admin/admin_users.html', users=users)


