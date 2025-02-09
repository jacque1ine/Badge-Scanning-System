from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import os

# Import your models
from models import db, User, Activity, Scan 

# Initialize Flask application
app = Flask(__name__)

# Define the path to the SQLite database
file_path = os.path.abspath(os.getcwd()) + "/data/database.db"  
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + file_path
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False 
db.init_app(app)

with app.app_context():
    db.create_all()  

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=3000) 