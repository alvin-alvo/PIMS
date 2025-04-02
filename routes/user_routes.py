import logging
from flask import Blueprint, request, jsonify, render_template, session, flash, redirect, url_for
from db import get_db_connection
from models import User
from auth import login_required
import mysql.connector
from routes.auth_routes import calculate_age, generate_short_uuid

# Configure logging
logging.basicConfig(level=logging.DEBUG, format='[%(levelname)s] %(message)s')

user_bp = Blueprint('user_bp', __name__, template_folder='../templates/user')

### DASHBOARD ###
@user_bp.route('/dashboard')
@login_required
def user_dashboard():
    logging.debug("Accessing Dashboard...")
    return render_template('user/user_dashboard.html', user=session.get('user'))

@user_bp.route('/update_dashboard', methods=['POST'])
@login_required
def update_dashboard():
    user_id = session.get('user', {}).get('user_id')
    
    if not user_id:
        flash("User not found!", "danger")
        return redirect(url_for('user_bp.user_dashboard'))

    first_name = request.form.get('first_name')
    last_name = request.form.get('last_name')
    gender = request.form.get('gender')
    dob = request.form.get('dob')

    try:
        conn = get_db_connection()
        cursor = conn.cursor()

        cursor.execute("""
            UPDATE user SET F_Name = %s, L_Name = %s, Gender = %s, DOB = %s WHERE user_id = %s
        """, (first_name, last_name, gender, dob, user_id))
        conn.commit()

        session['user'].update({'first_name': first_name, 'last_name': last_name, 'gender': gender, 'dob': dob})
        flash("Profile updated successfully!", "success")

    except mysql.connector.Error as err:
        conn.rollback()
        logging.error(f"Database error: {err}")
        flash("Error updating profile!", "danger")

    finally:
        cursor.close()
        conn.close()

    return redirect(url_for('user_bp.user_dashboard'))

### CONTACTS ###
@user_bp.route('/contacts')
@login_required
def user_contacts():
    return render_template('user/user_contacts.html', user=session.get('user'))

@user_bp.route('/update_contacts', methods=['POST'])
@login_required
def update_contacts():
    user_id = session.get('user', {}).get('user_id')

    if not user_id:
        flash("User not found!", "danger")
        return redirect(url_for('user_bp.user_contacts'))

    email = request.form.get('email')
    phone = request.form.get('phone')

    try:
        conn = get_db_connection()
        cursor = conn.cursor()

        cursor.execute("""
            UPDATE contact SET Email_id = %s, Phone_No = %s WHERE user_id = %s
        """, (email, phone, user_id))
        conn.commit()

        session['user'].update({'email': email, 'phone': phone})
        flash("Contact details updated successfully!", "success")

    except mysql.connector.Error as err:
        conn.rollback()
        flash("Error updating contacts!", "danger")
        logging.error(f"Database error: {err}")

    finally:
        cursor.close()
        conn.close()

    return redirect(url_for('user_bp.user_contacts'))

### ADDRESS ###
@user_bp.route('/address')
@login_required
def user_address():
    return render_template('user/user_address.html', user=session.get('user'))

@user_bp.route('/update_address', methods=['POST'])
@login_required
def update_address():
    user_id = session.get('user', {}).get('user_id')

    if not user_id:
        flash("User not found!", "danger")
        return redirect(url_for('user_bp.user_address'))

    house = request.form.get('house')
    street = request.form.get('street')
    city = request.form.get('city')
    state = request.form.get('state')
    postal_code = request.form.get('postal_code')
    country = request.form.get('country')

    print(f"[DEBUG] Address Update Request - House: {house}, Street: {street}, City: {city}, State: {state}, Postal Code: {postal_code}, Country: {country}, User ID: {user_id}")

    try:
        conn = get_db_connection()
        cursor = conn.cursor()

        # Check if the user has an address
        cursor.execute("SELECT COUNT(*) FROM address WHERE user_id = %s", (user_id,))
        user_exists = cursor.fetchone()[0]

        if user_exists == 0:

            address_id = generate_short_uuid()
            # If no address exists, INSERT a new address
            print(f"[INFO] No address found for User ID: {user_id}. Inserting new address.")
            cursor.execute("""
                INSERT INTO address (address_id, user_id, House_Name, Street_Name, City, State, Postal_Code, Country) 
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
            """, (address_id, user_id, house, street, city, state, postal_code, country))
        else:
            # If an address exists, UPDATE it
            cursor.execute("""
                UPDATE address 
                SET House_Name = %s, Street_Name = %s, City = %s, State = %s, Postal_Code = %s, Country = %s 
                WHERE user_id = %s
            """, (house, street, city, state, postal_code, country, user_id))

        conn.commit()
        flash("Address updated successfully!", "success")
        print(f"[INFO] Address updated successfully for User ID: {user_id}")

        # Update session to reflect new address data
        session['user'].update({
            'house': house,
            'street': street,
            'city': city,
            'state': state,
            'postal_code': postal_code,
            'country': country
        })
        session.modified = True

    except mysql.connector.Error as err:
        conn.rollback()
        flash("Error updating address!", "danger")
        logging.error(f"[ERROR] Database error: {err}")
        print(f"[ERROR] Database error: {err}")

    finally:
        cursor.close()
        conn.close()

    return redirect(url_for('user_bp.user_address'))

### EDUCATION ###
@user_bp.route('/education')
@login_required
def user_education():
    return render_template('user/user_education.html', user=session.get('user'))

@user_bp.route('/update_education', methods=['POST'])
@login_required
def update_education():
    user_id = session.get('user', {}).get('user_id')

    if not user_id:
        flash("User not found!", "danger")
        return redirect(url_for('user_bp.user_education'))

    degree = request.form.get('degree')
    institution = request.form.get('institution')
    year = request.form.get('year')

    try:
        conn = get_db_connection()
        cursor = conn.cursor()

        cursor.execute("""
            UPDATE education SET Degree = %s, Institution = %s, Year = %s WHERE user_id = %s
        """, (degree, institution, year, user_id))
        conn.commit()

        flash("Education details updated successfully!", "success")

    except mysql.connector.Error as err:
        conn.rollback()
        flash("Error updating education!", "danger")
        logging.error(f"Database error: {err}")

    finally:
        cursor.close()
        conn.close()

    return redirect(url_for('user_bp.user_education'))

### WORK EXPERIENCE ###
@user_bp.route('/workexp')
@login_required
def user_workexp():
    return render_template('user/user_workexp.html', user=session.get('user'))

@user_bp.route('/update_workexp', methods=['POST'])
@login_required
def update_workexp():
    user_id = session.get('user', {}).get('user_id')

    if not user_id:
        flash("User not found!", "danger")
        return redirect(url_for('user_bp.user_workexp'))

    company = request.form.get('company')
    role = request.form.get('role')
    years = request.form.get('years')

    try:
        conn = get_db_connection()
        cursor = conn.cursor()

        cursor.execute("""
            UPDATE work_experience SET Company = %s, Role = %s, Years = %s WHERE user_id = %s
        """, (company, role, years, user_id))
        conn.commit()

        flash("Work experience updated successfully!", "success")

    except mysql.connector.Error as err:
        conn.rollback()
        flash("Error updating work experience!", "danger")
        logging.error(f"Database error: {err}")

    finally:
        cursor.close()
        conn.close()

    return redirect(url_for('user_bp.user_workexp'))

### ONLINE ACCOUNTS ###
@user_bp.route('/online_acc')
@login_required
def user_onlineacc():
    return render_template('user/user_onlineacc.html', user=session.get('user'))

@user_bp.route('/update_onlineacc', methods=['POST'])
@login_required
def update_onlineacc():
    user_id = session.get('user', {}).get('user_id')

    if not user_id:
        flash("User not found!", "danger")
        return redirect(url_for('user_bp.user_onlineacc'))

    platform = request.form.get('platform')
    username = request.form.get('username')

    try:
        conn = get_db_connection()
        cursor = conn.cursor()

        cursor.execute("""
            UPDATE online_accounts SET Platform_Name = %s, UserName = %s WHERE user_id = %s
        """, (platform, username, user_id))
        conn.commit()

        flash("Online account updated successfully!", "success")

    except mysql.connector.Error as err:
        conn.rollback()
        flash("Error updating online accounts!", "danger")
        logging.error(f"Database error: {err}")

    finally:
        cursor.close()
        conn.close()

    return redirect(url_for('user_bp.user_onlineacc'))

@user_bp.route('/authentication')
@login_required
def user_authentication():
    user = session.get('user', {})
    return render_template('user/user_authentication.html', user=user)

@user_bp.route('/update_authentication', methods=['POST'])
@login_required
def update_authentication():
    user_id = session.get('user', {}).get('user_id')

    if not user_id:
        flash("User not found!", "danger")
        return redirect(url_for('user_bp.user_authentication'))

    new_password = request.form.get('password')

    try:
        conn = get_db_connection()
        cursor = conn.cursor()

        cursor.execute("UPDATE authentication SET Password = %s WHERE user_id = %s", (new_password, user_id))
        conn.commit()

        flash("Authentication details updated successfully!", "success")

        if 'user' in session:
            session['user']['password'] = new_password  

        logging.debug("Password updated successfully!")

    except mysql.connector.Error as err:
        flash("Database error occurred!", "danger")
        logging.error(f"Error: {err}")

    finally:
        cursor.close()
        conn.close()

    return redirect(url_for('user_bp.user_authentication'))