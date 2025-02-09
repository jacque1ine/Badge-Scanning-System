from datetime import datetime
from flask import Blueprint, jsonify, abort, request
from models import db, User, Activity, Scan

scan_bp = Blueprint('scan', __name__)

@scan_bp.route('/scan/<string:badge_code>', methods=['PUT'])
def add_scan(badge_code):
    # Look for the user associated with the provided badge code
    user = User.query.filter_by(badge_code=badge_code).first()
    if not user:
        abort(404, description="User not found with the provided badge code.")  # User must exist

    data = request.get_json()
    activity_name = data.get('activity_name')
    activity_category = data.get('activity_category')

    if not activity_name or not activity_category:
        abort(400, description="Both 'activity_name' and 'activity_category' are required.")  # Bad request if key fields are missing

    # Check if the activity already exists; if not, create it
    activity = Activity.query.filter_by(activity_name=activity_name).first()
    if activity is None:
        activity = Activity(
            activity_name=activity_name,
            activity_category=activity_category
        )
        db.session.add(activity)  

    # Create a new scan associated with the user
    scan = Scan(
        user_id=user.id, 
        activity_name=activity.activity_name,
        scanned_at=datetime.now() 
    )
    db.session.add(scan)  
    user.updated_at = datetime.now()

    try:
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        abort(500, description="An error occurred while adding the scan.") 
        
    return jsonify({
        'user_id': user.id, # primary key
        'user_email': user.email, #more readable 
        'activity_name': scan.activity_name,
        'scanned_at': scan.scanned_at.isoformat(),
        'activity_category': activity.activity_category  
    }), 201  