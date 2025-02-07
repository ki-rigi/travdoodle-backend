from random import randint
from faker import Faker
import random
from datetime import datetime, timedelta
from flask_bcrypt import Bcrypt

# Local imports
from app import app  # Import Flask app
from model import db, User, Itinerary, Destination, Activity  # Import your models

bcrypt = Bcrypt()
fake = Faker()

def generate_random_dates():
    """Generate realistic vacation start and end dates."""
    start_date = fake.date_between(start_date='-1y', end_date='today')
    end_date = start_date + timedelta(days=random.randint(3, 14))  # Trips last 3-14 days
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

        # Create random users and commit them
        users = []
        for _ in range(4):  # Generate 4 users
            user = User(
                username=fake.unique.user_name(),
                email=fake.unique.email(),
                password="password123"  # Gets hashed automatically
            )
            db.session.add(user)
        db.session.commit()

        # Retrieve users again
        users = User.query.all()

        # Create itineraries for each user
        itineraries = []
        for user in users:
            for _ in range(2):  # Create 2 itineraries per user
                start_date, end_date = generate_random_dates()
                itinerary = Itinerary(
                    name=fake.city(),
                    start_date=start_date,
                    end_date=end_date,
                    user_id=user.id
                )
                itineraries.append(itinerary)
                db.session.add(itinerary)

        db.session.commit()

        # Retrieve itineraries
        itineraries = Itinerary.query.all()

        # Create destinations for each itinerary
        destinations = []
        for itinerary in itineraries:
            for _ in range(2):  # Create 2 destinations per itinerary
                destination = Destination(
                    name=fake.city(),
                    itinerary_id=itinerary.id  # Associate with itinerary
                )
                destinations.append(destination)
                db.session.add(destination)

        db.session.commit()

        # Retrieve destinations
        destinations = Destination.query.all()

        # Create activities for each destination
        activities = []
        for destination in destinations:
            for _ in range(2):  # Create 2 activities per destination
                activity = Activity(
                    name=fake.catch_phrase(),  # More natural activity name
                    description=fake.sentence(),  # Full sentence for description
                    destination_id=destination.id
                )
                activities.append(activity)
                db.session.add(activity)

        db.session.commit()

        print("Database reset and seeding completed! ✅")
