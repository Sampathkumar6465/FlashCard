from sqlalchemy import create_engine, text

DATABASE_URL = "mysql+pymysql://root:Sampath_33@localhost:3306/flashcard_db"

engine = create_engine(DATABASE_URL, echo=True)

try:
    with engine.connect() as conn:
        result = conn.execute(text("SELECT DATABASE();"))
        current_db = result.fetchone()
        print("Connected to database:", current_db[0])
except Exception as e:
    print("Error connecting to DB:", e)
