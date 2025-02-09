# routes/user_routes.py
from datetime import datetime
from sqlite3 import IntegrityError
from flask import Blueprint, jsonify, abort, request
from models import db, User, Scan

user_bp = Blueprint('user', __name__)

@user_bp.route('/users', methods=['GET'])
def get_users():
    users = User.query.all()  # Retrieve all users from the database
    user_list = []
    
    for user in users:
        
        user_data = {
            'id': user.id,  
            'email': user.email,
            'name': user.name,
            'badge_code': user.badge_code,
            'phone': user.phone,
            'updated_at': user.updated_at.isoformat(),
            'scans': user.all_user_scans
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
        'scans': user.all_user_scans
    }

    return jsonify(user_data), 200  

@user_bp.route('/users/<int:user_id>', methods=['PUT'])
def update_user(user_id):
    user = User.query.get(user_id)
    if not user:
        abort(404, description="User not found.")  # User must exist

    # Get the JSON data from the request
    data = request.get_json()

    # Retrieve existing user data for batch checks
    new_email = data.get('email', user.email)  # Existing email if not provided
    new_badge_code = data.get('badge_code', user.badge_code)  # Existing badge_code if not provided

    # Batch check for uniqueness
    existing_email_user = User.query.filter_by(email=new_email).first()
    existing_badge_user = User.query.filter_by(badge_code=new_badge_code).first()
    
    # Check uniqueness of email, excluding the current user
    if existing_email_user and existing_email_user.id != user.id:
        abort(400, description="Email already in use.")  # Email conflict
    
    # Check uniqueness of badge_code, excluding the current user
    if new_badge_code and existing_badge_user and existing_badge_user.id != user.id:
        abort(400, description="Badge code already in use.")  # Badge code conflict

    # Update user fields
    user.name = data.get('name', user.name)  
    user.phone = data.get('phone', user.phone)
    user.email = new_email  
    user.badge_code = new_badge_code 
    user.updated_at = datetime.now()  
   
    # Commit the changes to the database
    try:
        db.session.commit()
    except IntegrityError as e:
        db.session.rollback()
        abort(500, description="An error occurred while updating the user.")  # Handle unexpected issues

    return jsonify({
        'id': user.id,  
        'email': user.email,
        'name': user.name,
        'badge_code': user.badge_code,
        'phone': user.phone,
        'updated_at': user.updated_at.isoformat(),
        'scans': user.all_user_scans


    }), 200  #