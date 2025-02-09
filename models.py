from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

class User(db.Model):
    __tablename__ = 'users'
    
    badge_code = db.Column(db.String, primary_key=True, unique=True, nullable=False)
    name = db.Column(db.String, nullable=False)
    email = db.Column(db.String, unique=True, nullable=False)
    phone = db.Column(db.String)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f'<User {self.name}>'

class Activity(db.Model):
    __tablename__ = 'activities'

    activity_name = db.Column(db.String, primary_key=True)
    activity_category = db.Column(db.String, nullable=False)

    def __repr__(self):
        return f'<Activity {self.activity_name}>'

class Scan(db.Model):
    __tablename__ = 'scans'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_badge_code = db.Column(db.String, db.ForeignKey('users.badge_code'), nullable=False)
    activity_name = db.Column(db.String, db.ForeignKey('activities.activity_name'), nullable=False)
    scanned_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    user = db.relationship('User', backref='scans')
    activity = db.relationship('Activity', backref='scans')

    def __repr__(self):
        return f'<Scan {self.user_badge_code} at {self.activity_name}>'