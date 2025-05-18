# Spend Analysis Application

A full-stack application for analyzing spending patterns using Django REST Framework backend and React frontend.

## Project Structure

```
spend_analysis/
├── backend/             # Django backend
│   ├── spend_analysis/  # Django project settings
│   ├── api/             # Django app for REST API
│   └── ...
├── frontend/            # React frontend
│   ├── src/
│   ├── public/
│   └── ...
├── .env                 # Environment variables (not tracked in git)
└── README.md            # This file
```

## Prerequisites

- Python 3.8+
- Node.js 14+ and npm
- PostgreSQL (optional, can use SQLite for development)

## Local Development Setup

### 1. Clone the Repository

```bash
git clone https://github.com/Akworldek/spend_analysis.git
cd spend_analysis
```

### 2. Backend Setup

```bash
# Create a virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Create .env file
cp .env.example .env
# Edit .env with your settings

# Run migrations
cd backend
python manage.py migrate

# Create superuser (optional)
python manage.py createsuperuser

# Run development server
python manage.py runserver
```

### 3. Frontend Setup

```bash
# Navigate to frontend directory
cd frontend

# Install dependencies
npm install

# Run development server
npm start
```

### 4. Access the Application

- Backend: http://localhost:8000/
- Admin interface: http://localhost:8000/admin/
- API: http://localhost:8000/api/
- Frontend: http://localhost:3000/

## API Documentation

The backend provides RESTful API endpoints for spending data:

- `GET /api/transactions/` - List all transactions
- `POST /api/transactions/` - Create a new transaction
- `GET /api/transactions/{id}/` - Retrieve a specific transaction
- `PUT /api/transactions/{id}/` - Update a transaction
- `DELETE /api/transactions/{id}/` - Delete a transaction
- `GET /api/categories/` - List all categories

## Environment Variables

The application uses the following environment variables:

- `DEBUG` - Enable/disable Django debug mode
- `SECRET_KEY` - Django secret key
- `DB_ENGINE` - Database engine
- `DB_NAME` - Database name
- `DB_USER` - Database user
- `DB_PASSWORD` - Database password
- `DB_HOST` - Database host
- `DB_PORT` - Database port
- `CORS_ALLOW_ALL_ORIGINS` - Allow all origins for CORS
- `CORS_ALLOWED_ORIGINS` - Comma-separated list of allowed origins

## Deployment

For production deployment, make sure to:

1. Set `DEBUG=False` in .env
2. Set a strong `SECRET_KEY` in .env
3. Configure proper `ALLOWED_HOSTS` and `CORS_ALLOWED_ORIGINS`
4. Use a production-ready database
5. Set up a proper web server (like Nginx)
6. Build the React frontend with `npm run build`