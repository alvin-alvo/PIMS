from flask import Blueprint, request, render_template, redirect, url_for, flash, session
import os
from db import get_db_connection
from models import User, Authentication
from datetime import datetime
import mysql.connector

auth_bp = Blueprint('auth_bp', __name__)
db = get_db_connection()
conn = get_db_connection()
print(conn)
cursor = conn.cursor()

def calculate_age(dob):
    today = datetime.today()
    dob = datetime.strptime(dob, "%Y-%m-%d")
    return today.year - dob.year - ((today.month, today.day) < (dob.month, dob.day))

# 1️⃣ Generate Unique User ID (Ensures Uniqueness)
def generate_user_id(first_name):
    conn = get_db_connection()
    cursor = conn.cursor()

    while True:
        prefix = first_name[:3].lower()  # Take first 3 letters
        query = "SELECT MAX(user_id) FROM user WHERE user_id LIKE %s"
        cursor.execute(query, (prefix + "%",))
        last_id = cursor.fetchone()[0]

        if last_id:
            last_number = int(last_id[-3:]) + 1
        else:
            last_number = 1

        new_user_id = f"{prefix}{last_number:03d}"

        cursor.execute("SELECT COUNT(*) FROM user WHERE user_id = %s", (new_user_id,))
        if cursor.fetchone()[0] == 0:
            break  # Exit loop if ID is unique

    cursor.close()
    conn.close()
    return new_user_id

# 2️⃣ Generate Unique Contact ID
def generate_contact_id():
    conn = get_db_connection()
    cursor = conn.cursor()

    while True:
        query = "SELECT MAX(contact_id) FROM contact WHERE contact_id LIKE 'CON%'"
        cursor.execute(query)
        last_id = cursor.fetchone()[0]

        if last_id:
            last_number = int(last_id[-3:]) + 1
        else:
            last_number = 1

        new_contact_id = f"con{last_number:03d}"

        cursor.execute("SELECT COUNT(*) FROM contact WHERE contact_id = %s", (new_contact_id,))
        if cursor.fetchone()[0] == 0:
            break  # Exit loop if ID is unique

    cursor.close()
    conn.close()
    return new_contact_id

# 3️⃣ Generate Unique Authentication ID
def generate_auth_id():
    conn = get_db_connection()
    cursor = conn.cursor()

    while True:
        query = "SELECT MAX(auth_id) FROM authentication WHERE auth_id LIKE 'AUTH%'"
        cursor.execute(query)
        last_id = cursor.fetchone()[0]

        if last_id:
            last_number = int(last_id[-3:]) + 1
        else:
            last_number = 1

        new_auth_id = f"aut{last_number:03d}"

        cursor.execute("SELECT COUNT(*) FROM authentication WHERE auth_id = %s", (new_auth_id,))
        if cursor.fetchone()[0] == 0:
            break  # Exit loop if ID is unique

    cursor.close()
    conn.close()
    return new_auth_id 

def get_admin_id():
    query = "SELECT admin_id FROM admin LIMIT 1"
    cursor.execute(query)
    result = cursor.fetchone()
    return result[0] if result else None

@auth_bp.route('/register', methods=['GET', 'POST'])
def register_user():
    if request.method == 'POST':
            first_name = request.form['first_name']
            last_name = request.form['last_name']
            gender = request.form['gender']
            dob = request.form['dob']
            email = request.form['email']
            phone = request.form['phone']
            password = request.form['password']
            security_question = request.form["security_question"]
            answer = request.form["answer"]
            
            age = calculate_age(dob)
            admin_id = get_admin_id()
            user_id = generate_user_id(first_name)
            contact_id = generate_contact_id()
            auth_id = generate_auth_id()

            try:
                conn = get_db_connection()
                cursor = conn.cursor()

                # Insert user into the database
                user_query = "INSERT INTO user (user_id, F_Name, L_Name, Gender, DOB, Age) VALUES (%s, %s, %s, %s, %s, %s)"
                cursor.execute(user_query, (user_id, first_name, last_name, gender, dob, age))
                
                con_query = "INSERT INTO contact (contact_id, user_id, Name, Email_id, Phone_No) VALUES (%s, %s, %s, %s, %s)"
                cursor.execute(con_query, (contact_id, user_id, first_name, email, phone))
                
                auth_query = "INSERT INTO authentication (auth_id, user_id, admin_id, Security_Question, Answer, Password) VALUES (%s, %s, %s, %s, %s, %s)"
                cursor.execute(auth_query, (auth_id, user_id, admin_id, security_question, answer, password))

                conn.commit()
                cursor.close()
                conn.close()

                flash("Registration successful! Please log in.", "success")
                return redirect(url_for('auth_bp.user_login'))

            except mysql.connector.Error as err:
                flash(f"Error: {err}", "danger")
                print(err)

    return render_template('user/register_user.html')    

@auth_bp.route('/login', methods=['GET', 'POST'])
def login_user():
    return render_template('user/user_login.html')

@auth_bp.route('/logout')
def user_logout():
    return render_template('user/user_login.html')

# admin login 
@auth_bp.route('/admin/login', methods=['GET', 'POST'])
def admin_login():
    if request.method == 'POST':
        admin_id = request.form['admin_id']
        password = request.form['password']

        cursor = db.cursor(dictionary=True)

        # fetch admin from db
        cursor.execute("SELECT * FROM admin WHERE admin_id = %s", (admin_id,))
        admin = cursor.fetchone()

        if admin and admin['Password'] == password:
            session['admin_id'] = admin['admin_id']
            session['admin_name'] = f"{admin['F_Name']} {admin['L_Name']}"
            flash('Login Successful!', 'success')
            return redirect(url_for('admin_bp.admin_dashboard'))
        else:
            flash('Invalid admin_id or password!', 'danger')

    return render_template('admin/admin_login.html')

# admin logout
@auth_bp.route('/admin/logout')
def admin_logout():
    session.pop('admin_id', None)
    session.popo('admin_name', None)
    flash('You have been logged out', 'info')
    return redirect(url_for('auth_bp.admin_login'))