# Football Matcher

A simple Flask web application to manage football pitch reservations and teams.

## Features
- View pitch schedule and existing reservations
- Register, login, and manage user profiles
- Create teams and view a leaderboard
- Make reservations for available slots

## Setup
1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
2. Run the application:
   ```bash
   python main.py
   ```
The app uses SQLite for storage and will create `football.db` on first run.

## Frontend

This project now includes a React frontend located in the `frontend/` folder.

### Development

1. Install Node dependencies:
   ```bash
   cd frontend
   npm install
   ```
2. Start the development server:
   ```bash
   npm run dev
   ```
   The React app proxies API requests to the Flask backend.

### Production build

To build the frontend and serve it with Flask:

1. Build the React app:
   ```bash
   cd frontend
   npm run build
   ```
   This generates static files in `frontend/dist/`.
2. Run the Flask application as usual:
   ```bash
   python main.py
   ```
   Flask will serve the contents of `frontend/dist` at the root URL.
