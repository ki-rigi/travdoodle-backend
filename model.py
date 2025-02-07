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

    serialize_rules = ('-user.itineraries', '-destinations.itinerary', '-packing_items.itinerary')  # Prevent circular references

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    start_date = db.Column(db.Date, nullable=False)
    end_date = db.Column(db.Date, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)

    # Relationship with User
    user = db.relationship("User", back_populates="itineraries")
    
    # Relationship with Destinations
    destinations = db.relationship("Destination", back_populates="itinerary", cascade="all, delete-orphan")

    # Relationship with Packing Items
    packing_items = db.relationship("PackingItem", back_populates="itinerary", cascade="all, delete-orphan")

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

    serialize_rules = ('-itinerary.destinations', '-accommodations.destination')  # Prevent circular reference
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    itinerary_id = db.Column(db.Integer, db.ForeignKey('itineraries.id'), nullable=False)

    # Relationship with Itinerary
    itinerary = db.relationship("Itinerary", back_populates="destinations")

    #Relationship with Activity
    activities = db.relationship("Activity", back_populates="destination", cascade ='all, delete-orphan')

    # Relationship with Accommodations
    accommodations = db.relationship("Accommodation", back_populates="destination", cascade='all, delete-orphan')

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
    

# Accommodation Model
class Accommodation(db.Model, SerializerMixin):
    __tablename__ = 'accommodations'
    
    serialize_rules = ('-destination.accommodations',)  # Prevent circular reference
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    address = db.Column(db.String(300), nullable=False)
    check_in_date = db.Column(db.Date, nullable=False)
    check_out_date = db.Column(db.Date, nullable=False)
    price = db.Column(db.Float, nullable=False)
    destination_id = db.Column(db.Integer, db.ForeignKey('destinations.id'), nullable=False)
    
    # Relationship with Destination
    destination = db.relationship("Destination", back_populates="accommodations")
    
    def __repr__(self):
        return f"<Accommodation {self.name} | {self.address} | ${self.price:.2f}>"
    
    @validates('name')
    def validate_name(self, key, name):
        if not name or len(name.strip()) == 0:
            raise ValueError("Accommodation name cannot be empty.")
        if len(name) > 200:
            raise ValueError("Accommodation name must be between 1 and 200 characters.")
        return name.strip()
    
    @validates('address')
    def validate_address(self, key, address):
        if not address or len(address.strip()) == 0:
            raise ValueError("Address cannot be empty.")
        if len(address) > 300:
            raise ValueError("Address must be between 1 and 300 characters.")
        return address.strip()
    
    @validates('check_in_date', 'check_out_date')
    def validate_dates(self, key, date_value):
        if not date_value:
            raise ValueError(f"{key.replace('_', ' ').capitalize()} is required.")
        
        if key == 'check_out_date' and self.check_in_date and date_value <= self.check_in_date:
            raise ValueError("Check-out date must be after check-in date.")
        
        return date_value
    
    @validates('price')
    def validate_price(self, key, price):
        if price is None or price < 0:
            raise ValueError("Price must be a positive number.")
        return price
    

    # PackingItem Model
class PackingItem(db.Model, SerializerMixin):
    __tablename__ = 'packing_items'

    serialize_rules = ('-itinerary.packing_items',)  # Prevent circular reference

    id = db.Column(db.Integer, primary_key=True)
    item_name = db.Column(db.String(100), nullable=False)
    quantity = db.Column(db.Integer, nullable=False, default=1)
    packed = db.Column(db.Boolean, default=False, nullable=False)
    itinerary_id = db.Column(db.Integer, db.ForeignKey('itineraries.id'), nullable=False)

    # Relationship with Itinerary
    itinerary = db.relationship("Itinerary", back_populates="packing_items")

    def __repr__(self):
        return f"<PackingItem {self.item_name} (x{self.quantity}) | Packed: {self.packed}>"

    @validates('item_name')
    def validate_item_name(self, key, item_name):
        if not item_name or len(item_name.strip()) == 0:
            raise ValueError("Item name cannot be empty.")
        if len(item_name) > 100:
            raise ValueError("Item name must be between 1 and 100 characters.")
        return item_name.strip()

    @validates('quantity')
    def validate_quantity(self, key, quantity):
        if quantity is None or quantity < 1:
            raise ValueError("Quantity must be at least 1.")
        return quantity


    




                               