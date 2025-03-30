from flask import Flask
from db import get_db_connection
from routes.user_routes import user_bp
from routes.auth_routes import auth_bp
from routes.admin_routes import admin_bp

app = Flask(__name__)

app.register_blueprint(admin_bp, url_prefix='/api/admin')
app.register_blueprint(user_bp, url_prefix='/api')
app.register_blueprint(auth_bp, url_prefix='/api')

@app.route("/")
def home():
    return "Welcome to the Personal Information System!"
    
if __name__ == "__main__":
    app.run(debug=True)