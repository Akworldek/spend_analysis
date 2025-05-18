Spend Analysis Application
A full-stack web application for tracking and analyzing personal spending.
Features

Track transactions with categories
Upload CSV files of transactions
Visualize spending patterns
User authentication and profiles
Responsive design for mobile and desktop

Technology Stack

Backend: Django, Django REST Framework
Frontend: React, Bootstrap
Database: SQLite (default), can be configured for PostgreSQL or MySQL
Visualization: Chart.js

Getting Started
Prerequisites

Python 3.8+
Node.js 14+
pip (Python package manager)
npm (Node.js package manager)

Installation

Clone the repository

bashgit clone https://github.com/Akworldek/spend_analysis.git
cd spend_analysis

Create and activate a virtual environment

bashpython -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

Install Python dependencies

bashpip install -r requirements.txt

Install Node.js dependencies

bashnpm install

Initialize the database

bashpython spend_analysis_main.py --init

Create a superuser

bashpython spend_analysis_main.py --superuser

Set up initial data

bashpython spend_analysis_main.py --setup-data
Running the Application
Run the server:
bashpython spend_analysis_main.py --run
The application will be available at http://127.0.0.1:8000/
Development
For frontend development:
bashnpm run dev
Project Structure

spend_analysis/ - Django project settings
src/ - Main application code

backend/ - Django backend

models.py - Database models
views.py - API views
serializers.py - REST API serializers
urls.py - API URL routing
auth_urls.py - Authentication URL routing


views/ - React frontend components

api.js - API client
landing_page.py - Landing page component


configs/ - Configuration files
utils/ - Utility functions


templates/ - Django HTML templates
static/ - Static files (CSS, JS, images)
media/ - User-uploaded files
spend_analysis_main.py - Main entry point

Deploying to Production
Option 1: Heroku

Create a Heroku account and install the Heroku CLI
Login to Heroku CLI

bashheroku login

Create a new Heroku app

bashheroku create your-app-name

Add PostgreSQL add-on

bashheroku addons:create heroku-postgresql:hobby-dev

Set up environment variables

bashheroku config:set DJANGO_SECRET_KEY=your-secret-key
heroku config:set DJANGO_DEBUG=False

Deploy to Heroku

bashgit push heroku main
Option 2: DigitalOcean

Create a DigitalOcean account
Create a new Droplet with Ubuntu
SSH into your Droplet
Clone the repository
Set up environment variables
Install dependencies
Set up Nginx and Gunicorn

License
This project is licensed under the MIT License - see the LICENSE file for details.
Contributing

Fork the repository
Create a feature branch
Commit your changes
Push to the branch
Create a new Pull Request