from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

# 1. User Table
class User(db.Model):
    __tablename__ = 'User'
    user_id = db.Column(db.String(6), primary_key=True)
    F_Name = db.Column(db.String(50), nullable=False)
    L_Name = db.Column(db.String(50), nullable=False)
    Gender = db.Column(db.Enum('Male', 'Female', 'Other'), nullable=False)
    DOB = db.Column(db.Date)
    Age = db.Column(db.Integer)

    addresses = db.relationship('Address', backref='user', lazy=True, cascade="all, delete-orphan")
    contacts = db.relationship('Contact', backref='user', lazy=True, cascade="all, delete-orphan")
    emergency_contacts = db.relationship('EmergencyContact', backref='user', lazy=True, cascade="all, delete-orphan")
    education = db.relationship('Education', backref='user', lazy=True, cascade="all, delete-orphan")
    work_experience = db.relationship('WorkExperience', backref='user', lazy=True, cascade="all, delete-orphan")
    finances = db.relationship('Finance', backref='user', lazy=True, cascade="all, delete-orphan")
    online_accounts = db.relationship('OnlineAccount', backref='user', lazy=True, cascade="all, delete-orphan")
    
# 2. Address Table
class Address(db.Model):
    __tablename__ = 'Address'
    address_id = db.Column(db.String(6), primary_key=True)
    user_id = db.Column(db.String(6), db.ForeignKey('User.user_id'), nullable=False)
    House_Name = db.Column(db.String(100))
    Street_Name = db.Column(db.String(100), nullable=False)
    City = db.Column(db.String(50), nullable=False)
    State = db.Column(db.String(50), nullable=False)
    Postal_Code = db.Column(db.String(20), nullable=False)
    Country = db.Column(db.String(50), nullable=False)

# 3. Contact Table
class Contact(db.Model):
    __tablename__ = 'Contact'
    contact_id = db.Column(db.String(6), primary_key=True)
    user_id = db.Column(db.String(6), db.ForeignKey('User.user_id'), nullable=False)
    Name = db.Column(db.String(100), nullable=False)
    Email_id = db.Column(db.String(100))
    Phone_No = db.Column(db.String(20), nullable=False)

# 4. Emergency Contact Table
class EmergencyContact(db.Model):
    __tablename__ = 'Emergency_Contact'
    econtact_id = db.Column(db.String(6), primary_key=True)
    user_id = db.Column(db.String(6), db.ForeignKey('User.user_id'), nullable=False)
    Name = db.Column(db.String(100), nullable=False)
    Relation = db.Column(db.String(50), nullable=False)
    Phone_No = db.Column(db.String(20), nullable=False)

# 5. Education Table
class Education(db.Model):
    __tablename__ = 'Education'
    education_id = db.Column(db.String(6), primary_key=True)
    user_id = db.Column(db.String(6), db.ForeignKey('User.user_id'), nullable=False)
    Institution_Name = db.Column(db.String(100), nullable=False)
    Field_Of_Study = db.Column(db.String(100), nullable=False)
    Degree = db.Column(db.String(50), nullable=False)
    Start_Date = db.Column(db.Date, nullable=False)
    End_Date = db.Column(db.Date)

# 6. Work Experience Table
class WorkExperience(db.Model):
    __tablename__ = 'Work_Experience'
    experience_id = db.Column(db.String(6), primary_key=True)
    user_id = db.Column(db.String(6), db.ForeignKey('User.user_id'), nullable=False)
    Company_Name = db.Column(db.String(100), nullable=False)
    Job_Title = db.Column(db.String(100), nullable=False)
    Role = db.Column(db.String(100))
    Start_Date = db.Column(db.Date, nullable=False)
    End_Date = db.Column(db.Date)

# 7. Finance Table
class Finance(db.Model):
    __tablename__ = 'Finance'
    account_id = db.Column(db.String(6), primary_key=True)
    user_id = db.Column(db.String(6), db.ForeignKey('User.user_id'), nullable=False)
    Account_Name = db.Column(db.String(100), nullable=False)
    Account_Type = db.Column(db.String(50), nullable=False)
    Bank_Name = db.Column(db.String(100), nullable=False)
    Account_Number = db.Column(db.String(50), nullable=False)
    IFSC_Code = db.Column(db.String(20))

# 8. Online Accounts Table
class OnlineAccount(db.Model):
    __tablename__ = 'Online_Accounts'
    online_account_id = db.Column(db.String(6), primary_key=True)
    user_id = db.Column(db.String(6), db.ForeignKey('User.user_id'), nullable=False)
    Platform_Name = db.Column(db.String(50), nullable=False)
    UserName = db.Column(db.String(50), nullable=False)
    Profile_Url = db.Column(db.String(255))

# 9. Admin Table
class Admin(db.Model):
    __tablename__ = 'Admin'
    admin_id = db.Column(db.String(6), primary_key=True)
    F_Name = db.Column(db.String(50), nullable=False)
    L_Name = db.Column(db.String(50), nullable=False)
    Email = db.Column(db.String(100), unique=True, nullable=False)
    Phone = db.Column(db.String(20))
    Password = db.Column(db.String(255), nullable=False)

# 10. Authentication Table
class Authentication(db.Model):
    __tablename__ = 'Authentication'
    auth_id = db.Column(db.String(6), primary_key=True)
    user_id = db.Column(db.String(6), db.ForeignKey('User.user_id'))
    admin_id = db.Column(db.String(6), db.ForeignKey('Admin.admin_id'))
    Security_Question = db.Column(db.String(255))
    Answer = db.Column(db.String(255))

# 11. Activity Log Table
class ActivityLog(db.Model):
    __tablename__ = 'Activity_Log'
    log_id = db.Column(db.String(6), primary_key=True)
    user_id = db.Column(db.String(6), db.ForeignKey('User.user_id'))
    admin_id = db.Column(db.String(6), db.ForeignKey('Admin.admin_id'))
    Action = db.Column(db.String(255), nullable=False)
    Timestamp = db.Column(db.DateTime, default=datetime.utcnow)

# 12. Login Activity Table
class LoginActivity(db.Model):
    __tablename__ = 'Login_Activity'
    login_id = db.Column(db.String(6), primary_key=True)
    user_id = db.Column(db.String(6), db.ForeignKey('User.user_id'))
    admin_id = db.Column(db.String(6), db.ForeignKey('Admin.admin_id'))
    IP_Address = db.Column(db.String(45), nullable=False)
    Timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    Status = db.Column(db.Enum('Logged_in', 'Logged_out'), nullable=False)
