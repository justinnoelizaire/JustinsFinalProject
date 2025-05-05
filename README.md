# Basketball App

A web application for tracking basketball statistics, team rankings, and game schedules. The app includes both a Flask-based web interface and a Streamlit analytics dashboard.

## Features

- User authentication (register, login, profile management)
- Player statistics
- Team rankings
- Game schedules
- Interactive analytics dashboard (Streamlit)
- Responsive design using Bootstrap

## Installation

1. Create and activate a virtual environment:
```bash
python3 -m venv .venv
source .venv/bin/activate
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

## Running the Application

1. Start the Flask application:
```bash
python app.py
```
The Flask app will be available at http://localhost:5000

2. In a separate terminal, start the Streamlit analytics dashboard:
```bash
streamlit run analytics.py
```
The Streamlit dashboard will be available at http://localhost:8501

## Project Structure

- `app.py` - Main Flask application
- `analytics.py` - Streamlit dashboard
- `templates/` - HTML templates
- `static/` - Static files (CSS, images)
- `requirements.txt` - Project dependencies
