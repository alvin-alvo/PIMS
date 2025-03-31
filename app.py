from flask import Flask, render_template
from routes.user_routes import user_bp
from routes.auth_routes import auth_bp
from routes.admin_routes import admin_bp

from db import get_db_connection


app = Flask(__name__, template_folder='templates')

get_db_connection()


app.register_blueprint(admin_bp, url_prefix='/admin')
app.register_blueprint(user_bp, url_prefix='/user')
app.register_blueprint(auth_bp, url_prefix='/auth')

@app.route("/")
def home():
    return render_template('index.html')
    
if __name__ == "__main__":
    app.run(debug=True)