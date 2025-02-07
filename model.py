from sqlalchemy_serializer import SerializerMixin
from sqlalchemy.orm import validates
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import MetaData
from sqlalchemy.ext.hybrid import hybrid_property
from flask_bcrypt import Bcrypt
from datetime import date
import re

# Define metadata, instantiate db
metadata = MetaData(naming_convention={
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
})
db = SQLAlchemy(metadata=metadata)
bcrypt = Bcrypt()

# User Model
class User(db.Model, SerializerMixin):
    __tablename__ = 'users'

    serialize_rules = ('-password', '-itineraries.user')  # Exclude password and avoid circular reference

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), nullable=False, unique=True)
    email = db.Column(db.String(120), nullable=False, unique=True)
    _password_hash = db.Column(db.String(128), nullable=False)  # Ensuring enough space for bcrypt hashes

    # Relationship with Itineraries
    itineraries = db.relationship("Itinerary", back_populates="user", cascade="all, delete-orphan")

    def __repr__(self):
        return f'<User ID: {self.id}, Username: {self.username}, Email: {self.email}>'

    @validates('username')
    def validate_username(self, key, username):
        if not username:
            raise ValueError('Username is required')
        if len(username) > 50:
            raise ValueError('Username must be less than 50 characters')
        return username

    @validates('email')
    def validate_email(self, key, email):
        if not email:
            raise ValueError('Email is required')
        
        email_pattern = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
        if not re.match(email_pattern, email):
            raise ValueError('Invalid email format')

        return email

    @hybrid_property
    def password(self):
        return self._password_hash

    @password.setter
    def password(self, plaintext_password):
        self._password_hash = bcrypt.generate_password_hash(plaintext_password).decode('utf-8')

    def check_password(self, plaintext_password):
        return bcrypt.check_password_hash(self._password_hash, plaintext_password)


# Itinerary Model
class Itinerary(db.Model, SerializerMixin):
    __tablename__ = 'itineraries'

    serialize_rules = ('-user.itineraries')  # Prevent circular reference 

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    start_date = db.Column(db.Date, nullable=False)
    end_date = db.Column(db.Date, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)

    # Relationship with User
    user = db.relationship("User", back_populates="itineraries")
    
    # Relationship with Destinations
    destinations = db.relationship("Destination", back_populates="itinerary", cascade="all, delete-orphan")

    def __repr__(self):
        return f"<Itinerary {self.name} | {self.start_date} to {self.end_date}>"

    @validates('name')
    def validate_name(self, key, name):
        if not name or len(name) > 100:
            raise ValueError("Itinerary name must be between 1 and 100 characters.")
        return name

    @validates('start_date', 'end_date')
    def validate_dates(self, key, date_value):
        if not date_value:
            raise ValueError(f"{key.replace('_', ' ').capitalize()} is required.")
        
        # Ensure start_date is before end_date
        if key == 'end_date' and self.start_date > date_value:
            raise ValueError("End date must be after start date.")
        
        return date_value


# Destination Model
class Destination(db.Model, SerializerMixin):
    __tablename__ = 'destinations'

    serialize_rules = ('-itinerary.destinations')  # Prevent circular reference

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    itinerary_id = db.Column(db.Integer, db.ForeignKey('itineraries.id'), nullable=False)

    # Relationship with Itinerary
    itinerary = db.relationship("Itinerary", back_populates="destinations")

    #Relationship with Activity
    activities = db.relationship("Activity", back_populates="destination", cascade ='all, delete-orphan')

    def __repr__(self):
        return f"<Destination {self.name}>"

    @validates('name')
    def validate_name(self, key, name):
        if not name or len(name) > 200:
            raise ValueError("Destination name must be between 1 and 200 characters.")
        return name
    

# Activity Model
class Activity(db.Model, SerializerMixin):
    __tablename__ = 'activities'
    
    serialize_rules = ('-destination.activities',)  # Prevent circular reference
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    description = db.Column(db.String(500), nullable=False)  
    destination_id = db.Column(db.Integer, db.ForeignKey('destinations.id'), nullable=False)
                               
    # Relationship with Destination
    destination = db.relationship("Destination", back_populates="activities")
    
    def __repr__(self):
        return f"<Activity {self.name} | {self.description[:30]}...>"

    @validates('name')
    def validate_name(self, key, name):
        if not name or len(name.strip()) == 0:
            raise ValueError("Activity name cannot be empty.")
        if len(name) > 200:
            raise ValueError("Activity name must be between 1 and 200 characters.")
        return name.strip()
    
    @validates('description')
    def validate_description(self, key, description):
        if not description or len(description.strip()) == 0:
            raise ValueError("Description cannot be empty.")
        if len(description) > 500:
            raise ValueError("Description must be between 1 and 500 characters.")
        return description.strip()

    




                               