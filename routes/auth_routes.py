from flask import Blueprint, request, render_template, redirect, url_for, flash, session
from db import get_db_connection
from datetime import datetime
import mysql.connector
import uuid

auth_bp = Blueprint('auth_bp', __name__)

from datetime import datetime

def calculate_age(dob):
    if not dob:
        return None  
    
    try:
        birth_date = datetime.strptime(dob, "%Y-%m-%d")  
        today = datetime.today()
        age = today.year - birth_date.year - ((today.month, today.day) < (birth_date.month, birth_date.day))
        return age
    except ValueError:
        print("Error: Invalid DOB format")
        return None


def generate_short_uuid():
    return str(uuid.uuid4().int)[:6]

def get_admin_id():
    conn = get_db_connection()
    cursor = conn.cursor()
    query = "SELECT admin_id FROM admin LIMIT 1"
    cursor.execute(query)
    result = cursor.fetchone()
    return result[0] if result else None

@auth_bp.route('/register', methods=['GET', 'POST'])
def register_user():
    if request.method == 'POST':
            try:
                first_name = request.form['first_name']
                last_name = request.form['last_name']
                gender = request.form['gender']
                dob = request.form['dob']
                email = request.form['email']
                phone = request.form['phone']
                password = request.form['password']
                security_question = request.form["security_question"]
                answer = request.form["answer"]

                try:
                    dob = datetime.strptime(dob, "%Y-%m-%d").strftime("%Y-%m-%d")
                except ValueError:
                    flash("Invalid date format!", "danger")
                    return render_template('user/register_user.html')
                
                age = calculate_age(dob)
                admin_id = get_admin_id()
                user_id = generate_short_uuid()
                contact_id = generate_short_uuid()
                auth_id = generate_short_uuid()

                
                conn = get_db_connection()
                cursor = conn.cursor()

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
                return redirect(url_for('auth_bp.login_user'))

            except mysql.connector.Error as err:
                flash(f"Error: {err}", "danger")
                print(err)

    return render_template('user/register_user.html')    

@auth_bp.route('/login', methods=['GET', 'POST'])
def login_user():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        print(f"\n[DEBUG] Login Attempt: Email={email}")

        try:
            conn = get_db_connection()
            cursor = conn.cursor(dictionary=True)

            # Debug SQL query execution
            print("[DEBUG] Executing Login Query...")

            cursor.execute("""
                SELECT u.user_id, u.F_Name, u.L_Name, c.Email_id, c.Phone_No, u.Gender, u.DOB, u.Age, 
                    e.Institution_Name, e.Field_Of_Study, e.Start_Date, e.End_Date, e.degree,
                    w.Job_Title, w.Role, w.Company_Name, w.W_Start_Date, w.W_End_Date,
                    a.Security_Question, a.Answer, a.Password,
                    ad.Street_Name, ad.House_Name, ad.City, ad.State, ad.Postal_Code, ad.Country
                FROM authentication a
                JOIN user u ON a.user_id = u.user_id
                JOIN contact c ON u.user_id = c.user_id
                LEFT JOIN address ad ON u.user_id = ad.user_id
                LEFT JOIN education e ON u.user_id = e.user_id
                LEFT JOIN work_experience w ON u.user_id = w.user_id
                WHERE c.Email_id = %s AND a.Password = %s
            """, (email, password))
            
            user = cursor.fetchone()

            if not user:
                print("[DEBUG] No user found with this email.")
                flash('Invalid email or password!', 'danger')
                return render_template('user/user_login.html')

            # ✅ Verify password match (Modify this if passwords are hashed)
            print(f"[DEBUG] DB Password: {user['Password']}, Entered Password: {password}")
            if user['Password'] != password:
                print("[DEBUG] Password mismatch!")
                flash('Invalid email or password!', 'danger')
                return render_template('user/user_login.html')

            print("[DEBUG] User authenticated! Storing session data...")

            if user['DOB']:
                formatted_dob = user['DOB'].strftime("%Y-%m-%d")

            #  Store user details in session
            session['user'] = {
                'user_id': user['user_id'],
                'first_name': user.get('F_Name', ""),
                'last_name': user.get('L_Name', ""),
                'email': user.get('Email_id', ""),
                'phone': user.get('Phone_No', ""),
                'gender': user.get('Gender', ""),
                'dob': formatted_dob,
                'age': user.get('Age', ""),
                'institution': user.get('Institution_Name',""),
                'field': user.get('Field_Of_Study',""),
                'start': user.get('Start_Date',""),
                'end': user.get('End_Date',""),
                'degree': user.get('degree', ""),
                'title': user.get('Job_Title', ""),
                'role': user.get('Role', ""),
                'company': user.get('Company_Name', ""),
                'wstart': user.get('W_Start_Date',""),
                'wend': user.get('W_End_Date',""),
                'platform': user.get('Platform_Name', ""),
                'username': user.get('UserName', ""),
                'url': user.get('Profile_Url', ""),
                'securityq': user.get('Security_Question', ""),
                'answer': user.get('Answer', ""),
                'password': user.get('Password', ""),
                'street': user.get('Street_Name', ""),
                'house': user.get('House_Name', ""),
                'city': user.get('City', ""),
                'state': user.get('State', ""),
                'postal_code': user.get('Postal_Code', ""),
                'country': user.get('Country', "")
            }

            session.modified = True
            print("[DEBUG] Session stored successfully!")

            flash('Login successful!', 'success')
            return redirect(url_for('user_bp.user_dashboard'))

        except mysql.connector.Error as err:
            flash('Database error occurred', 'danger')
            print(f"[ERROR] Database error: {err}")

        finally:
            cursor.close()
            conn.close()
    
    return render_template('user/user_login.html')


@auth_bp.route('/logout')
def user_logout():
    session.pop('user_id', None)
    session.pop('user_name', None)
    flash('You have been logged out', 'info')
    return redirect(url_for('auth_bp.login_user'))

# admin login 
@auth_bp.route('/admin/login', methods=['GET', 'POST'])
def admin_login():
    if request.method == 'POST':
        admin_id = request.form['admin_id']
        password = request.form['password']

        conn = get_db_connection()
        cursor = conn.cursor()
        cursor = conn.cursor(dictionary=True)

        # fetch admin from db
        cursor.execute("SELECT * FROM admin WHERE admin_id = %s", (admin_id,))
        admin = cursor.fetchone()

        if admin and admin['Password'] == password:
            session['admin_id'] = admin['admin_id']
            session['admin_name'] = f"{admin['F_Name']} {admin['L_Name']}"
            session['admin_email'] = admin['Email']
            session['admin_phone'] = admin['Phone']
            session['admin_password'] = admin['Password']
            flash('Login Successful!', 'success')
            return redirect(url_for('admin_bp.admin_dashboard'))
        else:
            flash('Invalid admin_id or password!', 'danger')

    return render_template('admin/admin_login.html')

# admin logout
@auth_bp.route('/admin/logout')
def admin_logout():
    session.pop('admin_id', None)
    session.pop('admin_name', None)
    flash('You have been logged out', 'info')
    return redirect(url_for('auth_bp.admin_login'))