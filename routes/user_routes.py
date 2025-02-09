# routes/user_routes.py
from flask import Blueprint, jsonify, abort
from models import db, User, Scan

user_bp = Blueprint('user', __name__)

@user_bp.route('/users', methods=['GET'])
def get_users():
    users = User.query.all()  # Retrieve all users from the database
    user_list = []
    
    for user in users:
        scans = [
            {
                'activity_name': scan.activity_name,
                'scanned_at': scan.scanned_at.isoformat(),
                'activity_category': scan.activity.activity_category  # Load activity category
            }
            for scan in user.scans
        ]
        
        user_data = {
            'id': user.id,  
            'email': user.email,
            'name': user.name,
            'badge_code': user.badge_code,
            'phone': user.phone,
            'updated_at': user.updated_at.isoformat(),
            'scans': scans
        }
        user_list.append(user_data)

    return jsonify(user_list), 200  

@user_bp.route('/users/<int:user_id>', methods=['GET'])
def get_user_by_id(user_id):
    user = User.query.get(user_id)  
    if not user:
        abort(404, description="User not found.") 

    scans = [
        {
            'activity_name': scan.activity_name,
            'scanned_at': scan.scanned_at.isoformat(),
            'activity_category': scan.activity.activity_category
        }
        for scan in user.scans
    ]

    user_data = {
        'id': user.id, 
        'email': user.email,
        'name': user.name,
        'badge_code': user.badge_code,
        'phone': user.phone,
        'updated_at': user.updated_at.isoformat(),
        'scans': scans
    }

    return jsonify(user_data), 200  