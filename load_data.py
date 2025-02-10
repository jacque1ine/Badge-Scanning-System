import json
from datetime import datetime
from sqlite3 import IntegrityError
from models.models import db, User, Activity, Scan

def populate_db_from_json(json_file_path):
    """
    Populates the database with user, activity, and scan data from a JSON file.
    
    Args:
        json_file_path (str): The file path to the JSON file containing user data.
    """
    if User.query.count() > 0 or Activity.query.count() > 0 or Scan.query.count() > 0:
        print("Database is not empty. Data loading skipped.")
        return  # Exit if there are existing records
    
    with open(json_file_path, 'r') as file:
        users_data = json.load(file)

        for user_data in users_data:
            badge_code = user_data.get('badge_code', None)
            if badge_code == "":
                badge_code = None  
            existing_user = User.query.filter_by(email=user_data['email']).first()
            if existing_user:
                existing_user.updated_at = datetime.now()
                existing_user.name = user_data['name']
                existing_user.phone = user_data['phone']
                existing_user.badge_code = badge_code  

                user = existing_user  
            else:
                user = User(
                    email=user_data['email'],
                    name=user_data['name'],
                    badge_code=badge_code,  
                    phone=user_data.get('phone'),
                    updated_at=datetime.utcnow()
                )
                db.session.add(user)

            for scan_data in user_data['scans']:
                activity = Activity.query.filter_by(activity_name=scan_data['activity_name']).first()
                
                if activity is None:
                    activity = Activity(
                        activity_name=scan_data['activity_name'],
                        activity_category=scan_data['activity_category']
                    )
                    db.session.add(activity)

                scan = Scan(
                    user_id=user.id,  
                    activity_name=activity.activity_name,
                    scanned_at=datetime.fromisoformat(scan_data['scanned_at'])
                )
                db.session.add(scan)

            user.updated_at = datetime.utcnow()

        try:
            db.session.commit()
        except IntegrityError as e:
            db.session.rollback()
            print(f"Database Integrity Error: {e}")