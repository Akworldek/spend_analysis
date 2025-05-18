import os
import sys
import argparse
import django
from django.core.management import execute_from_command_line


def setup_django_environment():
    """Set up Django environment"""
    print(sys.path)
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'src.configs.settings')
    django.setup()


def run_server(host='127.0.0.1', port=8000):
    """Run the Django development server"""
    print(f"Starting Spend Analysis server at http://{host}:{port}/")
    execute_from_command_line(['manage.py', 'runserver', f'{host}:{port}'])


def create_superuser():
    """Create a superuser for the admin interface"""
    from django.contrib.auth.models import User
    try:
        if not User.objects.filter(is_superuser=True).exists():
            username = input("Enter superuser username: ")
            email = input("Enter superuser email: ")
            password = input("Enter superuser password: ")
            User.objects.create_superuser(username, email, password)
            print("Superuser created successfully!")
        else:
            print("Superuser already exists.")
    except Exception as e:
        print(f"Error creating superuser: {e}")


def setup_initial_data():
    """Set up initial data for the application"""
    from src.backend.models import Category

    # Default categories
    default_categories = [
        {"name": "Food & Dining", "description": "Groceries, restaurants, etc.", "color": "#FF5733"},
        {"name": "Entertainment", "description": "Movies, games, etc.", "color": "#33FF57"},
        {"name": "Transportation", "description": "Gas, public transit, etc.", "color": "#3357FF"},
        {"name": "Housing", "description": "Rent, mortgage, utilities, etc.", "color": "#F633FF"},
        {"name": "Shopping", "description": "Clothing, electronics, etc.", "color": "#FF33A1"},
        {"name": "Health & Fitness", "description": "Medical expenses, gym, etc.", "color": "#33FFF6"},
        {"name": "Personal Care", "description": "Haircuts, cosmetics, etc.", "color": "#FFF633"},
        {"name": "Education", "description": "Tuition, books, etc.", "color": "#FF8C33"},
    ]

    print("Setting up initial data...")
    try:
        for category_data in default_categories:
            Category.objects.get_or_create(
                name=category_data["name"],
                defaults={
                    "description": category_data["description"],
                    "color": category_data["color"],
                }
            )
        print("Initial data setup complete!")
    except Exception as e:
        print(f"Error setting up initial data: {e}")


def init_database():
    """Initialize the database with migrations"""
    print("Setting up database...")
    execute_from_command_line(['spend_analysis_main.py', 'makemigrations', 'backend'])
    execute_from_command_line(['spend_analysis_main.py', 'migrate'])
    print("Database setup complete!")


def main():
    """Main entry point"""
    parser = argparse.ArgumentParser(description='Spend Analysis Application')
    parser.add_argument('--run', action='store_true', help='Run the server')
    parser.add_argument('--host', default='127.0.0.1', help='Host to run the server on')
    parser.add_argument('--port', type=int, default=8000, help='Port to run the server on')
    parser.add_argument('--init', action='store_true', help='Initialize the database')
    parser.add_argument('--superuser', action='store_true', help='Create a superuser')
    parser.add_argument('--setup-data', action='store_true', help='Set up initial data')

    args = parser.parse_args()

    setup_django_environment()

    if args.init:
        init_database()

    if args.superuser:
        create_superuser()

    if args.setup_data:
        setup_initial_data()

    if args.run:
        run_server(host=args.host, port=args.port)

    # If no arguments are provided, show help
    if len(sys.argv) == 1:
        parser.print_help()


if __name__ == '__main__':
    main()