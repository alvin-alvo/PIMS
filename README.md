#  Personal Information Management System (PIMS)

A centralized **Personal Information Management System** built using **Flask(Python)** that helps individuals securely store, manage, and update various personal information categories such as contact details, addresses, education, work experience, etc.


##  Features

##### **User Authentication**
  - Register and login system

##### **Personal Data Management**
  - Basic user information
  - Contact
  - Address
  - Education 
  - Work experience
 
##### **Admin Privileges**
  - Admin can view or delete users
  - Cannot alter personal data of users


##  Tech Stack

| Layer          | Technology      |
|----------------|-----------------|
| Backend        | Flask (Python)  |
| Frontend       | HTML, CSS       |
| Database       | MySQL           |
| Session/Logging| Flask Session   |



##  Database Schema Overview

###  Main Tables

- `users` – Stores basic user details
- `admin` – Stores basic admin details

###  Linked Tables

- `address`
- `contact`
- `education`
- `work_experience`
- `authentication`

Each table is linked via the `user_id` foreign key.


##  Getting Started

###  Prerequisites

- Python 3.8+ 
- MySQL server
- pip (Python package manager)

### 1. Clone the Repository
```bash
git clone https://github.com/alvin-alvo/PIMS.git
cd personal-information-system
```

### 2. Create and Activate a Virtual Environment
```sh
python -m venv env
env\Scripts\activate
```

### 3. Install Dependencies
```sh
pip install -r requirements.txt
```

### 4. Configure Database
1. Create a Database in MySQL 
```sql
CREATE DATABASE personalinformationsystem;
```
2. Import schema
```bash
mysql -u root -p personalinformationsystem < schema.sql
```
3. Update Database connection in db.py or use .env
```python
conn = mysql.connector.connect(
    host='localhost',
    user='your_mysql_user',
    password='your_mysql_password',
    database='personalinformationsystem'
)
```

### 5. Run the Flask App
```bash
python app.py
```
Visit http://localhost:5000 in your browser.

## Still to come

#### Pages
- Finance 
- Online Accounts
- Emergency Contacts
#### Features
- Activity tracking
- Improved security
- Add more than one set of data
- Exporting data in one click 
- Resume / CV maker

### Want to improve PIMS?
#### Open a Pull Request

