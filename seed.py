from random import randint
from faker import Faker
import random
import phonenumbers
from datetime import datetime, timedelta



# Local imports
from app import app  # Import Flask app 
from model import db

if __name__ == '__main__':
    fake = Faker()
    # Initialize Flask app context
    with app.app_context():
        print("Starting seed...")