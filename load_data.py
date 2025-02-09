# services/data_loader.py
import json
from datetime import datetime
from models import db, User, Activity, Scan
from sqlalchemy.exc import IntegrityError

def populate_db_from_json(json_file_path):
    with open(json_file_path, 'r') as file:
        users_data = json.load(file)

        for user_data in users_data:
            # Get badge_code and set it to None if it is an empty string
            badge_code = user_data.get('badge_code', None)
            if badge_code == "":
                badge_code = None  # Treat empty string as NULL for the database

            # Check for existing user by email to handle updates
            existing_user = User.query.filter_by(email=user_data['email']).first()
            if existing_user:
                # Update fields for existing user
                existing_user.updated_at = datetime.utcnow()
                existing_user.name = user_data['name']
                existing_user.phone = user_data['phone']
                existing_user.badge_code = badge_code  # Set to None if badge code was empty

                user = existing_user  # Continue processing with existing user
            else:
                # Create a new User instance
                user = User(
                    email=user_data['email'],
                    name=user_data['name'],
                    badge_code=badge_code,  # Can be empty or None
                    phone=user_data.get('phone'),
                    updated_at=datetime.utcnow()
                )
                db.session.add(user)

            # Process scans for the user
            for scan_data in user_data['scans']:
                # Ensure the activity exists
                activity = Activity.query.filter_by(activity_name=scan_data['activity_name']).first()
                
                # Create Activity if it doesn't exist
                if activity is None:
                    activity = Activity(
                        activity_name=scan_data['activity_name'],
                        activity_category=scan_data['activity_category']
                    )
                    db.session.add(activity)

                # Create Scan instance referencing user_email
                scan = Scan(
                    user_email=user.email,  # Reference the user's email
                    activity_name=activity.activity_name,
                    scanned_at=datetime.fromisoformat(scan_data['scanned_at'])
                )
                db.session.add(scan)

            # Update the user's updated_at timestamp again after processing scans
            user.updated_at = datetime.utcnow()

        # Commit all changes to the database
        try:
            db.session.commit()
        except IntegrityError as e:
            db.session.rollback()
            print(f"Database Integrity Error: {e}")