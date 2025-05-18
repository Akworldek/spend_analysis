echo Installing Python dependencies...
pip install -r requirements.txt

:: Set up .env file if it doesn't exist
if not exist .env (
    echo Creating .env file from template...
    copy .env.example .env
    echo Please update .env with your settings
)

:: Run Django migrations
echo Running Django migrations...
cd backend
python manage.py migrate
cd ..

:: Start Django server in a new window
echo Starting Django server...
start cmd /k "call venv\Scripts\activate && cd backend && python manage.py runserver"

:: Install Node.js dependencies
echo Installing Node.js dependencies...
cd frontend
call npm install

:: Start React server in a new window
echo Starting React server...
start cmd /k "cd frontend && npm start"

echo Both servers are running. Close the terminal windows to stop.