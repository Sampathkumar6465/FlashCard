# Flashcard App 📚

A simple flashcard app built using FastAPI, SQLAlchemy, and MySQL.

## 🚀 Requirements

- Python 3.8+
- MySQL Server running
- pip install -r requirements.txt

Setup Instructions

 Clone the repository:


Install dependencies:
pip install -r requirements.txt
Edit app/database.py with your MySQL credentials if needed.

Create the database in MySQL:
CREATE DATABASE flashcard_db;

Run the table creation script:
python create_tables.py

Start the server:
uvicorn app.main:app --reload

Open in browser:
http://127.0.0.1:8000
