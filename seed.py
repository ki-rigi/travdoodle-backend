from random import randint
from faker import Faker
import random
from datetime import datetime, timedelta
from flask_bcrypt import Bcrypt

# Local imports
from app import app  # Import Flask app
from model import db, User, Itinerary  # Import your User and Itinerary models

bcrypt = Bcrypt()
fake = Faker()

def generate_random_dates():
    """Generate random start and end dates."""
    start_date = fake.date_between(start_date='-1y', end_date='today')
    end_date = fake.date_between(start_date=start_date, end_date='+1y')  # End date after start date
    return start_date, end_date

if __name__ == '__main__':
    with app.app_context():
        print("Starting seed...")

        # Drop all tables and recreate them
        db.drop_all()
        db.create_all()

        # Create user Felicia
        felicia = User(
            username='felicia',
            email='nkathafelicia@gmail.com',
            password='felicia',
        )
        db.session.add(felicia)
        db.session.commit()  # Commit to get the user id

        # Create random users and commit them to get their IDs
        users = []
        for _ in range(4):  # Generate 4 users
            user = User(
                username=fake.user_name(),
                email=fake.email(),
                password="password123"  # Gets hashed automatically via @password.setter
            )
            db.session.add(user)
        db.session.commit()  # Now commit to assign IDs to users

        # Retrieve users again with IDs assigned
        users = User.query.all()

        # Create itineraries for each user
        itineraries = []
        for user in users:
            for _ in range(3):  # Create 3 itineraries per user
                start_date, end_date = generate_random_dates()
                itinerary = Itinerary(
                    name=fake.city(),
                    start_date=start_date,
                    end_date=end_date,
                    user_id=user.id  # Associate each itinerary with a user
                )
                itineraries.append(itinerary)

        # Add and commit itineraries at once
        db.session.bulk_save_objects(itineraries)
        db.session.commit()

        print("Database reset and seeding completed with users and itineraries! ✅")
