from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import os
from models import db, User, Activity, Scan 
from load_data import populate_db_from_json

app = Flask(__name__)

file_path = os.path.abspath(os.getcwd()) + "/data/database.db"  
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + file_path
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False 
db.init_app(app)

with app.app_context():
    db.create_all()
    populate_db_from_json(os.path.join(os.path.abspath(os.getcwd()), 'data/example_data.json'))


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=3000) 