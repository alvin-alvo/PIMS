from flask import Flask
from db import get_db_connection

app = Flask(__name__)

@app.route("/")
def home():
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SHOW TABLES")
        tables = cursor.fetchall()
        cursor.close()
        conn.close()
        return f"Connected to MySQL! Tables: {tables}"
    except Exception as e:
        return f"Error: {str(e)}"
    
if __name__ == "__main__":
    app.run(debug=True)