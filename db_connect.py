from sqlalchemy import create_engine, text

database_name = "flashcard_db"

engine = create_engine(f"mysql+pymysql://root:Sampath_33@localhost/{database_name}")

try:
    with engine.connect() as connection:
        result = connection.execute(text("SELECT DATABASE();"))
        current_db = result.fetchone()
        print(f"Connected to database: {current_db[0]}")
except Exception as e:
    print(f"Error connecting to database: {e}")
