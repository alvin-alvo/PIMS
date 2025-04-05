import logging
from flask import Blueprint, request, render_template, session, flash, redirect, url_for
from db import get_db_connection
from auth import login_required
import mysql.connector
from datetime import datetime
from routes.auth_routes import generate_short_uuid

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
        session.modified = True

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
    field = request.form.get('field')
    end = request.form.get('end')
    start = request.form.get('start')

    try:
        # Convert dates to MySQL format (YYYY-MM-DD)
        start_date = datetime.strptime(start, "%Y-%m-%d").date() if start else None
        end_date = datetime.strptime(end, "%Y-%m-%d").date() if end else None
    except ValueError:
        flash("Invalid date format!", "danger")
        return redirect(url_for('user_bp.user_education'))


    print(f"[DEBUG] Education Update Request - Degree: {degree}, Institution_Name: {institution}, Start_Date: {start}, End_Date: {end}, Field_Of_Study: {field} User ID: {user_id}")

    try:
        conn = get_db_connection()
        cursor = conn.cursor()

        # Check if the user has an education record
        cursor.execute("SELECT COUNT(*) FROM education WHERE user_id = %s", (user_id,))
        user_exists = cursor.fetchone()[0]

        if user_exists == 0:
            education_id = generate_short_uuid()  # Generate a unique ID for education entry
            print(f"[INFO] No education record found for User ID: {user_id}. Inserting new record.")
            cursor.execute("""
                INSERT INTO education (education_id, user_id, Degree, Institution_Name, Start_Date, End_Date, Field_Of_Study)
                VALUES (%s, %s, %s, %s, %s, %s, %s)
            """, (education_id, user_id, degree, institution, start, end, field))
        else:
            # If an education record exists, UPDATE it
            cursor.execute("""
                UPDATE education 
                SET Degree = %s, Institution_Name = %s, Start_Date = %s, End_Date =  %s, Field_Of_Study = %s 
                WHERE user_id = %s
            """, (degree, institution, start, end, field, user_id))

        conn.commit()
        flash("Education details updated successfully!", "success")
        print(f"[INFO] Education updated successfully for User ID: {user_id}")

        

        # Update session to reflect new education data
        session['user'].update({
            'degree': degree,
            'institution': institution,
            'field': field,
            'start': str(start_date),
            'end': str(end_date)
        })
        session.modified = True

    except mysql.connector.Error as err:
        conn.rollback()
        flash("Error updating education!", "danger")
        logging.error(f"[ERROR] Database error: {err}")
        print(f"[ERROR] Database error: {err}")

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

    company = request.form.get('company', '').strip()
    title = request.form.get('title', '').strip()
    role = request.form.get('role', '').strip()
    wstart = request.form.get('wstart', None)
    wend = request.form.get('wend', None)

    try:
        wstart_date = datetime.strptime(wstart, "%Y-%m-%d").date() if wstart else None
        wend_date = datetime.strptime(wend, "%Y-%m-%d").date() if wend else None
    except ValueError:
        flash("Invalid date format!", "danger")
        return redirect(url_for('user_bp.user_workexp'))

    print(f"[DEBUG] Work Experience Update Request - Company: {company}, Job Title: {title}, Role: {role}, Start Date: {wstart}, End Date: {wend}, User ID: {user_id}")

    # Validate that required fields are not empty
    if not company or not title:
        flash("Company Name and Job Title are required!", "danger")
        print("[ERROR] Missing required fields: Company Name or Job Title.")
        return redirect(url_for('user_bp.user_workexp'))

    try:
        conn = get_db_connection()
        cursor = conn.cursor()

        # Check if the user has a work experience record
        cursor.execute("SELECT COUNT(*) FROM work_experience WHERE user_id = %s", (user_id,))
        user_exists = cursor.fetchone()[0]

        if user_exists == 0:
            experience_id = generate_short_uuid()  # Generate unique ID
            print(f"[INFO] No work experience found for User ID: {user_id}. Inserting new record.")

            cursor.execute("""
                INSERT INTO work_experience (experience_id, user_id, Company_Name, Job_Title, Role, W_Start_Date, W_End_Date)
                VALUES (%s, %s, %s, %s, %s, %s, %s)
            """, (experience_id, user_id, company, title, role or None, wstart or None, wend or None))
        else:
            print(f"[INFO] Updating work experience for User ID: {user_id}.")
            cursor.execute("""
                UPDATE work_experience 
                SET Company_Name = %s, Job_Title = %s, Role = %s, W_Start_Date = %s, W_End_Date = %s
                WHERE user_id = %s
            """, (company, title, role or None, wstart or None, wend or None, user_id))

        conn.commit()
        flash("Work experience updated successfully!", "success")
        print(f"[INFO] Work experience updated successfully for User ID: {user_id}")

        

        session['user'].update({
            'company': company,
            'title': title,
            'role': role,
            'wstart': str(wstart_date),
            'wend': str(wend_date)
        })
        session.modified = True

    except mysql.connector.Error as err:
        conn.rollback()
        flash("Error updating work experience!", "danger")
        logging.error(f"[ERROR] Database error: {err}")
        print(f"[ERROR] Database error: {err}")

    finally:
        cursor.close()
        conn.close()

    return redirect(url_for('user_bp.user_workexp'))


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

    password = request.form.get('password', '').strip()
    securityq = request.form.get('securityq', "").strip()
    answer = request.form.get('answer', "").strip()

    # Validate input
    if not password:
        flash("Password cannot be empty!", "danger")
        logging.error("[ERROR] Password field is empty.")
        return redirect(url_for('user_bp.user_authentication'))

    try:
        conn = get_db_connection()
        cursor = conn.cursor()

        # Check if the user already has an authentication record
        cursor.execute("SELECT COUNT(*) FROM authentication WHERE user_id = %s", (user_id,))
        user_exists = cursor.fetchone()[0]

        if user_exists == 0:
            # Insert new authentication record
            auth_id = generate_short_uuid()  # Generate a unique auth_id
            print(f"[INFO] No authentication record found for User ID: {user_id}. Inserting new record.")

            cursor.execute("""
                INSERT INTO authentication (auth_id, user_id, Password, Security_Question, Answer) 
                VALUES (%s, %s, %s, %s, %s)
            """, (auth_id, user_id, password, securityq, answer))
        else:
            # Update existing authentication record
            cursor.execute("""
                UPDATE authentication SET Password = %s, Security_Question = %s, Answer = %s  WHERE user_id = %s
            """, (password, securityq, answer, user_id))

        conn.commit()
        flash("Authentication details updated successfully!", "success")
        logging.info("[INFO] Password updated successfully!")

        
        session['user'].update({
            'password': password,
            'securityq': answer,
            'answer': answer,
        })
        session.modified = True

    except mysql.connector.Error as err:
        conn.rollback()
        flash("Database error occurred!", "danger")
        logging.error(f"[ERROR] Database error: {err}")

    finally:
        cursor.close()
        conn.close()

    return redirect(url_for('user_bp.user_authentication'))
