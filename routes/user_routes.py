from sqlalchemy.orm import joinedload
# routes/user_routes.py
from flask import Blueprint, jsonify
from models import db, User

user_bp = Blueprint('user', __name__)

@user_bp.route('/users', methods=['GET'])
def get_users():
    # Retrieve all users with their scans using eager loading
    users = User.query.options(joinedload(User.scans)).all()  
    user_list = []
    
    for user in users:
        # Gather scan data directly from the eagerly loaded scans
        scans = [
            {
                'activity_name': scan.activity_name,
                'scanned_at': scan.scanned_at.isoformat(),
                'activity_category': scan.activity.activity_category  # Load activity category
            }
            for scan in user.scans
        ]
        
        user_data = {
            'email': user.email,
            'name': user.name,
            'badge_code': user.badge_code,
            'phone': user.phone,
            'updated_at': user.updated_at.isoformat(), #also includes updated at time which is different from the data that is initially loaded into db
            'scans': scans
        }
        user_list.append(user_data)
    
    return jsonify(user_list)