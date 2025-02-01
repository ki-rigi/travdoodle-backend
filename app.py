from flask import Flask, jsonify, request, make_response, session
from flask_restful import Resource,Api
import os
from dotenv import load_dotenv
from flask_cors import CORS
from flask_migrate import Migrate
from model import db
from flask_mail import Mail
from flask_mail import Message


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = ''
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False
app.config['MAIL_SERVER'] = ''
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = ''
app.config['MAIL_PASSWORD'] = ''
app.config['MAIL_DEFAULT_SENDER'] = ''

migrate = Migrate(app, db)
db.init_app(app)
mail = Mail(app)


api = Api(app)

CORS(app)
    

# Load environment variables from .env file
load_dotenv()


from model import db
# Set secret key
app.secret_key = ''

# Define home route
@app.route('/')
def home():
    return '<h1>Travdoodle server<hi>'
    

# Resource classes


if __name__ == '__main__':
    with app.app_context():
        app.run(port=5050, debug=True)