# routes/scan_routes.py
from datetime import datetime
from flask import Blueprint, jsonify, abort, request
from models.models import db, User, Activity, Scan
from sqlalchemy import func

scan_bp = Blueprint('scan', __name__)

@scan_bp.route('/scan/<string:badge_code>', methods=['PUT'])
def add_scan(badge_code):
    """
    Add a new scan for a user associated with the provided badge code.

    Args:
        badge_code (str): The badge code of the user.

    Returns:
        JSON response containing scan details, or raises a 404 error if the user
        is not found, 400 if the required data is missing, and 500 for other errors.
    """
    user = User.query.filter_by(badge_code=badge_code).first()
    if not user:
        abort(404, description="User not found with the provided badge code.")
    
    data = request.get_json()
    if not data:  # Check if JSON is parsed 
        abort(400, description="Missing or invalid JSON body.")  # Bad request if no JSON
        
    activity_name = data.get('activity_name')
    activity_category = data.get('activity_category')
    
    if not activity_name or not activity_category:
        abort(400, description="Both 'activity_name' and 'activity_category' are required.")

    activity = Activity.query.filter_by(activity_name=activity_name).first()
    if activity is None:
        activity = Activity(activity_name=activity_name, activity_category=activity_category)
        db.session.add(activity)

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
        'user_id': user.id,
        'user_email': user.email,
        'activity_name': scan.activity_name,
        'scanned_at': scan.scanned_at.isoformat(),
        'activity_category': activity.activity_category
    }), 201  

@scan_bp.route('/scans', methods=['GET'])
def get_scan_data():
    """
    Retrieve aggregated scan data based on optional filters.

    Query Parameters:
        min_frequency (int): Minimum number of scans to be included in the result.
        max_frequency (int): Maximum number of scans to be included in the result.
        activity_category (str): The category of the activity to filter by.

    Returns:
        JSON response containing a list of activities and their scan frequencies.
    """
    min_frequency = request.args.get('min_frequency', default=0, type=int)
    max_frequency = request.args.get('max_frequency', default=None, type=int)
    activity_category = request.args.get('activity_category', default=None, type=str)

    # Build the query to count scans per activity with optional filters
    query = db.session.query(
        Activity.activity_name,
        Activity.activity_category,
        func.count(Scan.id).label('frequency')
    ).outerjoin(Scan, Activity.activity_name == Scan.activity_name)  # Left join to include activities with no scans

    if activity_category:
        query = query.filter(Activity.activity_category == activity_category)

    query = query.group_by(Activity.activity_name, Activity.activity_category)

    query = query.having(func.count(Scan.id) >= min_frequency)
    if max_frequency is not None:
        query = query.having(func.count(Scan.id) <= max_frequency)

    results = query.all()

    scan_data = [
        {
            'activity_name': result.activity_name,
            'activity_category': result.activity_category,
            'frequency': result.frequency
        } for result in results
    ]
    
    return jsonify(scan_data), 200 