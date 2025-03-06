# Travdoodle API

## Overview
The **Travdoodle API** is a Flask-based RESTful API designed to support the **Travel Itinerary Organizer** application. It provides endpoints for managing users, itineraries, destinations, accommodations, activities, and packing items.

## Features
- User authentication (Login, Logout, Session Check)
- CRUD operations for Users
- CRUD operations for Itineraries
- CRUD operations for Destinations
- CRUD operations for Accommodations
- CRUD operations for Activities
- CRUD operations for Packing Items
- CORS support for cross-origin requests
- Database management using SQLAlchemy & Flask-Migrate

## Tech Stack
- **Backend:** Flask, Flask-RESTful
- **Database:** PostgreSQL (SQLAlchemy ORM)
- **Deployment:** Render
- **Authentication:** Flask sessions
- **Environment Variables:** dotenv

## Setup & Installation
### Prerequisites
Ensure you have the following installed:
- Python 3.x
- PostgreSQL
- Pipenv (for dependency management)

### Installation Steps
1. Clone the repository:
   ```sh
   git clone <repository-url>
   cd travdoodle-backend
   ```
2. Create a virtual environment and install dependencies:
   ```sh
   pipenv install
   ```
3. Set up environment variables in a `.env` file:
   ```sh
   DATABASE_URI=your_postgresql_database_url
   SECRET_KEY=your_secret_key
   FLASK_APP=app.py
   FLASK_ENV=development
   ```
4. Apply database migrations:
   ```sh
   flask db upgrade
   ```
5. Seed the database with sample data:
   ```sh
   python seed.py
   ```
6. Run the application:
   ```sh
   python app.py
   ```

## API Endpoints

### Authentication
| Endpoint      | Method | Description          |
|--------------|--------|----------------------|
| `/login`      | POST   | User login          |
| `/logout`     | DELETE | User logout         |
| `/check_session` | GET | Check user session |

### Users
| Endpoint       | Method  | Description          |
|---------------|---------|----------------------|
| `/users`      | GET     | List all users      |
| `/users`      | POST    | Create a new user   |
| `/users/<id>` | GET     | Get user details    |
| `/users/<id>` | PATCH   | Update user details |
| `/users/<id>` | DELETE  | Delete a user       |

### Itineraries
| Endpoint             | Method  | Description          |
|----------------------|---------|----------------------|
| `/itineraries`       | GET     | List all itineraries |
| `/itineraries`       | POST    | Create an itinerary  |
| `/itineraries/<id>`  | GET     | Get itinerary details |
| `/itineraries/<id>`  | PATCH   | Update itinerary     |
| `/itineraries/<id>`  | DELETE  | Delete itinerary     |

### Destinations
| Endpoint              | Method  | Description          |
|---------------------- |---------|----------------------|
| `/destinations`       | GET     | List all destinations |
| `/destinations`       | POST    | Create a destination |
| `/destinations/<id>`  | GET     | Get destination details |
| `/destinations/<id>`  | PATCH   | Update destination   |
| `/destinations/<id>`  | DELETE  | Delete destination   |

### Accommodations
| Endpoint               | Method  | Description          |
|----------------------- |---------|----------------------|
| `/accommodations`      | GET     | List all accommodations |
| `/accommodations`      | POST    | Create accommodation |
| `/accommodations/<id>` | GET     | Get accommodation details |
| `/accommodations/<id>` | PATCH   | Update accommodation |
| `/accommodations/<id>` | DELETE  | Delete accommodation |

### Activities
| Endpoint          | Method  | Description       |
|------------------ |---------|------------------|
| `/activities`     | GET     | List activities  |
| `/activities`     | POST    | Create activity  |
| `/activities/<id>`| GET     | Get activity details |
| `/activities/<id>`| PATCH   | Update activity  |
| `/activities/<id>`| DELETE  | Delete activity  |

### Packing Items
| Endpoint            | Method  | Description         |
|-------------------- |---------|---------------------|
| `/packing_items`    | GET     | List packing items  |
| `/packing_items`    | POST    | Create packing item |
| `/packing_items/<id>`| GET     | Get packing item details |
| `/packing_items/<id>`| PATCH   | Update packing item |
| `/packing_items/<id>`| DELETE  | Delete packing item |

## Deployment
To deploy the API backend on Render:
1. Push your repository to GitHub.
2. Create a new service on Render, selecting the repo.
3. Add environment variables under **Settings**.
4. Deploy the service.

## License
This project is licensed under the MIT License.

