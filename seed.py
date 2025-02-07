from random import randint, choice
from faker import Faker
import random
from datetime import datetime, timedelta
from flask_bcrypt import Bcrypt

# Local imports
from app import app  # Import Flask app
from model import db, User, Itinerary, Destination, Activity, Accommodation, PackingItem  # Import models

bcrypt = Bcrypt()
fake = Faker()

def generate_random_dates():
    """Generate realistic start and end dates for trips and accommodations."""
    start_date = fake.date_between(start_date='-1y', end_date='today')
    end_date = start_date + timedelta(days=random.randint(3, 14))  # 3-14 days duration
    return start_date, end_date

# Adding random packing items to each itinerary
def generate_random_packing_items(itinerary):
    packing_items = [
        "Shirt", "Pants", "Toothbrush", "Laptop", "Sunscreen", 
        "Socks", "Hat", "Toothpaste", "Charger", "Shoes", 
        "Passport", "Travel Tickets", "Travel Pillow", "Camera", "Hand Sanitizer", 
        "Medication", "First Aid Kit", "Wallet", "Snacks", "Power Bank", 
        "Sunglasses", "Maps", "Credit Cards", "Adapter", "Towel", 
        "Rain Jacket", "Swimming Suit", "Flip Flops", "Brush", "Deodorant",
        "Book", "Notebook", "Pen", "Earphones", "Emergency Contact List"
    ]

    # Randomly choose 5 items and assign a quantity and packed status
    for _ in range(5):
        item_name = random.choice(packing_items)
        quantity = randint(1, 3)  # Random quantity between 1 and 3
        packed = choice([True, False])  # Randomly choose if the item is packed

        packing_item = PackingItem(
            item_name=item_name,
            quantity=quantity,
            packed=packed,
            itinerary_id=itinerary.id
        )
        db.session.add(packing_item)

if __name__ == '__main__':
    with app.app_context():
        print("Starting seed...")

        # Drop and recreate tables
        db.drop_all()
        db.create_all()

        # Create user Felicia
        felicia = User(
            username='felicia',
            email='nkathafelicia@gmail.com',
            password='felicia',
        )
        db.session.add(felicia)
        db.session.commit()

        # Create random users
        users = []
        for _ in range(4):
            user = User(
                username=fake.unique.user_name(),
                email=fake.unique.email(),
                password="password123"
            )
            db.session.add(user)
        db.session.commit()

        users = User.query.all()

        # Create itineraries
        itineraries = []
        for user in users:
            for _ in range(2):
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

        itineraries = Itinerary.query.all()

        # Create destinations
        destinations = []
        for itinerary in itineraries:
            for _ in range(2):
                destination = Destination(
                    name=fake.city(),
                    itinerary_id=itinerary.id
                )
                destinations.append(destination)
                db.session.add(destination)

        db.session.commit()

        destinations = Destination.query.all()

        # Create activities
        activities = []
        for destination in destinations:
            for _ in range(2):
                activity = Activity(
                    name=fake.catch_phrase(),
                    description=fake.sentence(),
                    destination_id=destination.id
                )
                activities.append(activity)
                db.session.add(activity)

        db.session.commit()

        # Create accommodations
        accommodations = []
        for destination in destinations:
            check_in_date, check_out_date = generate_random_dates()  # Ensure correct dates

            accommodation = Accommodation(
                name=fake.company(),
                address=fake.address(),
                check_in_date=check_in_date,
                check_out_date=check_out_date,
                price=fake.pyfloat(left_digits=3, right_digits=2, positive=True),
                destination_id=destination.id
            )

            accommodations.append(accommodation)
            db.session.add(accommodation)

        db.session.commit()

        # Add random packing items to each itinerary
        for itinerary in itineraries:
            generate_random_packing_items(itinerary)

        db.session.commit()

        print("Database reset and seeding completed! ✅")
