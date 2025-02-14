from flask import Flask, jsonify, request, make_response, session
from flask_restful import Resource,Api
import os
from dotenv import load_dotenv
from flask_cors import CORS
from flask_migrate import Migrate
from model import db, User ,Itinerary, Destination, Accommodation,Activity
from datetime import datetime



app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///travdoodle.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False


migrate = Migrate(app, db)
db.init_app(app)


api = Api(app)

CORS(app)
    

# Load environment variables from .env file
load_dotenv()


from model import db
# Set secret key
app.secret_key = os.environ.get('SECRET_KEY', 'fallback_secret')

# Define home route
@app.route('/')
def home():
    return """
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Travdoodle API</title>
        <style>
            body {
                font-family: Arial, sans-serif;
                margin: 0;
                padding: 0;
                background-color: #f5f5f5;
            }
            .container {
                max-width: 800px;
                margin: 50px auto;
                background-color: #fff;
                padding: 20px;
                border-radius: 10px;
                box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
            }
            h1 {
                text-align: center;
            }
            p {
                margin-bottom: 15px;
            }
            ul {
                list-style-type: none;
                padding-left: 20px;
            }
            li {
                margin-bottom: 5px;
            }
            a {
                color: #007bff;
                text-decoration: none;
            }
            a:hover {
                text-decoration: underline;
            }
        </style>
    </head>
    <body>
        <div class="container">
            <h1>Welcome to travdoodle API</h1>
            <p>This is the API for travdoodle application.</p>
            <p>Endpoints:</p>
            <ul>
                <li><strong>/login</strong> -:POST - User login</li>
                <li><strong>/logout</strong> -:DELETE - User logout</li>
                <li><strong>/check_session</strong>:GET - Check user session</li>
                <li><strong>/users</strong> -:GET - List of all users details</li>
                <li><strong>/users</strong> -:POST - Sign up a new user</li>
                <li><strong>/users/int:id</strong> -:GET - Get a user details</li>
                <li><strong>/users/int:id</strong> -:PATCH - Update a user details</li>
                <li><strong>/users/int:id</strong> -:DELETE - Delete a user</li>
                <li><strong>/itineraries</strong> -:GET - List of all itineraries details</li>
                <li><strong>/itineraries</strong> -:POST - Sign up a new itinerary</li>
                <li><strong>/itineraries/int:id</strong> -:GET - Get itinerary details</li>
                <li><strong>/itineraries/int:id</strong> -:PATCH - Update itinerary details</li>
                <li><strong>/itineraries/int:id</strong> -:DELETE - Delete itinerary</li>
               <li><strong>/destinations</strong> -:GET - List of all destinations details</li>
                <li><strong>/destinations</strong> -:POST - Sign up a new destination</li>
                <li><strong>/destinations/int:id</strong> -:GET - Get destination details</li>
                <li><strong>/destinations/int:id</strong> -:PATCH - Update destinaion details</li>
                <li><strong>/destinations/int:id</strong> -:DELETE - Delete destination</li>
                 <li><strong>/accommodations</strong> -:GET - List of all accommodations details</li>
                <li><strong>/accommodations</strong> -:POST - Sign up a new accommodation</li>
                <li><strong>/accommodations/int:id</strong> -:GET - Get accommodation details</li>
                <li><strong>/accommodations/int:id</strong> -:PATCH - Update accommodation details</li>
                <li><strong>/accommodations/int:id</strong> -:DELETE - Delete accommodation</li>
                 <li><strong>/activities</strong> -:GET - List of all activities details</li>
                <li><strong>/activities</strong> -:POST - Sign up a new activities</li>
                <li><strong>/activities/int:id</strong> -:GET - Get activities details</li>
                <li><strong>/activities/int:id</strong> -:PATCH - Update activity details</li>
                <li><strong>/activities/int:id</strong> -:DELETE - Delete activity</li>
                 
            </ul>
        </div>
    </body>
    </html>
    """
    

# Resource classes
class Login(Resource):    
    def post(self):
        data = request.get_json()
        identifier = data.get('identifier')  # This can be username, email
        password = data.get('password')
        
        if not identifier or not password:
            return {'message': 'username/email and password are required'}, 400
        
        # Check if the input is an email address
        is_email = '@' in identifier
        
        if is_email:
            user = User.query.filter_by(email=identifier).first()
        else:
            user = User.query.filter_by(username=identifier).first()
        
        if not user:
            return {'error': 'User not found'}, 404
        
        if user.check_password(password):
            session['user_id'] = user.id
            return user.to_dict(), 200
        
        return {'error': 'Invalid password'}, 401

class Logout(Resource):
    def delete(self):
        if 'user_id' in session:
            session.pop('user_id')
            return '', 204


class CheckSession(Resource):
    def get(self):
        if 'user_id' in session:
            user_id = session['user_id']
            user = User.query.get(user_id)
            if user:
                return user.to_dict(), 200  
            else:
                return {'message': 'User not found'}, 404
        else:
            return {'message': 'Not logged in'}, 401  
        
# User classes
        
class Users(Resource):
    def get(self):
        users = [user.to_dict() for user in User.query.all()]
        return make_response(jsonify(users), 200)

    def post(self):
        data = request.get_json()

        # Check if the email already exists
        existing_email = User.query.filter_by(email=data['email']).first()
        if existing_email:
            return make_response(jsonify({'message': 'Email already exists'}), 400)

        # Check if the username already exists
        existing_username = User.query.filter_by(username=data['username']).first()
        if existing_username:
            return make_response(jsonify({'message': 'Username already exists'}), 400)

        # Create a new user
        new_user = User(
            username=data['username'],
            email=data['email'],
            password=data['password']
        )

        # Add the new user to the database
        db.session.add(new_user)
        try:
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            return {'error': str(e)}, 500

        return make_response(jsonify({'message': 'User successfully registered', 'user': new_user.to_dict()}), 201)



class UserByID(Resource):
    def get(self, id):
        user = User.query.filter_by(id=id).first().to_dict()
        return make_response(jsonify(user), 200)

    def patch(self, id):
        user = User.query.filter_by(id=id).first()
        data = request.get_json()

        for key, value in data.items():
            setattr(user, key, value)

        db.session.commit()

        return make_response(jsonify(user.to_dict()), 200)

    def delete(self, id):
        user = User.query.filter_by(id=id).first()

        db.session.delete(user)
        db.session.commit()



# Add routes to the API
api.add_resource(Login, '/login')
api.add_resource(Logout, '/logout')
api.add_resource(CheckSession, '/check_session')
api.add_resource(Users, '/users')
api.add_resource(UserByID, '/users/<int:id>')
       


# itinerary classes
        
class Itineraries(Resource):
    def get(self):
        itineraries = [itinerary.to_dict() for itinerary in Itinerary.query.all()]
        return make_response(jsonify(itineraries), 200)

    def post(self):
        data = request.get_json()

        # Validate user exists
        existing_user = User.query.filter_by(id=data['user_id']).first()
        if not existing_user:
            return make_response(jsonify({'message': 'User does not exist'}), 400)

        try:
            # Convert string dates to Python date objects
            start_date = datetime.strptime(data['start_date'], "%Y-%m-%d").date()
            end_date = datetime.strptime(data['end_date'], "%Y-%m-%d").date()
        except ValueError:
            return make_response(jsonify({'error': 'Invalid date format. Use YYYY-MM-DD'}), 400)

        # Create a new itinerary
        new_itinerary = Itinerary(
            name=data['name'],
            start_date=start_date,
            end_date=end_date,
            user_id=data['user_id']
        )

        # Save to the database
        db.session.add(new_itinerary)
        try:
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            return {'error': str(e)}, 500

        return make_response(jsonify({'message': 'Itinerary successfully created', 'itinerary': new_itinerary.to_dict()}), 201)


  
class ItineraryByID(Resource):
    def get(self, id):
        itinerary = Itinerary.query.filter_by(id=id).first().to_dict()
        return make_response(jsonify(itinerary), 200)

    def patch(self, id):
        itinerary = Itinerary.query.filter_by(id=id).first()
        if not itinerary:
            return make_response(jsonify({'error': 'Itinerary not found'}), 404)

        data = request.get_json()

        for key, value in data.items():
            if key in ["start_date", "end_date"]:
                try:
                    # Convert date string to Python date object
                    value = datetime.strptime(value, "%Y-%m-%d").date()
                except ValueError:
                    return make_response(jsonify({'error': f'Invalid format for {key}. Use YYYY-MM-DD'}), 400)

            setattr(itinerary, key, value)

        db.session.commit()

        return make_response(jsonify(itinerary.to_dict()), 200)

    def delete(self, id):
        itinerary = Itinerary.query.filter_by(id=id).first()

        db.session.delete(itinerary)
        db.session.commit()


# Add routes to the API
api.add_resource(Itineraries, '/itineraries')
api.add_resource(ItineraryByID, '/itineraries/<int:id>')



     # destination classes
        
class Destinations(Resource):
    def get(self):
        destinations = [destination.to_dict() for destination in Destination.query.all()]
        return make_response(jsonify(destinations), 200)

    def post(self):
        data = request.get_json()

        # Validate itinerary exists
        existing_itinerary = Itinerary.query.filter_by(id=data['itinerary_id']).first()
        if not existing_itinerary:
            return make_response(jsonify({'message': 'itinerary does not exist'}), 400)

        
        # Create a new destination
        new_destination = Destination(
            name=data['name'],
            itinerary_id=data['itinerary_id']
        )

        # Save to the database
        db.session.add(new_destination)
        try:
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            return {'error': str(e)}, 500

        return make_response(jsonify({'message': 'Destination successfully created', 'destination': new_destination.to_dict()}), 201)
   


class DestinationByID(Resource):
    def get(self, id):
        destination = Destination.query.filter_by(id=id).first().to_dict()
        return make_response(jsonify(destination), 200)

    def patch(self, id):
        destination = Destination.query.filter_by(id=id).first()
        if not destination:
            return make_response(jsonify({'error': 'Destination not found'}), 404)

        data = request.get_json()

        for key, value in data.items():
            setattr(destination, key, value)

        db.session.commit()

        return make_response(jsonify(destination.to_dict()), 200)

    def delete(self, id):
        destination = Destination.query.filter_by(id=id).first()

        db.session.delete(destination)
        db.session.commit() 


        # Add routes to the API
api.add_resource(Destinations, '/destinations')
api.add_resource(DestinationByID, '/destinations/<int:id>')



# accommodation classes
        
class Accommodations(Resource):
    def get(self):
        accommodations = [accommodation.to_dict() for accommodation in Accommodation.query.all()]
        return make_response(jsonify(accommodations), 200)

    def post(self):
        data = request.get_json()

        # Validate destination exists
        existing_destination = Destination.query.filter_by(id=data['destination_id']).first()
        if not existing_destination:
            return make_response(jsonify({'message': 'Destination does not exist'}), 400)

        try:
            # Convert price to a float
            price = float(data['price'])  
        except ValueError:
            return make_response(jsonify({'error': 'Invalid price format'}), 400)
        
        try:
                # Convert string dates to Python date objects
                check_in_date = datetime.strptime(data['check_in_date'], "%Y-%m-%d").date()
                check_out_date = datetime.strptime(data['check_out_date'], "%Y-%m-%d").date()
        except ValueError:
                return make_response(jsonify({'error': 'Invalid date format. Use YYYY-MM-DD'}), 400)

        # Create a new accommodation
        new_accommodation = Accommodation(
            name=data['name'],
            address=data['address'],
            check_in_date=check_in_date,
            check_out_date=check_out_date,
            price=price,  # Ensuring correct type
            destination_id=data['destination_id']
        )

        # Save to the database
        db.session.add(new_accommodation)
        try:
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            return {'error': str(e)}, 500

        return make_response(jsonify({
            'message': 'Accommodation successfully created',
            'accommodation': new_accommodation.to_dict()
        }), 201)


class AccommodationByID(Resource):
    def get(self, id):
        accommodation = Accommodation.query.filter_by(id=id).first().to_dict()
        return make_response(jsonify(accommodation), 200)

    def patch(self, id):
        accommodation = Accommodation.query.filter_by(id=id).first()
        if not accommodation:
            return make_response(jsonify({'error': 'Accommodation not found'}), 404)

        data = request.get_json()

        for key, value in data.items():
            if key in ["check_in_date", "check_out_date"]:  # Handling date fields
                try:
                    # Convert date string to Python date object
                    value = datetime.strptime(value, "%Y-%m-%d").date()
                except ValueError:
                    return make_response(jsonify({'error': f'Invalid format for {key}. Use YYYY-MM-DD'}), 400)
                
            if key == "price":  # Handling price field
                try:
                    value = float(value)  # Convert price to a float
                except ValueError:
                    return make_response(jsonify({'error': 'Invalid price format. It must be a number.'}), 400)
                
            setattr(accommodation, key, value)  # Set the value for the attribute

        db.session.commit()  # Commit changes to the database

        return make_response(jsonify(accommodation.to_dict()), 200)

    def delete(self, id):
        accommodation = Accommodation.query.filter_by(id=id).first()

        if accommodation:
            db.session.delete(accommodation)
            db.session.commit()

            return make_response(jsonify({'message': 'Accommodation deleted successfully'}), 200)
        
        return make_response(jsonify({'error': 'Accommodation not found'}), 404)



       # Add routes to the API
api.add_resource(Accommodations, '/accommodations')
api.add_resource(AccommodationByID, '/accommodations/<int:id>')
 


# activity classes
        
class Activities(Resource):
    def get(self):
        activities = [activity.to_dict() for activity in Activity.query.all()]
        return make_response(jsonify(activities), 200)

    def post(self):
        data = request.get_json()

        # Validate destination exists
        existing_destination = Destination.query.filter_by(id=data['destination_id']).first()
        if not existing_destination:
            return make_response(jsonify({'message': 'Destination does not exist'}), 400)

        # Create a new activity
        new_activity = Activity(
            name=data['name'],
            description=data['description'],
            destination_id=data['destination_id']
        )

        # Save to the database
        db.session.add(new_activity)
        try:
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            return {'error': str(e)}, 500

        return make_response(jsonify({
            'message': 'Activity successfully created',
            'activity': new_activity.to_dict()
        }), 201)
    

class ActivityByID(Resource):
    def get(self, id):
        activity = Activity.query.filter_by(id=id).first().to_dict()
        return make_response(jsonify(activity), 200)

    def patch(self, id):
        activity = Activity.query.filter_by(id=id).first()
        if not activity:
            return make_response(jsonify({'error': 'Activity not found'}), 404)

        data = request.get_json()

        for key, value in data.items():    
            setattr(activity, key, value)  # Set the value for the attribute

        db.session.commit()  # Commit changes to the database

        return make_response(jsonify(activity.to_dict()), 200)

    def delete(self, id):
        activity = Activity.query.filter_by(id=id).first()

        if activity:
            db.session.delete(activity)
            db.session.commit()

            return make_response(jsonify({'message': 'Activity deleted successfully'}), 200)
        
        return make_response(jsonify({'error': 'Activity not found'}), 404)


# Add routes to the API
api.add_resource(Activities, '/activities')
api.add_resource(ActivityByID, '/activities/<int:id>')
 

if __name__ == '__main__':
    with app.app_context():
        app.run(port=5050, debug=True)