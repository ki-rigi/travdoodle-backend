from random import randint
from faker import Faker
import random
from datetime import datetime, timedelta
from flask_bcrypt import Bcrypt

# Local imports
from app import app  # Import Flask app
from model import db, User  # Import your User model

bcrypt = Bcrypt()
fake = Faker()

if __name__ == '__main__':
    with app.app_context():
        print("Starting seed...")

        # Drop all tables and recreate them
        db.drop_all()
        db.create_all()

        users = []
        for _ in range(10):  # Generate 10 users
            user = User(
                username=fake.user_name(),
                email=fake.email(),
                password="password123"  # Gets hashed automatically via @password.setter
            )
            users.append(user)

        # Add and commit all users at once
        db.session.bulk_save_objects(users)
        db.session.commit()

        print("Database reset and seeding completed! ✅")
