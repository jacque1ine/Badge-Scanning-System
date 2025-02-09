from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)  # Unique ID for each user
    email = db.Column(db.String, unique=True, nullable=False)  
    name = db.Column(db.String, nullable=False)
    phone = db.Column(db.String, nullable=False)
    badge_code = db.Column(db.String, unique=True, nullable=True) 
    updated_at = db.Column(db.DateTime, default=datetime.now, onupdate=datetime.now)  

    def __repr__(self):
        return f'<User {self.name}>'

    @property
    def all_user_scans(self):
        return [
            {
                'activity_name': scan.activity_name,
                'scanned_at': scan.scanned_at.isoformat(),
                'activity_category': scan.activity.activity_category
            } for scan in self.scans
        ]

class Activity(db.Model):
    __tablename__ = 'activities'
    
    activity_name = db.Column(db.String, primary_key=True)
    activity_category = db.Column(db.String, nullable=False)

    def __repr__(self):
        return f'<Activity {self.activity_name}>'

class Scan(db.Model):
    __tablename__ = 'scans'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_email = db.Column(db.String, db.ForeignKey('users.email', ondelete='CASCADE'), nullable=True, index=True)  # Changed to reference email
    activity_name = db.Column(db.String, db.ForeignKey('activities.activity_name', ondelete='CASCADE'), nullable=False)
    scanned_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    user = db.relationship('User', backref='scans')
    activity = db.relationship('Activity', backref='scans')

    def __repr__(self):
        return f'<Scan {self.user_email} at {self.activity_name}>'
    